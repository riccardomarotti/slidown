# -*- coding: utf-8 -*-

import os
import sys
import pypandoc
import bs4


def get_reveal_js_path():
    """Get the path to reveal.js, handling PyInstaller, pip installation, and source"""
    if hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        return os.path.join(sys._MEIPASS, 'reveal.js')
    else:
        # Try different possible locations
        possible_paths = [
            # Pip installation: reveal.js inside slidown package
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reveal.js'),
            # Source development: reveal.js in parent directory  
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reveal.js'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        # If none exist, provide detailed diagnostic info
        error_msg = (
            f"reveal.js directory not found.\n"
            f"Searched in: {possible_paths}\n"
            f"Current working directory: {os.getcwd()}\n"
            f"Python executable: {sys.executable}\n"
            f"__file__ location: {__file__}"
        )
        raise FileNotFoundError(error_msg)


def _generate_presentation_html(presentation_md_text, theme='white'):
    reveal_js_path = get_reveal_js_path()

    setup_pandoc_for_pyinstaller()

    return pypandoc.convert_text(presentation_md_text,
                                 'revealjs',
                                 extra_args=['-V', 'revealjs-url:' + reveal_js_path,
                                             '--embed-resources',
                                             '--standalone',
                                             '-V', 'transition:slide',
                                             '-V', 'theme:' + theme],
                                 format='md')


def generate_presentation_html(presentation_md_file, theme='white'):
    md = open(presentation_md_file).read()
    return _generate_presentation_html(md, theme)


def get_changed_slide(old_html, new_html):
    soup_old = bs4.BeautifulSoup(old_html, 'html.parser')
    soup_new = bs4.BeautifulSoup(new_html, 'html.parser')

    if old_html == new_html:
        raise(RuntimeError('Slides have no differences.'))

    horizontal_index, vertical_index = get_changed_with_vertical(soup_old,
                                                                 soup_new)

    if horizontal_index != -1:
        return horizontal_index, vertical_index

    slides_old = get_horizontal_slides(soup_old)
    slides_new = get_horizontal_slides(soup_new)

    changed_slides_indexes = [index for index, slide in enumerate(slides_new)
                              if index >= len(slides_old)
                              or slide.get_text().strip() != slides_old[index].get_text().strip()
                              or slide.attrs != slides_old[index].attrs
                              ]

    
    # Handle case where slides were removed
    if not changed_slides_indexes:
        if len(slides_new) < len(slides_old):
            # Slides were removed, navigate to the last existing slide
            # But return the index where deletion occurred (first removed slide)
            return len(slides_new), 0
        else:
            # This shouldn't happen if we detect HTML differences
            return 0, 0
    
    return changed_slides_indexes[0], 0


def get_changed_with_vertical(soup_old, soup_new):
    """Find changes in vertical slide structure"""
    containers_old = get_vertical_slides(soup_old)
    containers_new = get_vertical_slides(soup_new)

    # If no vertical slides, let horizontal logic handle it
    if len(containers_old) == 0 or len(containers_new) == 0:
        return -1, -1

    # Compare each container (horizontal slide with verticals)
    for h_index, container_new in enumerate(containers_new):
        if h_index >= len(containers_old):
            # New horizontal slide added
            return h_index, 0
            
        container_old = containers_old[h_index]
        
        # Get child sections (vertical slides) within this container
        children_old = container_old.find_all('section', recursive=False)
        children_new = container_new.find_all('section', recursive=False)
        
        # Compare vertical slides within this container
        for v_index, child_new in enumerate(children_new):
            if v_index >= len(children_old):
                # New vertical slide added
                return h_index, v_index
            
            child_old = children_old[v_index]
            if child_new.get_text().strip() != child_old.get_text().strip():
                # Vertical slide content changed
                return h_index, v_index
    
    # Check for removed slides
    if len(containers_new) < len(containers_old):
        return len(containers_new), 0
        
    # No changes found
    return -1, -1


def get_horizontal_slides(soup):
    """Get top-level slides (horizontal navigation)"""
    slides_div = soup.find('div', class_='slides')
    if not slides_div:
        return []
    
    # Get direct children sections of the slides div
    return slides_div.find_all('section', recursive=False)

def get_vertical_slides(soup):
    """Get slide containers that have vertical slides (nested sections)"""
    # Get only horizontal slides (top-level) that contain vertical slides
    horizontal_slides = get_horizontal_slides(soup)
    containers = []
    for section in horizontal_slides:
        # Check if this section contains other sections (has vertical slides)
        child_sections = section.find_all('section', recursive=False)
        if child_sections:
            containers.append(section)
    return containers


def setup_pandoc_for_pyinstaller():
    try:
        pypandoc._ensure_pandoc_path()
    except OSError as error:
        if hasattr(sys, '_MEIPASS'):
            pypandoc.__pandoc_path = os.path.join(
                sys._MEIPASS,  'pandoc/pandoc')
        else:
            raise(error)
