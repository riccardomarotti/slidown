# -*- coding: utf-8 -*-

import os
import pypandoc
import bs4

def generate_presentation_html(presentation_md_file, theme='white'):
    reveal_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'reveal.js')

    return pypandoc.convert(presentation_md_file,
                            'revealjs',
                            extra_args=['-V', 'revealjs-url:' + reveal_js_path,
                                        '--self-contained',
                                        '-V', 'transition:slide',
                                        '-V', 'theme:' + theme])

def get_changed_slide(old_html, new_html):
    soup_old = bs4.BeautifulSoup(old_html, 'html.parser')
    soup_new = bs4.BeautifulSoup(new_html, 'html.parser')

    if old_html == new_html:
        raise(RuntimeError('Slides have no differences.'))

    horizontal_index, vertical_index = get_changed_with_vertical(soup_old, soup_new)

    if horizontal_index != -1:
        return horizontal_index, vertical_index

    slides_old = soup_old.find_all('section', attrs={'class': 'slide'})
    slides_new = soup_new.find_all('section', attrs={'class': 'slide'})

    if len(slides_new) > len(slides_old):
        return len(slides_new), 0

    horizontal_index = 0

    for index, slide in enumerate(slides_new):
        if index >= len(slides_old) or slide != slides_old[index]:
            horizontal_index = index
            break

    return horizontal_index, 0

def get_changed_with_vertical(soup_old, soup_new):
    slides_old = soup_old.find_all('section', attrs={'class': None})
    slides_new = soup_new.find_all('section', attrs={'class': None})

    if len(slides_old) == 0 or len(slides_new) == 0:
        return -1, -1

    if len(slides_new) > len(slides_new):
        return len(slides_new), 0

    for hindex, parent_slide in enumerate(slides_new):
        for vindex, child_slide in enumerate(list(parent_slide.children)):
            if hindex >= len(slides_old):
                return hindex, 0
            children = list(slides_old[hindex].children)
            if vindex >= len(children) or child_slide != children[vindex]:
                return hindex, vindex


    return 0,0
