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

presentation_file_watcher = QtCore.QFileSystemWatcher(
    [presentation_md_file,
     os.path.dirname(presentation_md_file)])

presentation_file_watcher.fileChanged.connect(
    lambda file_name: monitor.on_file_changed(file_name, web_view,
                                              presentation_html,
                                              presentation_file_watcher,
                                              presentation_html_file))

presentation_file_watcher.directoryChanged.connect(
    lambda directory_name: monitor.on_directory_changed(
        directory_name, presentation_md_file, presentation_file_watcher))


layout = QtWidgets.QVBoxLayout()
web_view = QtWebKitWidgets.QWebView()
web_view.load(QtCore.QUrl('file://' + presentation_html_file))

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
        presentation_html_file,
        themes[index].lower()))
lower_window_layout.addWidget(themes_combo)

group = QtWidgets.QGroupBox()
group.setLayout(lower_window_layout)


layout.addWidget(group)

main_widget.setWindowTitle('Slidown: ' + os.path.basename(presentation_md_file))
main_widget.show()

sys.exit(app.exec_())
