# -*- coding: utf-8 -*-

import sys
import os

import core
import gui
import config


app = gui.create_qt_application(sys.argv)

configuration = config.get()

if len(sys.argv) == 2:
    presentation_md_file = os.path.abspath(sys.argv[1])
else:
    if not 'last_presentation' in configuration:
        presentation_md_file = gui.get_presentation_file_name(os.path.expanduser('~'))
    else:
        presentation_md_file = configuration['last_presentation']

if not presentation_md_file:
    sys.exit(0)

configuration['last_presentation'] = presentation_md_file
config.save(configuration)

presentation_html = core.generate_presentation_html(presentation_md_file)
presentation_html_file = os.path.splitext(presentation_md_file)[0] + '.html'
open(presentation_html_file, 'w').write(presentation_html)

gui.generate_window(presentation_html_file,
                    presentation_md_file,
                    presentation_html,
                    'Slidown: ' + os.path.basename(presentation_md_file))

sys.exit(app.exec_())
