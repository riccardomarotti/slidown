# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtWebKitWidgets

import monitor
import core
import gui
import config


app = QtWidgets.QApplication(sys.argv)

configuration = config.get()

if len(sys.argv) == 2:
    presentation_md_file = os.path.abspath(sys.argv[1])
else:
    if not 'last_presentation' in configuration:
        presentation_md_file = QtWidgets.QFileDialog.getOpenFileName(None,
                                                                     'Open presentation',
                                                                     os.path.expanduser('~'),
                                                                     'Markdown files (*.md)')[0]
    else:
        presentation_md_file = configuration['last_presentation']

if not presentation_md_file:
    sys.exit(0)

configuration['last_presentation'] = presentation_md_file
config.save(configuration)

presentation_html = core.generate_presentation_html(presentation_md_file)
presentation_html_file = os.path.splitext(presentation_md_file)[0] + '.html'
open(presentation_html_file, 'w').write(presentation_html)

presentation_file_watcher = monitor.create_filesystem_watcher(presentation_md_file)


gui.generate_window(presentation_html_file,
                    presentation_md_file,
                    presentation_file_watcher,
                    'Slidown: ' + os.path.basename(presentation_md_file))


sys.exit(app.exec_())
