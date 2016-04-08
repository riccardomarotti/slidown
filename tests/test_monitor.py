# -*- coding: utf-8 -*-

import os
import time
import tempfile

from slidown import monitor

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
    with tempfile.NamedTemporaryFile() as a_file:
        current = 'anything'

        previous = {
            'filename': a_file.name,
            'previous_modify_date': os.path.getmtime(a_file.name),
            'changed': False
        }

        time.sleep(0.01) #allows to modified date to change
        os.utime(a_file.name, None)

        expected_output = {
            'filename': a_file.name,
            'previous_modify_date': os.path.getmtime(a_file.name),
            'changed': True
        }

        assert monitor.check_changes(previous, current) == expected_output

def test_create_new_html_with_changed_slide():
    from slidown import core
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
    from slidown import core
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
