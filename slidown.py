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


app = QtWidgets.QApplication(sys.argv)

import qimage
import slides

widget = QtWidgets.QWidget()
grid = QtWidgets.QGridLayout()
grid.columnCount = 4

presentation_md_source = get_presentation_file_name()

if not presentation_md_source:
    sys.exit(0)

html_slides = slides.slides_from_html(slides.html_from_markdown(
    presentation_md_source))
qimages = map(qimage.from_html, html_slides)
pixmaps = map(lambda qimage: QtGui.QIcon(QtGui.QPixmap.fromImage(qimage)),
              qimages)



for i, pixmap in enumerate(pixmaps):
    button = QtWidgets.QPushButton()
    button.setIcon(pixmap)
    button.setIconSize(QtCore.QSize(200,200))
    button.setFlat(True)
    grid.addWidget(button, i / 4, i % 4)

widget.setLayout(grid)
scroll_area = QtWidgets.QScrollArea()
scroll_area.setWidget(widget)
widget.show()
scroll_area.show()

sys.exit(app.exec_())
