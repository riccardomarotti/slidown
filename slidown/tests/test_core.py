# -*- coding: utf-8 -*-

import os
from nose.tools import assert_equals

from .. import core

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
    assert_equals(-1, core.get_changed_slide(html1, html2))

def test_get_changed_slide_simple():
    html0 = '\
<section class="slide">\
<h1> A title </h1>\
</section>\
<section class="slide">\
<h1> Second title </h1>\
</section>\
'
    html1 = '\
<section class="slide">\
<h1> A title </h1>\
</section>\
<section class="slide">\
<h1> A different title title </h1>\
</section>\
'
    assert_equals(1, core.get_changed_slide(html0, html1))

def test_get_changed_slide_with_file():
    current_dir = os.path.dirname(__file__)
    html1 = open(os.path.join(current_dir, 'test_file1.html')).read()
    html2 = open(os.path.join(current_dir, 'test_file2.html')).read()

    assert_equals(3, core.get_changed_slide(html1, html2))
