# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWebKitWidgets

import pypandoc


app = QtWidgets.QApplication(sys.argv)

presentation_md_file = QtWidgets.QFileDialog.getOpenFileName(None,
                                                             'Open presentation',
                                                             os.path.expanduser('~'))[0]

if not presentation_md_file:
    sys.exit(0)

reveal_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'reveal.js')

reveal_html = pypandoc.convert(presentation_md_file,
                               'revealjs',
                               extra_args=['-V', 'revealjs-url:' + reveal_js_path,
                                           '--self-contained',
                                           '-V', 'theme:white'])

main_widget = QtWebKitWidgets.QWebView()
main_widget.setHtml(reveal_html)

main_widget.loadFinished.connect(lambda: main_widget.page().mainFrame().evaluateJavaScript('Reveal.toggleOverview();'))
main_widget.loadFinished.connect(lambda: main_widget.show())

sys.exit(app.exec_())
