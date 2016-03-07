# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import monitor

def full_screen_change(mode, main_widget):
    {QtCore.Qt.Checked: main_widget.showFullScreen,
     QtCore.Qt.Unchecked: main_widget.showNormal}[mode]()

def mode_change(mode, widget):
    opacity = {QtCore.Qt.Checked: 0.8,
               QtCore.Qt.Unchecked: 1} [mode]
    widget.setWindowOpacity(opacity)

    geometry = widget.geometry()

    window_flags = {QtCore.Qt.Checked: widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint,
                    QtCore.Qt.Unchecked: QtCore.Qt.Window & ~(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint) } [mode]
    widget.setWindowFlags(window_flags)

    widget.setGeometry(geometry)
    widget.show()
