# -*- coding: utf-8 -*-

import os
import pytest

from slidown import core

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

    with pytest.raises(RuntimeError):
        core.get_changed_slide(html1, html2)


def test_first_slide_different():
    html1 = '<section class="slide">Single Horizontal Slide</section>'
    html2 = '<section class="slide">Single Horizontal Slide Different</section>'

    assert core.get_changed_slide(html1, html2) == (0,0)

def test_second_slide_different():
    html1 = '\
<section class="slide">First Horizontal Slide</section>\
<section class="slide">Second Horizontal Slide</section>\
'
    html2 = '\
<section class="slide">First Horizontal Slide</section>\
<section class="slide">Second  different Horizontal Slide</section>\
'
    assert core.get_changed_slide(html1, html2) == (1,0)


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

    assert core.get_changed_slide(html1, html2) == (1, 0)


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

    assert core.get_changed_slide(html1, html2) == (1, 0)


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

    assert core.get_changed_slide(html1, html2) == (2,0)

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

    assert core.get_changed_slide(html1, html2) == (1, 2)


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

    assert core.get_changed_slide(html1, html2) == (0,2)

def test_bug_when_adding_background_images():
    html1 = """
<section id="big-title" class="slide level2" data-background="image url">
<h1>Big Title</h1>
</section><section id="title-1" class="slide level2" data-background="image url">
<h1>Title 1</h1>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
</section>"""

    html2 = """
<section id="big-title" class="slide level2" data-background="image url">
<h1>Big Title</h1>
</section><section id="title-1" class="slide level2">
<h1>Title 1</h1>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
</section>"""

    assert core.get_changed_slide(html1, html2) == (1,0)

@pytest.fixture()
def pypandoc():
    def os_error():
        raise OSError

    import pypandoc
    pypandoc._ensure_pandoc_path = os_error
    return pypandoc

def test_setup_pandoc_not_found_and_not_pyinstaller(pypandoc):
    with pytest.raises(OSError):
        core.setup_pandoc_for_pyinstaller()

def test_setup_pandoc_not_found_and_pyinstaller_present(pypandoc):
    import sys
    sys._MEIPASS = '/a/path/'

    core.setup_pandoc_for_pyinstaller()

    assert pypandoc.__pandoc_path == '/a/path/pandoc/pandoc'
