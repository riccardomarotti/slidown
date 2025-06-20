# -*- coding: utf-8 -*-

import sys
import os

from slidown import gui, config, file_utils


def main():
    """Main entry point for the slidown application."""
    # Force X11 mode for icon compatibility (works on both X11 and Wayland systems)
    import os
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    
    app = gui.create_qt_application(sys.argv)
    
    # Set desktop file name for proper system integration
    app.setDesktopFileName('slidown')

    # Global cleanup for any remaining subscriptions
    def cleanup_app():
        # Additional cleanup if needed
        pass

    app.aboutToQuit.connect(cleanup_app)

    configuration = config.load()

    if len(sys.argv) == 2:
        presentation_md_file = os.path.abspath(sys.argv[1])
    else:
        if 'last_presentation' in configuration and os.path.isfile(configuration['last_presentation']):
            presentation_md_file = configuration['last_presentation']
        else:
            presentation_md_file = gui.ask_for_presentation_file_name(os.path.expanduser('~'))

    if not presentation_md_file:
        sys.exit(0)

    presentation_md_file = file_utils.add_md_extension(presentation_md_file)
    file_utils.touch(presentation_md_file)

    configuration['last_presentation'] = presentation_md_file
    config.save(configuration)

    presentation_html_file = os.path.splitext(presentation_md_file)[0] + '.html'
    if os.path.isfile(presentation_html_file):
        os.remove(presentation_html_file)

    gui.generate_window(presentation_html_file,
                        presentation_md_file,
                        'Slidown: ' + os.path.basename(presentation_md_file))

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
