# -*- coding: utf-8 -*-

import os
import time
import tempfile
from nose.tools import assert_equals

from .. import monitor


def test_check_changes_with_not_existing_path():
    previous = {
        'filename': 'not_existing_file',
        'previous_modify_date': 'anything'
    }

    current = 'anything'

    expected_output = {
        'filename': 'not_existing_file',
        'previous_modify_date': -1,
        'changed': True
    }

    assert_equals(expected_output, monitor.check_changes(previous, current))

def test_check_changes_with_existing_not_modified_path():
    a_file = tempfile.NamedTemporaryFile()
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

    assert_equals(expected_output, monitor.check_changes(previous, current))

def test_check_changes_with_existing_modified_path():
    a_file = tempfile.NamedTemporaryFile()
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

    assert_equals(expected_output, monitor.check_changes(previous, current))
