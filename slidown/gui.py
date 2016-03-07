# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import monitor

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
