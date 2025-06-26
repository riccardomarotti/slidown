# -*- coding: utf-8 -*-

import os, sys, subprocess

def add_md_extension(file_name):
    return '.'.join([file_name.split('.')[0], 'md'])

def touch(file_name):
    with open(file_name, 'a'):
        os.utime(file_name, None)

def start(file_name):
    open_functions = {
        'darwin': lambda file_name: subprocess.run(['open', file_name]),
        'linux': lambda file_name: subprocess.run(['xdg-open', file_name]),
        'win32': lambda file_name: os.startfile(file_name)
    }

    open_functions[sys.platform](file_name)

