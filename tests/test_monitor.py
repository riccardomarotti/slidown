# -*- coding: utf-8 -*-

import os
import time
import tempfile

from unittest.mock import MagicMock

from slidown import monitor, core

def test_check_changes_with_not_existing_path():
    previous = {
        'filename': 'not_existing_file',
        'previous_modify_date': 'a modified date'
    }

    current = 'anything'

    expected_output = {
        'filename': 'not_existing_file',
        'previous_modify_date': 'a modified date',
        'changed': False
    }

    assert monitor.check_changes(previous, current) == expected_output

def test_check_changes_with_existing_not_modified_path():
    with tempfile.TemporaryFile() as a_file:
        modified_date = os.path.getmtime(a_file.name)

        previous = {
            'filename': a_file.name,
            'previous_modify_date': modified_date,
            'changed': False
        }

        current = 'anything'

        expected_output = {
            'filename': a_file.name,
            'previous_modify_date': modified_date,
            'changed': False
        }

        assert monitor.check_changes(previous, current) == expected_output

def test_check_changes_with_existing_modified_path():
    now = time.time()
    then = now + 10

    with tempfile.NamedTemporaryFile() as a_file:
        current = 'anything'

        previous = {
            'filename': a_file.name,
            'previous_modify_date': os.path.getmtime(a_file.name),
            'changed': False
        }

        os.utime(a_file.name, (then, then))

        expected_output = {
            'filename': a_file.name,
            'previous_modify_date': os.path.getmtime(a_file.name),
            'changed': True
        }

        assert monitor.check_changes(previous, current) == expected_output

def test_create_new_html_with_changed_slide():
    core.generate_presentation_html = lambda file_name, theme: 'a new html text'
    core.get_changed_slide = lambda previous_html, new_html: 'the changed slide'

    with tempfile.NamedTemporaryFile() as an_input_file:
        an_input_file_name = an_input_file.name

        expected_output = {
            'html': 'a new html text',
            'file_name': an_input_file_name,
            'changed_slide': 'the changed slide'
        }

        actual_output = monitor.create_new_html({
            'html': 'an old html text',
            'file_name': an_input_file_name,
            'changed_slide': 'an old changed slide'
        }, {})

        assert expected_output, actual_output == expected_output

def test_create_new_html_with_no_changes():
    core.generate_presentation_html = lambda file_name, theme: 'generated html text'

    with tempfile.NamedTemporaryFile() as an_input_file:
        an_input_file_name = an_input_file.name

        expected_output = {
            'html': 'generated html text',
            'file_name': an_input_file_name,
            'changed_slide': None
        }

        actual_output = monitor.create_new_html({
            'html': 'generated html text',
            'file_name': an_input_file_name,
            'changed_slide': 'an old changed slide'
        }, {})

        assert actual_output == expected_output

def test_load_new_html():
    with tempfile.NamedTemporaryFile() as output_file:
        mock_webview = MagicMock()
        monitor.load_new_html('html text', (1,2), output_file.name, mock_webview)

        assert open(output_file.name).read() == 'html text'

        mock_webview.reload.assert_called_with()
        mock_webview.webview.loadFinished.connect.assert_called_once()
        
        callback = mock_webview.webview.loadFinished.connect.call_args[0][0]
        callback()
        
        mock_webview.load.assert_called_with('file://' + output_file.name + '#/1/2')


def test_refresh_theme():
    with tempfile.NamedTemporaryFile() as output_file:
        core.generate_presentation_html = MagicMock(return_value='some html text')
        mock_webview = MagicMock()
        
        mock_webview.show_loading = MagicMock()
        mock_webview.hide_loading = MagicMock()

        # Create QApplication if it doesn't exist (needed for Qt signals)
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        monitor.refresh_presentation_theme('a file name',
                                           mock_webview,
                                           output_file.name,
                                           'a theme')

        # Wait for the worker thread to complete and process events
        import time
        for _ in range(10):  # Try multiple times
            app.processEvents()
            time.sleep(0.01)
            if open(output_file.name).read():
                break

        assert open(output_file.name).read() == 'some html text'
        mock_webview.load.assert_called_with('file://' + output_file.name)
        mock_webview.show_loading.assert_called_once()
        mock_webview.hide_loading.assert_called_once()
        core.generate_presentation_html.assert_called_with('a file name', 'a theme')
