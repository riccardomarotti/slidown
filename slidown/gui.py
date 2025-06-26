# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

# No longer using RxPY - using Qt's QFileSystemWatcher for event-driven file monitoring

from slidown import monitor, file_utils, config, core
import os
import pypandoc
import subprocess


def create_qt_application(argv):
    app = QtWidgets.QApplication(argv)
    
    # Set application properties for better Linux compatibility
    app.setApplicationName("Slidown")
    app.setApplicationDisplayName("Slidown")
    app.setOrganizationName("Slidown")
    app.setApplicationVersion("1.0")
    
    # Set application icon at startup with absolute path
    import sys
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'icon', 'slidown.png')
    else:
        # Use absolute path for icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'icon', 'slidown.png')
    
    if os.path.exists(icon_path):
        from PyQt5.QtGui import QIcon
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)  # Application level icon
    
    return app

def export_to_pdf(presentation_md_file):
    """Export presentation to PDF without speaker notes"""
    dialog = QtWidgets.QFileDialog()
    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
    dialog.setNameFilter("PDF files (*.pdf)")
    dialog.setDefaultSuffix("pdf")
    
    # Set default filename based on markdown file
    base_name = os.path.splitext(os.path.basename(presentation_md_file))[0]
    dialog.selectFile(f"{base_name}.pdf")
    
    if dialog.exec() == QtWidgets.QFileDialog.Accepted:
        pdf_path = dialog.selectedFiles()[0]
        
        try:
            # Read markdown content
            with open(presentation_md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Remove speaker notes (lines starting with ::: {.notes})
            lines = md_content.split('\n')
            filtered_lines = []
            in_notes = False
            
            for line in lines:
                if line.strip().startswith('::: {.notes}'):
                    in_notes = True
                    continue
                elif line.strip() == ':::' and in_notes:
                    in_notes = False
                    continue
                elif not in_notes:
                    filtered_lines.append(line)
            
            filtered_content = '\n'.join(filtered_lines)
            
            # Setup pandoc for pyinstaller (same as in core.py)
            core.setup_pandoc_for_pyinstaller()
            
            # Convert to PDF using pandoc with wkhtmltopdf
            pypandoc.convert_text(
                filtered_content,
                'pdf',
                format='md',
                outputfile=pdf_path,
                extra_args=['--pdf-engine=wkhtmltopdf', '--slide-level=2']
            )
            
            # Open PDF automatically
            QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))
            
        except Exception as e:
            # Show error message
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle("Export Error")
            msg.setText(f"Failed to export PDF:\n{str(e)}")
            msg.exec()

def generate_window(presentation_html_file,
                    presentation_md_file,
                    window_title):

    layout = QtWidgets.QVBoxLayout()
    web_view = QtWebEngineWidgets.QWebEngineView()
    
    stacked_widget = QtWidgets.QStackedWidget()
    
    loading_widget = QtWidgets.QWidget()
    loading_layout = QtWidgets.QVBoxLayout(loading_widget)
    loading_layout.addStretch()
    
    spinner_label = QtWidgets.QLabel()
    spinner_label.setAlignment(QtCore.Qt.AlignCenter)
    spinner_label.setStyleSheet("font-size: 24px; color: #333;")
    
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    spinner_timer = QtCore.QTimer()
    spinner_index = [0]
    
    def update_spinner():
        spinner_label.setText(spinner_chars[spinner_index[0]])
        spinner_index[0] = (spinner_index[0] + 1) % len(spinner_chars)
    
    spinner_timer.timeout.connect(update_spinner)
    spinner_timer.start(100)
    update_spinner()
    
    loading_layout.addWidget(spinner_label)
    
    loading_label = QtWidgets.QLabel("Generating presentation...")
    loading_label.setAlignment(QtCore.Qt.AlignCenter)
    loading_label.setStyleSheet("font-size: 18px; color: #666; margin-top: 10px;")
    loading_layout.addWidget(loading_label)
    
    loading_layout.addStretch()
    
    stacked_widget.addWidget(loading_widget)  # Index 0
    stacked_widget.addWidget(web_view)        # Index 1
    
    stacked_widget.setCurrentIndex(0)
    
    wrapped_web_view = WebViewWrapper(web_view, stacked_widget, spinner_timer)
    
    def on_load_finished():
        wrapped_web_view.hide_loading()
    
    web_view.loadFinished.connect(on_load_finished)
    
    wrapped_web_view.load('file://' + presentation_html_file)
    
    layout.addWidget(stacked_widget)
    main_widget = QtWidgets.QWidget()
    main_widget.setLayout(layout)
    
    # Store watcher reference for cleanup
    main_widget._watcher = None

    mode_checkbox = QtWidgets.QCheckBox()
    mode_checkbox.setText('Edit mode')
    mode_checkbox.stateChanged.connect(lambda state: mode_change(state,
                                                                 main_widget))

    open_editor_button = QtWidgets.QPushButton(text='Editor')
    open_editor_button.clicked.connect(lambda evt: QDesktopServices.openUrl(QUrl.fromLocalFile(presentation_md_file)))

    open_editor_browser = QtWidgets.QPushButton(text='Browser')
    open_editor_browser.clicked.connect(lambda evt: QDesktopServices.openUrl(QUrl('file://' + presentation_html_file)))

    export_pdf_button = QtWidgets.QPushButton(text='Export PDF')
    export_pdf_button.clicked.connect(lambda evt: export_to_pdf(presentation_md_file))

    lower_window_layout = QtWidgets.QHBoxLayout()
    lower_window_layout.addWidget(mode_checkbox)
    lower_window_layout.addWidget(open_editor_button)
    lower_window_layout.addWidget(open_editor_browser)
    lower_window_layout.addWidget(export_pdf_button)


    themes = ['White', 'Black', 'League', 'Beige', 'Sky',
              'Night', 'Serif', 'Simple', 'Solarized']
    themes_combo = QtWidgets.QComboBox()
    themes_combo.addItems(themes)
    
    # Load saved theme BEFORE starting file monitoring
    saved_theme = config.get_presentation_theme(presentation_md_file)
    saved_theme_capitalized = saved_theme.capitalize()
    if saved_theme_capitalized in themes:
        themes_combo.setCurrentText(saved_theme_capitalized)
        monitor.current_theme = saved_theme

    # Store the file watcher for proper cleanup - start AFTER theme is set
    main_widget._watcher = monitor.manage_md_file_changes(presentation_md_file,
                                                          presentation_html_file,
                                                          wrapped_web_view)
    
    def on_theme_changed(index):
        selected_theme = themes[index].lower()
        config.save_presentation_theme(presentation_md_file, selected_theme)
        monitor.refresh_presentation_theme(
            presentation_md_file,
            wrapped_web_view,
            presentation_html_file,
            selected_theme)
    
    themes_combo.activated.connect(on_theme_changed)
    lower_window_layout.addWidget(themes_combo)

    group = QtWidgets.QGroupBox()
    group.setLayout(lower_window_layout)


    layout.addWidget(group)

    main_widget.setWindowTitle(window_title)
    
    # Set window icon (will work in X11 mode)
    import sys
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'icon', 'slidown.png')
    else:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'icon', 'slidown.png')
    
    if os.path.exists(icon_path):
        from PyQt5.QtGui import QIcon
        icon = QIcon(icon_path)
        main_widget.setWindowIcon(icon)
    
    # Add cleanup when widget closes
    def cleanup_on_close(event):
        if main_widget._watcher:
            main_widget._watcher.deleteLater()
        event.accept()
    
    main_widget.closeEvent = cleanup_on_close
    main_widget.show()


def ask_for_presentation_file_name(start_dir):
    dialog = QtWidgets.QFileDialog(parent=None,
                                  caption='Open presentation',
                                  directory=start_dir,
                                  filter='Markdown files (*.md)',
                                  options=QtWidgets.QFileDialog.DontConfirmOverwrite)

    dialog.setLabelText(QtWidgets.QFileDialog.Accept, 'Open')
    file_name = None
    if dialog.exec():
        file_name = dialog.selectedFiles()[0]

    return file_name

def full_screen_change(mode, main_widget):
    {QtCore.Qt.Checked: main_widget.showFullScreen,
     QtCore.Qt.Unchecked: main_widget.showNormal}[mode]()

def mode_change(edit_checkbox_state, widget):
    function = {QtCore.Qt.Checked: set_edit_mode,
                QtCore.Qt.Unchecked: unset_edit_mode} [edit_checkbox_state]
    function(widget)

def unset_edit_mode(widget):
    widget.setWindowOpacity(1)

    geometry = widget.geometry()

    window_flags = QtCore.Qt.Window & ~(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    widget.setWindowFlags(window_flags)

    widget.setGeometry(geometry)
    widget.show()

def set_edit_mode(widget):
    widget.setWindowOpacity(0.8)

    geometry = widget.geometry()

    window_flags = widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
    widget.setWindowFlags(window_flags)

    widget.setGeometry(geometry)
    widget.show()


class WebViewWrapper():
    def __init__(self, webview, stacked_widget=None, spinner_timer=None):
        self.webview = webview
        self.stacked_widget = stacked_widget
        self.spinner_timer = spinner_timer

    def load(self, url):
        self.webview.load(QtCore.QUrl(url))

    def reload(self):
        self.webview.reload()
        
    def show_loading(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(0)
            if self.spinner_timer:
                self.spinner_timer.start()
            
    def hide_loading(self):
        if self.stacked_widget:
            self.stacked_widget.setCurrentIndex(1)
            if self.spinner_timer:
                self.spinner_timer.stop()
