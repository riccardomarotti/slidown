# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from os.path import expanduser
import qimage

def get_presentation_md_source():
    fname = QtWidgets.QFileDialog.getOpenFileName(None,
                                                  'Open presentation',
                                                  expanduser('~'))[0]
    if fname:
        return open(fname, 'r').read()

    return None


def single_page_layout(stacked_layout, html_slide):
    web_view = stacked_layout.widget(1)
    web_view.setHtml(html_slide)
    stacked_layout.setCurrentIndex(1)


def layout_for_list(html_slides, stacked_layout):
    grid = QtWidgets.QGridLayout()
    size = 300
    number_of_columns = size // 100

    for i, html_slide in enumerate(html_slides):
        pixmap = pixmap_from_qimage(qimage.qimage_from_html(html_slide))

        button = QtWidgets.QPushButton()
        button.setIcon(pixmap)
        button.setIconSize(QtCore.QSize(size, size))
        button.setFlat(True)
        button.clicked.connect(lambda x, pixmap=pixmap: single_page_layout(stacked_layout, html_slide))
        grid.addWidget(button, i / number_of_columns, i % number_of_columns)

    return grid

def pixmap_from_qimage(qimage):
    return QtGui.QIcon(QtGui.QPixmap.fromImage(qimage))
