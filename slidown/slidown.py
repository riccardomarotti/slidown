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
                                                             os.path.expanduser('~'))[0]

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


theme_radio_buttons = [gui.theme_radio_button(theme,
                                              presentation_md_file,
                                              web_view,
                                              presentation_file_watcher)
                       for theme in ['White', 'Black', 'League', 'Beige', 'Sky',
                                     'Night', 'Serif', 'Simple', 'Solarized']]
theme_radio_buttons[0].setChecked(True)



lower_window_layout = QtWidgets.QHBoxLayout()
lower_window_layout.addWidget(mode_checkbox)

for button in theme_radio_buttons:
    lower_window_layout.addWidget(button)


group = QtWidgets.QGroupBox()
group.setLayout(lower_window_layout)


layout.addWidget(group)

main_widget.show()




main_widget.setWindowTitle('Slidown: ' + os.path.basename(presentation_md_file))

sys.exit(app.exec_())
