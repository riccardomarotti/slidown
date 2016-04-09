# -*- coding: utf-8 -*-

from slidown import core

import os

import rx
from rx import Observable
from rx.concurrency import QtScheduler

current_theme = 'white'

def check_changes(previous, cur):
    current_modify_date = previous['previous_modify_date']
    filename = previous['filename']

    if os.path.isfile(filename):
        current_modify_date = os.path.getmtime(filename)

    return {
        'previous_modify_date': current_modify_date,
        'changed': previous['previous_modify_date'] != current_modify_date,
        'filename': filename
    }


def create_new_html(previous, cur):
    previous_html = previous['html']
    file_name = previous['file_name']
    new_html = core.generate_presentation_html(file_name,
                                               theme=current_theme)

    if new_html != previous_html:
        changed_slide = core.get_changed_slide(previous_html, new_html)
    else:
        changed_slide = None

    return {'file_name': file_name,
            'html': new_html,
            'changed_slide': changed_slide}

def create_new_html_on_md_file_changes_observable(file_name):
    from PyQt5 import QtCore
    return Observable.interval(100, scheduler=QtScheduler(QtCore)).scan(
        check_changes,
        seed={'previous_modify_date': -1,
              'changed': False,
              'filename': file_name}).filter(
                  lambda val: val['changed']).scan(
                      create_new_html,
                      seed={'file_name': file_name,
                            'html': '',
                            'changed_slide': (0,0)}).filter(
                                lambda val: val['changed_slide'] != None)

def load_new_html(html, changed_slide, output_file_name, web_view):
    from PyQt5 import QtCore
    open(output_file_name, 'w').write(html)

    slide_url = 'file://' + output_file_name + '#/' + "/".join(map(str,
                                                                   changed_slide))

    web_view.load(
        QtCore.QUrl(slide_url))
    web_view.reload()

def manage_md_file_changes(presentation_md_file,
                           presentation_html_file,
                           web_view):
    create_new_html_on_md_file_changes_observable(
        presentation_md_file).subscribe(
            lambda values: load_new_html(
                values['html'],
                values['changed_slide'],
                presentation_html_file,
                web_view
            )
        )

def refresh_presentation_theme(file_name, web_view, output_file_name, theme):
    from PyQt5 import QtCore
    html = core.generate_presentation_html(file_name, theme)
    open(output_file_name, 'w').write(html)
    web_view.load(QtCore.QUrl('file://' + output_file_name))
    global current_theme
    current_theme = theme
