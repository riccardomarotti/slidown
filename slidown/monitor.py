# -*- coding: utf-8 -*-

import os
import core

def on_file_changed(file_name, web_view, old_html, watcher, theme='white'):
    if os.path.isfile(file_name):
        new_presentation_html = core.generate_presentation_html(file_name, theme)
        if new_presentation_html == old_html:
            return

        number_of_slides = web_view.page().mainFrame().evaluateJavaScript(
            'Reveal.getTotalSlides();')
        web_view.loadFinished.connect(
            lambda: on_web_view_load(web_view,
                                     core.get_changed_slide(
                                         old_html,
                                         new_presentation_html)))
        web_view.setHtml(new_presentation_html)

        watcher.fileChanged.disconnect()
        watcher.fileChanged.connect(
            lambda file_name: on_file_changed(file_name,
                                              web_view,
                                              new_presentation_html,
                                              watcher,
                                              theme))



def on_directory_changed(directory_name, file_name_to_verify, watcher):
    if len(watcher.files()) == 0 and os.path.isfile(file_name_to_verify):
        watcher.addPath(file_name_to_verify)

def on_web_view_load(web_view, page_number):
    web_view.page().mainFrame().evaluateJavaScript(
        'Reveal.slide(' + str(page_number) + ');')
    web_view.loadFinished.disconnect()


def refresh_presentation(file_name, web_view, watcher, theme):
    html = core.generate_presentation_html(file_name, theme)
    web_view.setHtml(html)
    watcher.fileChanged.disconnect()
    watcher.fileChanged.connect(
            lambda file_name: on_file_changed(file_name,
                                              web_view,
                                              html,
                                              watcher,
                                              theme))
