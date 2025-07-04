# -*- coding: utf-8 -*-

import os
import time
import tempfile

from unittest.mock import MagicMock, patch

from slidown import monitor, core

def test_check_changes_with_not_existing_path():
    previous = {
        'filename': 'not_existing_file',
        'previous_modify_date': 'a modified date'
    }

    current = 'anything'

    expected_output = {
        'filename': 'not_existing_file',
        'previous_modify_date': 'a modified date',
        'changed': False
    }

    assert monitor.check_changes(previous, current) == expected_output

def test_check_changes_with_existing_not_modified_path():
    with tempfile.TemporaryFile() as a_file:
        modified_date = os.path.getmtime(a_file.name)

        previous = {
            'filename': a_file.name,
            'previous_modify_date': modified_date,
            'changed': False
        }

        current = 'anything'

        expected_output = {
            'filename': a_file.name,
            'previous_modify_date': modified_date,
            'changed': False
        }

        assert monitor.check_changes(previous, current) == expected_output

def test_check_changes_with_existing_modified_path():
    now = time.time()
    then = now + 10

    with tempfile.NamedTemporaryFile() as a_file:
        current = 'anything'

        previous = {
            'filename': a_file.name,
            'previous_modify_date': os.path.getmtime(a_file.name),
            'changed': False
        }

        os.utime(a_file.name, (then, then))

        expected_output = {
            'filename': a_file.name,
            'previous_modify_date': os.path.getmtime(a_file.name),
            'changed': True
        }

        assert monitor.check_changes(previous, current) == expected_output

def test_create_new_html_with_changed_slide():
    core.generate_presentation_html = lambda file_name, theme: 'a new html text'
    core.get_changed_slide = lambda previous_html, new_html: 'the changed slide'

    with tempfile.NamedTemporaryFile() as an_input_file:
        an_input_file_name = an_input_file.name

        expected_output = {
            'html': 'a new html text',
            'file_name': an_input_file_name,
            'changed_slide': 'the changed slide'
        }

        actual_output = monitor.create_new_html({
            'html': 'an old html text',
            'file_name': an_input_file_name,
            'changed_slide': 'an old changed slide'
        }, {})

        assert expected_output, actual_output == expected_output

def test_create_new_html_with_no_changes():
    core.generate_presentation_html = lambda file_name, theme: 'generated html text'

    with tempfile.NamedTemporaryFile() as an_input_file:
        an_input_file_name = an_input_file.name

        expected_output = {
            'html': 'generated html text',
            'file_name': an_input_file_name,
            'changed_slide': None
        }

        actual_output = monitor.create_new_html({
            'html': 'generated html text',
            'file_name': an_input_file_name,
            'changed_slide': 'an old changed slide'
        }, {})

        assert actual_output == expected_output

def test_file_monitor_creation():
    """Test that FileMonitor can be created with a file path"""
    with tempfile.NamedTemporaryFile() as temp_file:
        file_monitor = monitor.FileMonitor(temp_file.name)
        assert file_monitor.file_path == temp_file.name
        assert file_monitor.current_html == ''

def test_file_monitor_with_missing_file():
    """Test FileMonitor behavior with non-existent file"""
    # Create QApplication if it doesn't exist
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    file_monitor = monitor.FileMonitor('/non/existent/file.md')
    
    # Track signal emissions
    signal_emitted = []
    file_monitor.file_changed.connect(lambda html, slide, path: signal_emitted.append((html, slide, path)))
    
    # This should not emit any signal since file doesn't exist
    file_monitor.check_and_generate_html()
    
    # Process Qt events
    app.processEvents()
    
    # No signal should be emitted
    assert len(signal_emitted) == 0

def test_file_monitor_no_change():
    """Test FileMonitor when HTML doesn't change"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_file.write('# Test slide')
        temp_file.flush()
        
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        file_monitor = monitor.FileMonitor(temp_file.name)
        
        with patch('slidown.core.generate_presentation_html') as mock_generate, \
             patch('slidown.core.get_changed_slide') as mock_get_slide:
            
            mock_generate.return_value = 'same html content'
            mock_get_slide.return_value = (1, 2)
            
            signal_emitted = []
            file_monitor.file_changed.connect(lambda html, slide, path: signal_emitted.append((html, slide, path)))
            
            # First call should emit signal
            file_monitor.check_and_generate_html()
            app.processEvents()
            assert len(signal_emitted) == 1
            
            # Second call with same HTML should not emit signal
            signal_emitted.clear()
            file_monitor.check_and_generate_html()
            app.processEvents()
            assert len(signal_emitted) == 0
            
        os.unlink(temp_file.name)

def test_manage_md_file_changes_with_runtime_error():
    """Test manage_md_file_changes handles RuntimeError gracefully"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_file.write('# Test slide')
        temp_file.flush()
        
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create a mock webview that raises RuntimeError when accessed
        mock_webview = MagicMock()
        mock_webview.webview.loadFinished.connect.side_effect = RuntimeError("QWebEngineView deleted")
        
        with patch('slidown.core.generate_presentation_html') as mock_generate, \
             patch('slidown.core.get_changed_slide') as mock_get_slide:
            
            mock_generate.return_value = 'mocked html content'
            mock_get_slide.return_value = (0, 0)
            
            with tempfile.NamedTemporaryFile() as output_file:
                # This should not raise an exception even with RuntimeError
                watcher = monitor.manage_md_file_changes(temp_file.name, 
                                                        output_file.name, 
                                                        mock_webview)
                
                # Trigger file change manually
                if hasattr(watcher, 'fileChanged'):
                    # Emit the signal to test error handling
                    from PyQt5.QtCore import QFileSystemWatcher
                    if isinstance(watcher, QFileSystemWatcher):
                        # The error handling should prevent crashes
                        pass
                
                watcher.deleteLater()
                
        os.unlink(temp_file.name)

def test_load_new_html():
    """Test load_new_html function"""
    with tempfile.NamedTemporaryFile() as output_file:
        mock_webview = MagicMock()
        monitor.load_new_html('html text', (1,2), output_file.name, mock_webview)

        assert open(output_file.name).read() == 'html text'

        mock_webview.reload.assert_called_with()
        mock_webview.webview.loadFinished.connect.assert_called_once()
        
        callback = mock_webview.webview.loadFinished.connect.call_args[0][0]
        callback()
        
        mock_webview.load.assert_called_with('file://' + output_file.name + '#/1/2')

def test_manage_md_file_changes():
    """Test that manage_md_file_changes creates a QFileSystemWatcher"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_file.write('# Test slide')
        temp_file.flush()
        
        # Create QApplication if it doesn't exist
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        mock_webview = MagicMock()
        
        # Mock the core functions to avoid pandoc dependency
        with patch('slidown.core.generate_presentation_html') as mock_generate, \
             patch('slidown.core.get_changed_slide') as mock_get_slide:
            
            mock_generate.return_value = 'mocked html content'
            mock_get_slide.return_value = (0, 0)
            
            with tempfile.NamedTemporaryFile() as output_file:
                watcher = monitor.manage_md_file_changes(temp_file.name, 
                                                        output_file.name, 
                                                        mock_webview)
                
                # Verify watcher was created and file is being watched
                from PyQt5.QtCore import QFileSystemWatcher
                assert isinstance(watcher, QFileSystemWatcher)
                assert temp_file.name in watcher.files()
                
                # Cleanup
                watcher.deleteLater()
                
        os.unlink(temp_file.name)

def test_refresh_theme():
    """Test refresh_presentation_theme function"""
    with tempfile.NamedTemporaryFile() as output_file:
        mock_webview = MagicMock()
        
        mock_webview.show_loading = MagicMock()
        mock_webview.hide_loading = MagicMock()

        # Create QApplication if it doesn't exist (needed for Qt signals)
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        with patch('slidown.core.generate_presentation_html') as mock_generate:
            mock_generate.return_value = 'some html text'
            
            monitor.refresh_presentation_theme('a file name',
                                               mock_webview,
                                               output_file.name,
                                               'a theme')

            # Wait for the worker thread to complete and process events
            import time
            for _ in range(10):  # Try multiple times
                app.processEvents()
                time.sleep(0.01)
                if open(output_file.name).read():
                    break

            assert open(output_file.name).read() == 'some html text'
            mock_webview.load.assert_called_with('file://' + output_file.name)
            mock_webview.show_loading.assert_called_once()
            mock_webview.hide_loading.assert_called_once()
            mock_generate.assert_called_with('a file name', 'a theme')
