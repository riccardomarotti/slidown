# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from os.path import expanduser


def get_presentation_md_source():
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

def pixmaps_from_qimages(qimages):
    return map(lambda qimage: QtGui.QIcon(QtGui.QPixmap.fromImage(qimage)),
              qimages)
