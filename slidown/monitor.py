# -*- coding: utf-8 -*-

import os
import core
import rx
from rx import Observable
from rx.concurrency import QtScheduler
from PyQt5 import QtCore

current_theme = 'white'

def check_changes(previous, cur):
    current_modify_date = -1
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
    new_html = core.generate_presentation_html(previous['file_name'], theme=current_theme)

    if new_html != previous_html:
        changed_slide = core.get_changed_slide(previous_html, new_html)
    else:
        changed_slide = None

    return {'file_name': previous['file_name'],
            'output_file_name': previous['output_file_name'],
            'html': new_html,
            'changed_slide': changed_slide,
            'web_view': previous['web_view']}


def file_changed_observable(file_name, output_file_name, web_view):
    return Observable.interval(100, scheduler=QtScheduler(QtCore)).scan(
        check_changes,
        seed={'previous_modify_date': -1,
              'changed': False,
              'filename': file_name}).filter(
                  lambda val: val['changed']).scan(
                      create_new_html,
                      seed={'file_name': file_name,
                            'output_file_name': output_file_name,
                            'html': '',
                            'changed_slide': (0,0),
                            'web_view': web_view}).filter(
                                lambda val: val['changed_slide'] != None)

def load_new_html(values):
    html = values['html']
    changed_slide = values['changed_slide']
    output_file_name = values['output_file_name']
    web_view = values['web_view']
    open(output_file_name, 'w').write(html)

    web_view.load(
        QtCore.QUrl(
            'file://' + output_file_name + '#/' + "".join(map(str,
                                                              changed_slide))))
    web_view.reload()

def manage_md_file_changes(presentation_md_file,
                           presentation_html_file,
                           web_view):
    file_changed_observable(presentation_md_file,
                            presentation_html_file,
                            web_view).subscribe(load_new_html)

def refresh_presentation_theme(file_name, web_view, output_file_name, theme):
    html = core.generate_presentation_html(file_name, theme)
    open(output_file_name, 'w').write(html)
    web_view.load(QtCore.QUrl('file://' + output_file_name))
    global current_theme
    current_theme = theme
