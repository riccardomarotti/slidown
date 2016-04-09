# -*- coding: utf-8 -*-

import os, tempfile

from slidown import core


def generate_html(md):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(md)

    return core.generate_presentation_html(temp_file.name)

def test_second_vertical_slide_different():
    md1 = '\
# Single horizontal slide\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical Slide 2\
'
    html1 = generate_html(md1)

    md2 = '\
# Single horizontal slide\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical different Slide 2\
'

    html2 = generate_html(md2)

    assert core.get_changed_slide(html1, html2) == (0,2)

def test_added_new_slide():
    html1 = generate_html('')
    html2 = generate_html('## A title')

    assert core.get_changed_slide(html1, html2) == (0,0)

def test_double_vertical():
    md1 = '\
# First Vertical Slide 1\
\n\n\
## Vertical Slide 1 1\
\n\n\
## Vertical Slide 1 2\
\n\n\
## Vertical Slide 1 3\
\n\n\
# First Vertical Slide 2\
\n\n\
## Vertical Slide 2 1\
\n\n\
## Vertical Slide 2 2\
\n\n\
## Vertical Slide 2 3\
'
    html1 = generate_html(md1)

    md2 = '\
# First Vertical Slide 1\
\n\n\
## Vertical Slide 1 1\
\n\n\
## Vertical Slide 1 2\
\n\n\
## Vertical Slide 1 3\
\n\n\
# First Vertical Slide 2\
\n\n\
## Vertical Slide 2 1\
\n\n\
## Vertical Different Slide 2 2\
\n\n\
## Vertical Slide 2 3\
'
    html2 = generate_html(md2)

    assert core.get_changed_slide(html1, html2) == (1, 2)



def test_more_complex():
    md1 = '\
# Horizontal slide 1\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical Slide 2\
\n\n\
## Vertical Slide 3\
\n\n\
# Horizontal slide 2\
\n\n\
# Horizontal slide 3\
'
    html1 = generate_html(md1)

    md2 = '\
# Horizontal slide 1\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical Slide 2\
\n\n\
## Vertical Slide 3\
\n\n\
# Horizontal slide 2\
\n\n\
# Horizontal different slide 3\
'
    html2 = generate_html(md2)

    assert core.get_changed_slide(html1, html2) == (2,0)

def test_add_new_horizontal():
    md1 = '\
# Horizontal slide 1\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical Slide 2\
\n\n\
'
    html1 = generate_html(md1)

    md2 = '\
# Horizontal slide 1\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical Slide 2\
\n\n\
# New Horizontal\
\n\n\
'
    html2 = generate_html(md2)

    assert core.get_changed_slide(html1, html2) == (1, 0)

def test_delete_last_horizontal():
    md1 = '\
# Horizontal slide 1\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical Slide 2\
\n\n\
# New Horizontal\
\n\n\
'
    html1 = generate_html(md1)

    md2 = '\
# Horizontal slide 1\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical Slide 2\
\n\n\
'
    html2 = generate_html(md2)

    assert core.get_changed_slide(html1, html2) == (1, 0)


def test_bug_when_adding_background_images():
    md1 = """
# Big Title

# Title 1{data-background=image_url}

- Item 1
- Item 2

"""
    html1 = generate_html(md1)

    md2 = """
# Big Title

# Title 1

- Item 1
- Item 2

"""
    html2 = generate_html(md2)

    assert core.get_changed_slide(html1, html2) == (1,0)
