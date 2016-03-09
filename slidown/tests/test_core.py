# -*- coding: utf-8 -*-

import os
from nose.tools import assert_equals, raises

from .. import core

@raises(RuntimeError)
def test_get_changed_slide_with_same_html():
    html1 = '\
<section class="slide">\
<h1> A title </h1>\
</section>\
'
    html2 = '\
<section class="slide">\
<h1> A title </h1>\
</section>\
'
    core.get_changed_slide(html1, html2)


def test_first_slide_different():
    html1 = '<section class="slide">Single Horizontal Slide</section>'
    html2 = '<section class="slide">Single Horizontal Slide Different</section>'

    assert_equals((0,0), core.get_changed_slide(html1, html2))

def test_second_slide_different():
    html1 = '\
<section class="slide">First Horizontal Slide</section>\
<section class="slide">Second Horizontal Slide</section>\
'
    html2 = '\
<section class="slide">First Horizontal Slide</section>\
<section class="slide">Second  different Horizontal Slide</section>\
'

    assert_equals((1,0), core.get_changed_slide(html1, html2))

def test_second_vertical_slide_different():
    md1 ='\
# Single horizontal slide\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical Slide 2\
'
    html1 = core._generate_presentation_html(md1)

    md2 = '\
# Single horizontal slide\
\n\n\
## Vertical Slide 1\
\n\n\
## Vertical different Slide 2\
\
'
    html2 = core._generate_presentation_html(md2)

    assert_equals((0,2), core.get_changed_slide(html1, html2))

def test_added_new_slide():
    html1 = core._generate_presentation_html('')
    html2 = core._generate_presentation_html('## A title')

    assert_equals((0,0), core.get_changed_slide(html1, html2))


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
    html1 = core._generate_presentation_html(md1)

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
    html2 = core._generate_presentation_html(md2)

    assert_equals((1, 2), core.get_changed_slide(html1, html2))



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
    html1 = core._generate_presentation_html(md1)

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
    html2 = core._generate_presentation_html(md2)

    assert_equals((2,0), core.get_changed_slide(html1, html2))
