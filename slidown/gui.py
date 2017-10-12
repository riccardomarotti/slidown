# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets

from rx.concurrency import QtScheduler

from slidown import monitor, file_utils

def create_qt_application(argv):
    return QtWidgets.QApplication(argv)

def generate_window(presentation_html_file,
                    presentation_md_file,
                    window_title):

    layout = QtWidgets.QVBoxLayout()
    web_view = QtWebEngineWidgets.QWebEngineView()
    wrapped_web_view = WebViewWrapper(web_view)
    wrapped_web_view.load('file://' + presentation_html_file)

    layout.addWidget(web_view)
    main_widget = QtWidgets.QWidget()
    main_widget.setLayout(layout)

    mode_checkbox = QtWidgets.QCheckBox()
    mode_checkbox.setText('Edit mode')
    mode_checkbox.stateChanged.connect(lambda state: mode_change(state,
                                                                 main_widget))

    open_editor_button = QtWidgets.QPushButton(text='Editor')
    open_editor_button.clicked.connect(lambda evt: file_utils.start(presentation_md_file))

    open_editor_browser = QtWidgets.QPushButton(text='Browser')
    open_editor_browser.clicked.connect(lambda evt: file_utils.start(presentation_html_file))


    lower_window_layout = QtWidgets.QHBoxLayout()
    lower_window_layout.addWidget(mode_checkbox)
    lower_window_layout.addWidget(open_editor_button)
    lower_window_layout.addWidget(open_editor_browser)


    monitor.manage_md_file_changes(presentation_md_file,
                                    presentation_html_file,
                                    wrapped_web_view,
                                    QtScheduler(QtCore))


    themes = ['White', 'Black', 'League', 'Beige', 'Sky',
              'Night', 'Serif', 'Simple', 'Solarized']
    themes_combo = QtWidgets.QComboBox()
    themes_combo.addItems(themes)
    themes_combo.activated.connect(lambda index: monitor.refresh_presentation_theme(
        presentation_md_file,
        wrapped_web_view,
        presentation_html_file,
        themes[index].lower()))
    lower_window_layout.addWidget(themes_combo)

    group = QtWidgets.QGroupBox()
    group.setLayout(lower_window_layout)


    layout.addWidget(group)

    main_widget.setWindowTitle(window_title)
    main_widget.show()


def ask_for_presentation_file_name(start_dir):
    dialog = QtWidgets.QFileDialog(parent=None,
                                  caption='Open presentation',
                                  directory=start_dir,
                                  filter='Markdown files (*.md)',
                                  options=QtWidgets.QFileDialog.DontConfirmOverwrite)

    dialog.setLabelText(QtWidgets.QFileDialog.Accept, 'Open')
    file_name = None
    if dialog.exec():
        file_name = dialog.selectedFiles()[0]

    return file_name

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


class WebViewWrapper():
    def __init__(self, webview):
        self.webview = webview

    def load(self, url):
        self.webview.load(QtCore.QUrl(url))

    def reload(self):
        self.webview.reload()
