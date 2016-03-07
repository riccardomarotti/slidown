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

    slides_old = soup_old.find_all('section', attrs={'class': 'slide'})
    slides_new = soup_new.find_all('section', attrs={'class': 'slide'})

    horizontal_index = 0
    vertical_index = 0

    for index, slide in enumerate(slides_new):
        if index >= len(slides_old) or slide != slides_old[index]:
            break

        if slide.parent.name == 'section':
            vertical_index += 1
        else:
            vertical_index = 0
            horizontal_index += 1

    return horizontal_index, vertical_index
