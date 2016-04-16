# -*- coding: utf-8 -*-

import os

def add_md_extension(file_name):
    return '.'.join([file_name.split('.')[0], 'md'])

def touch(file_name):
    with open(file_name, 'a'):
        os.utime(file_name, None)
