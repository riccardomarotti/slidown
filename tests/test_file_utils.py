# -*- coding: utf-8 -*-
import tempfile, os
from unittest.mock import patch, MagicMock

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

@patch('sys.platform', 'win32')
def test_start_on_windows():
    os.startfile = MagicMock()
    file_utils.start('a file name')

    os.startfile.assert_called_with('a file name')

@patch('sys.platform', 'darwin')
def test_start_on_osx():
    with patch('subprocess.run', MagicMock()) as run:
        file_utils.start('another file name')

        run.assert_called_with(['open', 'another file name'])

@patch('sys.platform', 'linux')
def test_start_on_linux():
    with patch('subprocess.run', MagicMock()) as run:
        file_utils.start('yet another file name')

        run.assert_called_with(['xdg-open', 'yet another file name'])
