# -*- coding: utf-8 -*-

import os, sys, subprocess
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

def add_md_extension(file_name):
    return '.'.join([file_name.split('.')[0], 'md'])

def touch(file_name):
    with open(file_name, 'a'):
        os.utime(file_name, None)

def start(file_name):
    # Use QDesktopServices for opening files/URLs, as it's more robust in Qt applications
    # and handles cross-platform differences internally.
    QDesktopServices.openUrl(QUrl.fromLocalFile(file_name))

