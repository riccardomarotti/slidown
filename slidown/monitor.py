# -*- coding: utf-8 -*-

import os
import core
from PyQt5 import QtCore

def create_filesystem_watcher(presentation_md_file):
    presentation_file_watcher = QtCore.QFileSystemWatcher(
    [presentation_md_file,
     os.path.dirname(presentation_md_file)])

    presentation_file_watcher.fileChanged.connect(
        lambda file_name: monitor.on_file_changed(file_name, web_view,
                                                  presentation_html,
                                                  presentation_file_watcher,
                                                  presentation_html_file))


    presentation_file_watcher.directoryChanged.connect(
        lambda directory_name: monitor.on_directory_changed(
            directory_name, presentation_md_file, presentation_file_watcher))

    return presentation_file_watcher

def on_file_changed(file_name, web_view, old_html, watcher, output_file_name, theme='white'):
    if os.path.isfile(file_name):
        new_presentation_html = core.generate_presentation_html(file_name, theme)
        if new_presentation_html == old_html:
            return

        web_view.loadFinished.connect(
            lambda: on_web_view_load(web_view,
                                     core.get_changed_slide(
                                         old_html,
                                         new_presentation_html)))
        web_view.load(QtCore.QUrl('file://' + output_file_name))

        watcher.fileChanged.disconnect()
        watcher.fileChanged.connect(
            lambda file_name: on_file_changed(file_name,
                                              web_view,
                                              new_presentation_html,
                                              watcher,
                                              output_file_name,
                                              theme))

        open(output_file_name, 'w').write(new_presentation_html)



def on_directory_changed(directory_name, file_name_to_verify, watcher):
    if len(watcher.files()) == 0 and os.path.isfile(file_name_to_verify):
        watcher.addPath(file_name_to_verify)

def on_web_view_load(web_view, page_number):
    web_view.page().mainFrame().evaluateJavaScript(
        'Reveal.slide' + str(page_number) + ';')
    web_view.loadFinished.disconnect()


def refresh_presentation(file_name, web_view, watcher, output_file_name, theme):
    html = core.generate_presentation_html(file_name, theme)
    open(output_file_name, 'w').write(html)
    web_view.load(QtCore.QUrl('file://' + output_file_name))
    watcher.fileChanged.disconnect()
    watcher.fileChanged.connect(
            lambda file_name: on_file_changed(file_name,
                                              web_view,
                                              html,
                                              watcher,
                                              output_file_name,
                                              theme))
