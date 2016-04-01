# -*- coding: utf-8 -*-

import os
import tempfile
from nose.tools import assert_equals

from .. import config


def test_load_not_existing_config():
    with tempfile.TemporaryDirectory() as temp_dir:
        configuration_file = os.path.join(temp_dir, 'config.json')
        import appdirs
        appdirs.user_config_dir = lambda any_appname: temp_dir

        config_hash = config.load()

        assert_equals("{}", open(configuration_file).read())
        assert_equals({}, config_hash)

def test_load_existing_config():
    with tempfile.TemporaryDirectory() as temp_dir:
        configuration_file = os.path.join(temp_dir, 'config.json')
        open(configuration_file, 'w+').write('{"a json": "config"}')

        import appdirs
        appdirs.user_config_dir = lambda any_appname: temp_dir


        config_hash = config.load()

        assert_equals('{"a json": "config"}', open(configuration_file).read())
        assert_equals({'a json': 'config'}, config_hash)

def test_save():
    config_hash = {
        'hash': 'of configuration',
        'with': 'some',
        'interesting': 'values'
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        configuration_file = os.path.join(temp_dir, 'config.json')
        import appdirs
        appdirs.user_config_dir = lambda any_appname: temp_dir

        config.save(config_hash)

        assert_equals(config_hash, config.load())
