# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWebKitWidgets

import monitor

def create_qt_application(argv):
    return QtWidgets.QApplication(argv)

def generate_window(presentation_html_file,
                    presentation_md_file,
                    presentation_html,
                    window_title):

    layout = QtWidgets.QVBoxLayout()
    web_view = QtWebKitWidgets.QWebView()
    web_view.load(QtCore.QUrl('file://' + presentation_html_file))

    layout.addWidget(web_view)
    main_widget = QtWidgets.QWidget()
    main_widget.setLayout(layout)

    mode_checkbox = QtWidgets.QCheckBox()
    mode_checkbox.setText('Edit mode')
    mode_checkbox.stateChanged.connect(lambda state: mode_change(state,
                                                                 main_widget))

    lower_window_layout = QtWidgets.QHBoxLayout()
    lower_window_layout.addWidget(mode_checkbox)

    presentation_file_watcher = monitor.create_presentation_file_watcher(presentation_md_file,
                                                                         web_view,
                                                                         presentation_html,
                                                                         presentation_html_file)

    themes = ['White', 'Black', 'League', 'Beige', 'Sky',
              'Night', 'Serif', 'Simple', 'Solarized']
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

    main_widget.setWindowTitle(window_title)
    main_widget.show()


def ask_for_presentation_file_name(start_dir):
    return QtWidgets.QFileDialog.getOpenFileName(None,
                                          'Open presentation',
                                          start_dir,
                                          'Markdown files (*.md)')[0]

def full_screen_change(mode, main_widget):
    {QtCore.Qt.Checked: main_widget.showFullScreen,
     QtCore.Qt.Unchecked: main_widget.showNormal}[mode]()

def mode_change(edit_checkbox_state, widget):
    function = {QtCore.Qt.Checked: set_edit_mode,
                QtCore.Qt.Unchecked: unset_edit_mode} [edit_checkbox_state]
    function(widget)

def unset_edit_mode(widget):
    widget.setWindowOpacity(1)

    geometry = widget.geometry()

    window_flags = QtCore.Qt.Window & ~(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    widget.setWindowFlags(window_flags)

    widget.setGeometry(geometry)
    widget.show()

def set_edit_mode(widget):
    widget.setWindowOpacity(0.8)

    geometry = widget.geometry()

    window_flags = widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
    widget.setWindowFlags(window_flags)

    widget.setGeometry(geometry)
    widget.show()
