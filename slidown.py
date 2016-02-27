# -*- coding: utf-8 -*-

import sys
from os.path import expanduser

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore



def get_presentation_file_name():
    fname = QtWidgets.QFileDialog.getOpenFileName(None,
                                                  'Open presentation',
                                                  expanduser('~'))[0]
    if fname:
        return open(fname, 'r').read()

    return None

def change_layout_to(widget, layout):
    QtWidgets.QWidget().setLayout(widget.layout())
    widget.setLayout(layout)
    widget.resize(QtWidgets.QApplication.instance().activeWindow().size())


def layout_for_list(pixmaps, widget):
    grid = QtWidgets.QGridLayout()
    size = 300
    number_of_columns = size // 100

    for i, pixmap in enumerate(pixmaps):
        button = QtWidgets.QPushButton()
        button.setIcon(pixmap)
        button.setIconSize(QtCore.QSize(size, size))
        button.setFlat(True)
        button.clicked.connect(lambda x, pixmap=pixmap: change_layout_to(widget, layout_for_single(pixmap)))
        grid.addWidget(button, i / number_of_columns, i % number_of_columns)

    return grid

def layout_for_single(pixmap):
    grid = QtWidgets.QGridLayout()

    button = QtWidgets.QPushButton()
    button.setIcon(pixmap)
    button.setIconSize(QtWidgets.QApplication.instance().activeWindow().size())
    button.setFlat(True)
    #button.clicked.connect(lambda x,i=i: open_file_dialog(i))
    grid.addWidget(button, 0, 0)

    return grid




app = QtWidgets.QApplication(sys.argv)

import qimage
import slides

presentation_md_source = get_presentation_file_name()

if not presentation_md_source:
    sys.exit(0)

html_slides = slides.slides_from_html(slides.html_from_markdown(
    presentation_md_source))
qimages = map(qimage.from_html, html_slides)
pixmaps = map(lambda qimage: QtGui.QIcon(QtGui.QPixmap.fromImage(qimage)),
              qimages)

widget = QtWidgets.QWidget()
grid = layout_for_list(pixmaps, widget)
widget.setLayout(grid)
scroll_area = QtWidgets.QScrollArea()
scroll_area.setWidget(widget)
widget.show()
scroll_area.show()

sys.exit(app.exec_())
