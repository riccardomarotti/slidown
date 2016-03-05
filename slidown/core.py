# -*- coding: utf-8 -*-

import os
import pypandoc
import difflib

def generate_presentation_html(presentation_md_file):
    reveal_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'reveal.js')

    return pypandoc.convert(presentation_md_file,
                            'revealjs',
                            extra_args=['-V', 'revealjs-url:' + reveal_js_path,
                                        '--self-contained',
                                        '-V', 'theme:white'])

def get_changed_slide(old_html, new_html):
    return 0
