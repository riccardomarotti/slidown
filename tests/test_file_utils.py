# -*- coding: utf-8 -*-
import tempfile, os
from slidown import file_utils

def test_add_extension():
    assert file_utils.add_md_extension('/a/path/to/a/filename.md') == '/a/path/to/a/filename.md'
    assert file_utils.add_md_extension('/a/path/to/another/filename') == '/a/path/to/another/filename.md'
    assert file_utils.add_md_extension('/a/path/to/another/filename.') == '/a/path/to/another/filename.md'
    assert file_utils.add_md_extension('/a/path/to/another/filename.other_extension') == '/a/path/to/another/filename.md'

def test_touch():
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_file_name = os.path.join(temp_dir_name, "a_file")
        file_utils.touch(temp_file_name)

        assert os.path.isfile(temp_file_name)
