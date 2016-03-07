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
import gui


app = QtWidgets.QApplication(sys.argv)

presentation_md_file = QtWidgets.QFileDialog.getOpenFileName(None,
                                                             'Open presentation',
                                                             os.path.expanduser('~'),
                                                             'Markdown files (*.md)')[0]

if not presentation_md_file:
    sys.exit(0)

presentation_html = core.generate_presentation_html(presentation_md_file)

presentation_file_watcher = QtCore.QFileSystemWatcher(
    [presentation_md_file,
     os.path.dirname(presentation_md_file)])

presentation_file_watcher.fileChanged.connect(
    lambda file_name: monitor.on_file_changed(file_name, web_view,
                                              presentation_html,
                                              presentation_file_watcher))

presentation_file_watcher.directoryChanged.connect(
    lambda directory_name: monitor.on_directory_changed(
        directory_name, presentation_md_file, presentation_file_watcher))


layout = QtWidgets.QVBoxLayout()
web_view = QtWebKitWidgets.QWebView()
web_view.setHtml(presentation_html)

layout.addWidget(web_view)
main_widget = QtWidgets.QWidget()
main_widget.setLayout(layout)

mode_checkbox = QtWidgets.QCheckBox()
mode_checkbox.setText('Edit mode')
mode_checkbox.stateChanged.connect(lambda state: gui.mode_change(state,
                                                             main_widget))

themes = ['White', 'Black', 'League', 'Beige', 'Sky',
          'Night', 'Serif', 'Simple', 'Solarized']

lower_window_layout = QtWidgets.QHBoxLayout()
lower_window_layout.addWidget(mode_checkbox)

themes_combo =QtWidgets.QComboBox()
themes_combo.addItems(themes)
themes_combo.activated.connect(lambda index: monitor.refresh_presentation(
        presentation_md_file,
        web_view,
        presentation_file_watcher,
        themes[index].lower()))
lower_window_layout.addWidget(themes_combo)

export_button = QtWidgets.QPushButton('Export as HTML')


def export_html(presentation_md_file):
    output_file_name = os.path.splitext(presentation_md_file)[0] + '.html'

    presentation_html_file = QtWidgets.QFileDialog.getSaveFileName(None,
                                                                   'Export presentation',
                                                                   output_file_name,
                                                                   'Markdown files (*.md)')[0]
    if not presentation_html_file:
        return

    output = core.generate_presentation_html(presentation_md_file)
    open(presentation_html_file, 'w').write(output)


export_button.clicked.connect(lambda: export_html(presentation_md_file))
lower_window_layout.addWidget(export_button)


group = QtWidgets.QGroupBox()
group.setLayout(lower_window_layout)


layout.addWidget(group)

main_widget.setWindowTitle('Slidown: ' + os.path.basename(presentation_md_file))
main_widget.show()

sys.exit(app.exec_())
