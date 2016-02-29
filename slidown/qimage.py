# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5 import QtWebKitWidgets

def from_html(html, webkit=QtWebKitWidgets.QWebView(), painter=QtGui.QPainter()):
    webkit.setHtml(html)
    page = webkit.page()
    frame = page.mainFrame()
    image = QtGui.QImage(frame.contentsSize(), QtGui.QImage.Format_ARGB32)
    painter.begin(image)
    frame.render(painter)
    painter.end()

    return image
