# -*- coding: utf-8 -*-

import os
import core

def on_file_changed(file_name, web_views, old_html, watcher):
    if os.path.isfile(file_name):
        new_presentation_html = core.generate_presentation_html(file_name)
        if new_presentation_html == old_html:
            return

        for web_view in web_views:
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
                                              web_views,
                                              new_presentation_html,
                                              watcher))

def on_directory_changed(directory_name, file_name_to_verify, watcher):
    if len(watcher.files()) == 0 and os.path.isfile(file_name_to_verify):
        watcher.addPath(file_name_to_verify)

def on_web_view_load(web_view, page_number):
    web_view.page().mainFrame().evaluateJavaScript(
        'Reveal.slide(' + str(page_number) + ');')
    web_view.loadFinished.disconnect()
