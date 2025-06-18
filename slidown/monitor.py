# -*- coding: utf-8 -*-

from slidown import core

import os

from PyQt5.QtCore import QThread, pyqtSignal, QFileSystemWatcher

current_theme = 'white'
_active_workers = []  # Keep references to prevent garbage collection
_active_watcher = None  # Global file watcher to ensure only one is active

class ThemeChangeWorker(QThread):
    html_generated = pyqtSignal(str)
    
    def __init__(self, file_name, theme):
        super().__init__()
        self.file_name = file_name
        self.theme = theme
    
    def run(self):
        html = core.generate_presentation_html(self.file_name, self.theme)
        self.html_generated.emit(html)

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

class FileMonitor(QThread):
    file_changed = pyqtSignal(str, object, str)  # html, changed_slide, file_path
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.current_html = ''
        
    def check_and_generate_html(self):
        if os.path.isfile(self.file_path):
            new_html = core.generate_presentation_html(self.file_path, theme=current_theme)
            
            if new_html != self.current_html:
                changed_slide = core.get_changed_slide(self.current_html, new_html)
                self.current_html = new_html
                
                if changed_slide is not None:
                    self.file_changed.emit(new_html, changed_slide, self.file_path)

def load_new_html(html, changed_slide, output_file_name, web_view):
    open(output_file_name, 'w').write(html)

    slide_url = 'file://' + output_file_name + '#/' + "/".join(map(str,
                                                                   changed_slide))

    def navigate_after_reload():
        web_view.load(slide_url)
        # Disconnect after use to prevent accumulation
        web_view.webview.loadFinished.disconnect(navigate_after_reload)
    
    web_view.webview.loadFinished.connect(navigate_after_reload)
    web_view.reload()

def manage_md_file_changes(presentation_md_file,
                           presentation_html_file,
                           web_view,
                           scheduler=None):
    global _active_watcher, _active_workers
    
    # Stop previous watcher if exists
    if _active_watcher:
        _active_watcher.deleteLater()
    
    # Clear previous workers
    for worker in _active_workers:
        worker.quit()
        worker.wait()
        worker.deleteLater()
    _active_workers.clear()
    
    # Create file system watcher
    _active_watcher = QFileSystemWatcher()
    _active_watcher.addPath(presentation_md_file)
    
    # Create file monitor
    file_monitor = FileMonitor(presentation_md_file)
    _active_workers.append(file_monitor)
    
    def on_file_changed(file_path):
        file_monitor.check_and_generate_html()
    
    def on_html_generated(html, changed_slide, file_path):
        # Check if web_view still exists before using it
        try:
            if web_view and hasattr(web_view, 'webview'):
                load_new_html(html, changed_slide, presentation_html_file, web_view)
        except RuntimeError:
            # QWebEngineView has been deleted, ignore
            pass
    
    _active_watcher.fileChanged.connect(on_file_changed)
    file_monitor.file_changed.connect(on_html_generated)
    
    # Generate initial HTML
    file_monitor.check_and_generate_html()
    
    return _active_watcher

def refresh_presentation_theme(file_name, web_view, output_file_name, theme):
    global current_theme, _active_workers
    current_theme = theme
    
    if hasattr(web_view, 'show_loading'):
        web_view.show_loading()
    
    worker = ThemeChangeWorker(file_name, theme)
    _active_workers.append(worker)
    
    def on_html_generated(html):
        open(output_file_name, 'w').write(html)
        web_view.load(('file://' + output_file_name))
        
        if hasattr(web_view, 'hide_loading'):
            web_view.hide_loading()
        
        _active_workers.remove(worker)
        worker.quit()
        worker.deleteLater()
    
    worker.html_generated.connect(on_html_generated)
    worker.start()
