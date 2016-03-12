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
