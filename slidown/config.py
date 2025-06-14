# -*- coding: utf-8 -*-

import os
import appdirs
import json

def load():
    config_file = os.path.join(appdirs.user_config_dir('slidown'),
                               'config.json')
    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            configuration = json.load(f)
    else:
        basedir = os.path.dirname(config_file)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        with open(config_file, 'w') as f:
            f.write('{}')

        configuration = {}


    return configuration

def save(configuration):
    config_file = os.path.join(appdirs.user_config_dir('slidown'),
                               'config.json')
    with open(config_file, 'w') as f:
        json.dump(configuration, f)

def get_presentation_theme(presentation_file):
    """Get the saved theme for a specific presentation file"""
    config = load()
    presentations = config.get('presentations', {})
    return presentations.get(presentation_file, 'white')

def save_presentation_theme(presentation_file, theme):
    """Save the theme for a specific presentation file"""
    config = load()
    if 'presentations' not in config:
        config['presentations'] = {}
    config['presentations'][presentation_file] = theme
    save(config)
