# -*- coding: utf-8 -*-

import sys
from os.path import expanduser

from PyQt5 import QtWidgets
from PyQt5 import QtCore


app = QtWidgets.QApplication(sys.argv)

import qimage
import slides
import gui

presentation_md_source = gui.get_presentation_md_source()

if not presentation_md_source:
    sys.exit(0)

html_slides = slides.slides_from_html(slides.html_from_markdown(
    presentation_md_source))
qimages = qimage.qimages_from_htmls(html_slides)
pixmaps = gui.pixmaps_from_qimages(qimages)

widget = QtWidgets.QWidget()
grid = gui.layout_for_list(pixmaps, widget)
widget.setLayout(grid)
scroll_area = QtWidgets.QScrollArea()
scroll_area.setWidget(widget)
widget.show()
scroll_area.show()

sys.exit(app.exec_())
