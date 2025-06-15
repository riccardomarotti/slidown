# -*- coding: utf-8 -*-

import os
import tempfile

from slidown import config


def test_load_not_existing_config():
    with tempfile.TemporaryDirectory() as temp_dir:
        configuration_file = os.path.join(temp_dir, 'config.json')
        import appdirs
        appdirs.user_config_dir = lambda any_appname: temp_dir

        config_hash = config.load()

        assert open(configuration_file).read() == "{}"
        assert config_hash == {}

def test_load_existing_config():
    with tempfile.TemporaryDirectory() as temp_dir:
        configuration_file = os.path.join(temp_dir, 'config.json')
        open(configuration_file, 'w+').write('{"a json": "config"}')

        import appdirs
        appdirs.user_config_dir = lambda any_appname: temp_dir


        config_hash = config.load()

        assert open(configuration_file).read() == '{"a json": "config"}'
        assert config_hash == {'a json': 'config'}

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

        assert config.load() == config_hash

def test_not_existing_config_directory():
    temp_dir_name = tempfile.TemporaryDirectory().name

    configuration_file = os.path.join(temp_dir_name, 'config.json')
    import appdirs
    appdirs.user_config_dir = lambda any_appname: temp_dir_name

    config_hash = config.load()

    assert open(configuration_file).read() == "{}"
    assert config_hash == {}

def test_presentation_theme_management():
    with tempfile.TemporaryDirectory() as temp_dir:
        import appdirs
        appdirs.user_config_dir = lambda any_appname: temp_dir
        
        test_file = '/path/to/test.md'
        
        assert config.get_presentation_theme(test_file) == 'white'
        
        config.save_presentation_theme(test_file, 'dark')
        assert config.get_presentation_theme(test_file) == 'dark'
        
        another_file = '/path/to/another.md'
        assert config.get_presentation_theme(another_file) == 'white'
