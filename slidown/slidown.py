# -*- coding: utf-8 -*-

import sys
from os.path import expanduser

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


def keypressed(event, stacked_layout):
    if type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_Escape:
        stacked_layout.setCurrentIndex(0)
        event.accept()
    else:
        event.ignore()

app = QtWidgets.QApplication(sys.argv)

import qimage
import slides
import gui

presentation_md_source = gui.get_presentation_md_source()

if not presentation_md_source:
    sys.exit(0)

html_slides = slides.slides_from_markdown(presentation_md_source)
qimages = qimage.qimages_from_htmls(html_slides)
pixmaps = gui.pixmaps_from_qimages(qimages)

main_widget = QtWidgets.QWidget()

stacked_layout = QtWidgets.QStackedLayout()
widget = QtWidgets.QWidget()
grid = gui.layout_for_list(pixmaps, stacked_layout)
widget.setLayout(grid)
scroll_area = QtWidgets.QScrollArea()
scroll_area.setWidget(widget)
stacked_layout.addWidget(scroll_area)
single_widget = QtWidgets.QPushButton()
stacked_layout.addWidget(single_widget)

main_widget.setLayout(stacked_layout)
main_widget.show()

single_widget.keyPressEvent = lambda event: keypressed(event, stacked_layout)

sys.exit(app.exec_())
