# -*- coding: utf-8 -*-

from PyQt5 import QtCore

def full_screen_change(mode, main_widget):
    {QtCore.Qt.Checked: main_widget.showFullScreen,
     QtCore.Qt.Unchecked: main_widget.showNormal}[mode]()

def mode_change(mode, main_widget):
    opacity = {QtCore.Qt.Checked: 0.8,
               QtCore.Qt.Unchecked: 1} [mode]
    main_widget.setWindowOpacity(opacity)

    window_flags = {QtCore.Qt.Checked: QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint,
                    QtCore.Qt.Unchecked: QtCore.Qt.Window} [mode]
    main_widget.setWindowFlags(window_flags)

    main_widget.show()
