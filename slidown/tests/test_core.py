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
    html1 = '\
<section class="slide">Single Horizontal Slide</section>\
<section>\
    <section class="slide">Vertical Slide 1</section>\
    <section class="slide">Vertical Slide 2</section>\
</section>\
'

    html2 = '\
<section class="slide">Single Horizontal Slide</section>\
<section>\
    <section class="slide">Vertical Slide 1</section>\
    <section class="slide">Vertical different Slide 2</section>\
</section>\
'
    assert_equals((1,1), core.get_changed_slide(html1, html2))

def test_added_new_slide():
    html1 = ''
    html2 = '\
<section class="slide">\
<h1> A title </h1>\
</section>\
'

    assert_equals((0,0), core.get_changed_slide(html1, html2))
