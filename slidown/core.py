# -*- coding: utf-8 -*-

import os
import pypandoc
import bs4

def generate_presentation_html(presentation_md_file):
    reveal_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'reveal.js')

    return pypandoc.convert(presentation_md_file,
                            'revealjs',
                            extra_args=['-V', 'revealjs-url:' + reveal_js_path,
                                        '--self-contained',
                                        '-V', 'theme:solarized'])

def get_changed_slide(old_html, new_html):
    soup_old = bs4.BeautifulSoup(old_html, 'html.parser')
    soup_new = bs4.BeautifulSoup(new_html, 'html.parser')

    slides_old = soup_old.find_all('section', attrs={'class': 'slide'})
    slides_new = soup_new.find_all('section', attrs={'class': 'slide'})

    different_slide_index = -1

    for index, slide_new in enumerate(slides_new):
        if slide_new != slides_old[index]:
            different_slide_index = index
            break

    return different_slide_index