# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from .. import slides

def test_simple_convert():
  markdown = "#Title"
  expected_output = '<h1>Title</h1>'

  assert_equals(expected_output, slides.html_from_markdown(markdown))

def test_split():
  markdown = '\
# Title 1\n---\n\
# Title 2\n-------- \n\
# Title 3\n***\n\
# Title 4\n* * *\n\
# Title 5\n- - - - -\n\
# Title 6\n*****\n\
# Title 7'

  expected_output = ['<h1>Title 1</h1>',
                     '<h1>Title 2</h1>',
                     '<h1>Title 3</h1>',
                     '<h1>Title 4</h1>',
                     '<h1>Title 5</h1>',
                     '<h1>Title 6</h1>',
                     '<h1>Title 7</h1>']

  assert_equals(expected_output,
                slides.slides_from_html(slides.html_from_markdown(markdown)))


if __name__ == "__main__":
    unittest.main()
