# -*- coding: utf-8 -*-

import os
import sys
import pypandoc
import bs4


def _generate_presentation_html(presentation_md_text, theme='white'):
    reveal_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  '..',
                                  'reveal.js')

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

    slides_old = soup_old.find_all('section', attrs={'class': 'slide'})
    slides_new = soup_new.find_all('section', attrs={'class': 'slide'})

    changed_slides_indexes = [index for index, slide in enumerate(slides_new)
                              if index >= len(slides_old)
                              or slide.get_text().strip() != slides_old[index].get_text().strip()
                              or slide.attrs != slides_old[index].attrs
                              ]

    open('old.html', 'w').write(old_html)
    open('new.html', 'w').write(new_html)
    return changed_slides_indexes[0], 0


def get_changed_with_vertical(soup_old, soup_new):
    slides_old = get_vertical_slides(soup_old)
    slides_new = get_vertical_slides(soup_new)

    no_vertical_slides = len(slides_old) == 0 or len(slides_new) == 0
    if no_vertical_slides:
        return -1, -1

    slide_removed = len(slides_old) > len(slides_new)
    if slide_removed:
        return len(slides_new), 0

    indexes = [(hindex, vindex) for hindex, parent_slide in enumerate(slides_new)
               for vindex, child_slide in enumerate(list(parent_slide.children))
               if len(slides_old) <= hindex
               or vindex >= len(list(slides_old[hindex].children))
               or child_slide != list(slides_old[hindex].children)[vindex]]

    return indexes[0]


def get_vertical_slides(soup):
    return [slide for slide in soup.find_all('section', attrs={'class': None})
            if slide.parent.name != 'section']


def setup_pandoc_for_pyinstaller():
    try:
        pypandoc._ensure_pandoc_path()
    except OSError as error:
        if hasattr(sys, '_MEIPASS'):
            pypandoc.__pandoc_path = os.path.join(
                sys._MEIPASS,  'pandoc/pandoc')
        else:
            raise(error)
