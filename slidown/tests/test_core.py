# -*- coding: utf-8 -*-

import os
from nose.tools import assert_equals

from .. import core


def test_get_changed_slide():
    current_dir = os.path.dirname(__file__)
    html1 = open(os.path.join(current_dir, 'test_file1.html')).read()
    html2 = open(os.path.join(current_dir, 'test_file2.html')).read()

    assert_equals(3, core.get_changed_slide(html1, html2))
