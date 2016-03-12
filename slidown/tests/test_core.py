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


def test_add_new_horizontal():
    html1 = """
<section>
  <section id="horizontal-slide-1" class="titleslide slide level1">
    <h1>Horizontal slide 1</h1>
  </section>
  <section>
    <section id="vertical-slide-1" class="titleslide slide level2">
      <h1>Vertical Slide 1</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-2" class="titleslide slide level2">
      <h1>Vertical Slide 2</h1>
    </section>
  </section>
</section>"""

    html2 = """
<section>
  <section id="horizontal-slide-1" class="titleslide slide level1">
    <h1>Horizontal slide 1</h1>
  </section>
  <section>
    <section id="vertical-slide-1" class="titleslide slide level2">
      <h1>Vertical Slide 1</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-2" class="titleslide slide level2">
      <h1>Vertical Slide 2</h1>
    </section>
  </section>
</section>
<section>
  <section id="new-horizontal" class="titleslide slide level1">
    <h1>New Horizontal</h1>
  </section>
</section>"""

    assert_equals((1, 0), core.get_changed_slide(html1, html2))


def test_bug():
    html1 = """
<section>
  <section id="title-1" class="titleslide slide level2">
    <h1>Title 1</h1>
  </section>
</section>
<section>
  <section id="title-2" class="titleslide slide level2">
    <h1>Title 2</h1>
  </section>
</section>
<section>
  <section id="title-3" class="titleslide slide level2">
    <h1>Title 3</h1>
  </section>
</section>
"""
    html2 ="""
<section id="title-1" class="slide level2">
  <h1>Title 1</h1>
</section>
<section id="title-2" class="slide level2">
  <h1>Title 2</h1>
<p>different text</p>
</section>
<section id="title-3" class="slide level2">
  <h1>Title 3</h1>
</section>"""

    assert_equals((1,0), core.get_changed_slide(html1, html2))


def test_delete_last_horizontal():
    html1 = """
<section>
  <section id="horizontal-slide-1" class="titleslide slide level1">
    <h1>Horizontal slide 1</h1>
  </section>
<section>
  <section id="vertical-slide-1" class="titleslide slide level2">
    <h1>Vertical Slide 1</h1>
  </section>
</section>
<section>
  <section id="vertical-slide-2" class="titleslide slide level2">
    <h1>Vertical Slide 2</h1>
  </section>
</section>
</section>
<section>
  <section id="new-horizontal" class="titleslide slide level1">
    <h1>New Horizontal</h1>
  </section>
</section>
"""

    html2 ="""
<section>
  <section id="horizontal-slide-1" class="titleslide slide level1">
    <h1>Horizontal slide 1</h1>
  </section>
<section>
  <section id="vertical-slide-1" class="titleslide slide level2">
    <h1>Vertical Slide 1</h1>
  </section>
</section>
<section>
  <section id="vertical-slide-2" class="titleslide slide level2">
    <h1>Vertical Slide 2</h1>
  </section>
</section>
</section>"""

    assert_equals((1, 0), core.get_changed_slide(html1, html2))


def test_more_complex():
    html1 = """
<section>
  <section id="horizontal-slide-1" class="titleslide slide level1">
    <h1>Horizontal slide 1</h1>
  </section>
  <section>
    <section id="vertical-slide-1" class="titleslide slide level2">
      <h1>Vertical Slide 1</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-2" class="titleslide slide level2">
      <h1>Vertical Slide 2</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-3" class="titleslide slide level2">
      <h1>Vertical Slide 3</h1>
    </section>
  </section>
</section>
<section>
  <section id="horizontal-slide-2" class="titleslide slide level1">
    <h1>Horizontal slide 2</h1>
  </section>
</section>
<section><section id="horizontal-slide-3" class="titleslide slide level1">
  <h1>Horizontal slide 3</h1>
</section></section>"""

    html2 = """
<section>
  <section id="horizontal-slide-1" class="titleslide slide level1">
    <h1>Horizontal slide 1</h1>
  </section>
  <section>
    <section id="vertical-slide-1" class="titleslide slide level2">
      <h1>Vertical Slide 1</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-2" class="titleslide slide level2">
      <h1>Vertical Slide 2</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-3" class="titleslide slide level2">
      <h1>Vertical Slide 3</h1>
    </section>
  </section>
</section>
<section>
  <section id="horizontal-slide-2" class="titleslide slide level1">
    <h1>Horizontal slide 2</h1>
  </section>
</section>
<section><section id="horizontal-different-slide-3" class="titleslide slide level1">
  <h1>Horizontal different slide 3</h1>
</section></section>"""

    assert_equals((2,0), core.get_changed_slide(html1, html2))

def test_double_vertical():
    html1 = """
<section>
  <section id="first-vertical-slide-1" class="titleslide slide level1">
    <h1>First Vertical Slide 1</h1>
  </section>
  <section>
    <section id="vertical-slide-1-1" class="titleslide slide level2">
      <h1>Vertical Slide 1 1</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-1-2" class="titleslide slide level2">
      <h1>Vertical Slide 1 2</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-1-3" class="titleslide slide level2">
      <h1>Vertical Slide 1 3</h1>
    </section>
  </section>
</section>
<section><section id="first-vertical-slide-2" class="titleslide slide level1">
  <h1>First Vertical Slide 2</h1>
</section><section>
<section id="vertical-slide-2-1" class="titleslide slide level2">
  <h1>Vertical Slide 2 1</h1>
</section></section><section><section id="vertical-slide-2-2" class="titleslide slide level2">
<h1>Vertical Slide 2 2</h1>
</section></section><section><section id="vertical-slide-2-3" class="titleslide slide level2">
<h1>Vertical Slide 2 3</h1>
</section></section></section>
"""
    html2 = """
<section>
  <section id="first-vertical-slide-1" class="titleslide slide level1">
    <h1>First Vertical Slide 1</h1>
  </section>
  <section>
    <section id="vertical-slide-1-1" class="titleslide slide level2">
      <h1>Vertical Slide 1 1</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-1-2" class="titleslide slide level2">
      <h1>Vertical Slide 1 2</h1>
    </section>
  </section>
  <section>
    <section id="vertical-slide-1-3" class="titleslide slide level2">
      <h1>Vertical Slide 1 3</h1>
    </section>
  </section>
</section>
<section><section id="first-vertical-slide-2" class="titleslide slide level1">
  <h1>First Vertical Slide 2</h1>
</section><section>
<section id="vertical-slide-2-1" class="titleslide slide level2">
  <h1>Vertical Slide 2 1</h1>
</section></section><section><section id="vertical-different-slide-2-2" class="titleslide slide level2">
<h1>Vertical Different Slide 2 2</h1>
</section></section><section><section id="vertical-slide-2-3" class="titleslide slide level2">
<h1>Vertical Slide 2 3</h1>
</section></section></section>
"""

    assert_equals((1, 2), core.get_changed_slide(html1, html2))


def test_second_vertical_slide_different():
    html1 = """
<section><section id="single-horizontal-slide" class="titleslide slide level1">
<h1>Single horizontal slide</h1>
</section><section><section id="vertical-slide-1" class="titleslide slide level2">
<h1>Vertical Slide 1</h1>
</section></section><section><section id="vertical-slide-2" class="titleslide slide level2">
<h1>Vertical Slide 2</h1></section>
</section></section>"""

    html2 = """
<section><section id="single-horizontal-slide" class="titleslide slide level1">
<h1>Single horizontal slide</h1>
</section><section><section id="vertical-slide-1" class="titleslide slide level2">
<h1>Vertical Slide 1</h1>
</section></section><section><section id="vertical-different-slide-2" class="titleslide slide level2">
<h1>Vertical different Slide 2</h1>
</section></section></section>"""

    assert_equals((0,2), core.get_changed_slide(html1, html2))
