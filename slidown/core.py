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

    different_slide_index = 0

    for index, slide in enumerate(slides_new):
        if index >= len(slides_old) or slide != slides_old[index]:
            different_slide_index = index
            break

    horizontal_index = 0
    vertical_index = 0

    first = True
    for index in range(0, different_slide_index+1):
        if slides_new[index].parent.name != 'section':
            horizontal_index += 1
            vertical_index = 0
            first = True
        elif index > 0 and slides_new[index-1].nextSibling is not slides_new[index]:
            horizontal_index += 1
            vertical_index = 0
            first = True
        else:
            if first:
                horizontal_index += 1
                first = False
            else:
                vertical_index += 1


    print(horizontal_index-1, vertical_index)
    return horizontal_index-1, vertical_index
