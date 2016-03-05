# -*- coding: utf-8 -*-

import sys
import os
import threading

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWebKitWidgets

import monitor
import core


app = QtWidgets.QApplication(sys.argv)

presentation_md_file = QtWidgets.QFileDialog.getOpenFileName(None,
                                                             'Open presentation',
                                                             os.path.expanduser('~'))[0]

if not presentation_md_file:
    sys.exit(0)

presentation_html = core.generate_presentation_html(presentation_md_file)

main_widget = QtWebKitWidgets.QWebView()
main_widget.setHtml(presentation_html)

#main_widget.loadFinished.connect(lambda: main_widget.page().mainFrame().evaluateJavaScript('Reveal.toggleOverview();'))
main_widget.show()


presentation_file_watcher = QtCore.QFileSystemWatcher(
    [presentation_md_file,
     os.path.dirname(presentation_md_file)])

presentation_file_watcher.fileChanged.connect(
    lambda file_name: monitor.on_file_changed(file_name, [main_widget],
                                              presentation_html))

presentation_file_watcher.directoryChanged.connect(
    lambda directory_name: monitor.on_directory_changed(
        directory_name, presentation_md_file, presentation_file_watcher))


sys.exit(app.exec_())
