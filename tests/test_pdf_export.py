# -*- coding: utf-8 -*-

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from slidown.gui import export_to_pdf


def test_pdf_export_filters_speaker_notes():
    """Unit test that verifies speaker notes filtering logic"""
    # Create a temporary markdown file with speaker notes
    md_content = """# Test Presentation

## Slide 1
This is the first slide.

::: {.notes}
These are speaker notes that should NOT appear in the PDF export.
:::

## Slide 2
This is the second slide.

::: {.notes}
More speaker notes to be filtered.
:::

## Slide 3
Final slide without notes.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        md_file_path = f.name
    
    try:
        # Mock the file dialog to return a PDF path
        pdf_path = md_file_path.replace('.md', '.pdf')
        
        # Mock QFileDialog
        with patch('slidown.gui.QtWidgets.QFileDialog') as mock_dialog_class:
            mock_dialog = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            mock_dialog.exec.return_value = 1  # QFileDialog.Accepted
            mock_dialog.selectedFiles.return_value = [pdf_path]
            mock_dialog_class.AcceptSave = 1
            mock_dialog_class.Accepted = 1
            
            # Mock QMessageBox to avoid GUI
            with patch('slidown.gui.QtWidgets.QMessageBox'):
                
                # Mock pypandoc.convert_text to capture the filtered content
                with patch('slidown.gui.pypandoc.convert_text') as mock_convert:
                    export_to_pdf(md_file_path)
                    
                    # Verify pypandoc was called
                    assert mock_convert.called
                    
                    # Get the filtered content that was passed to pypandoc
                    call_args = mock_convert.call_args
                    filtered_content = call_args[0][0]  # First positional argument
                    
                    # Verify speaker notes were removed
                    assert '::: {.notes}' not in filtered_content
                    assert 'These are speaker notes' not in filtered_content
                    assert 'More speaker notes' not in filtered_content
                    
                    # Verify slide content is preserved
                    assert '# Test Presentation' in filtered_content
                    assert '## Slide 1' in filtered_content
                    assert 'This is the first slide.' in filtered_content
                    assert '## Slide 2' in filtered_content
                    assert 'This is the second slide.' in filtered_content
                    assert '## Slide 3' in filtered_content
                    assert 'Final slide without notes.' in filtered_content
                    
                    # Verify correct arguments passed to pypandoc
                    assert call_args[0][1] == 'pdf'  # output format
                    assert call_args[1]['format'] == 'md'  # input format
                    assert call_args[1]['outputfile'] == pdf_path
                    assert '--pdf-engine=wkhtmltopdf' in call_args[1]['extra_args']
                    assert '--slide-level=2' in call_args[1]['extra_args']
    
    finally:
        # Clean up
        if os.path.exists(md_file_path):
            os.unlink(md_file_path)


def test_pdf_export_handles_pandoc_error():
    """Test that PDF export handles pypandoc errors gracefully"""
    md_content = "# Simple Test\n\n## Slide 1\nContent"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        md_file_path = f.name
    
    try:
        pdf_path = md_file_path.replace('.md', '.pdf')
        
        # Mock QFileDialog
        with patch('slidown.gui.QtWidgets.QFileDialog') as mock_dialog_class:
            mock_dialog = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            mock_dialog.exec.return_value = 1  # QFileDialog.Accepted
            mock_dialog.selectedFiles.return_value = [pdf_path]
            mock_dialog_class.AcceptSave = 1
            mock_dialog_class.Accepted = 1
            
            # Mock pypandoc to raise an exception
            with patch('slidown.gui.pypandoc.convert_text') as mock_convert:
                mock_convert.side_effect = Exception("Pandoc error")
                
                # Mock QMessageBox to capture error dialog
                with patch('slidown.gui.QtWidgets.QMessageBox') as mock_msgbox_class:
                    mock_msgbox = MagicMock()
                    mock_msgbox_class.return_value = mock_msgbox
                    
                    export_to_pdf(md_file_path)
                    
                    # Verify error dialog was shown
                    assert mock_msgbox_class.called
                    mock_msgbox.setIcon.assert_called()
                    mock_msgbox.setWindowTitle.assert_called_with("Export Error")
                    mock_msgbox.setText.assert_called()
                    mock_msgbox.exec.assert_called()
    
    finally:
        # Clean up
        if os.path.exists(md_file_path):
            os.unlink(md_file_path)


def test_pdf_export_dialog_cancelled():
    """Test that PDF export handles dialog cancellation"""
    md_content = "# Simple Test\n\n## Slide 1\nContent"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        md_file_path = f.name
    
    try:
        # Mock QFileDialog to return cancelled
        with patch('slidown.gui.QtWidgets.QFileDialog') as mock_dialog_class:
            mock_dialog = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            mock_dialog.exec.return_value = 0  # QFileDialog.Rejected
            
            # Mock pypandoc - should not be called
            with patch('slidown.gui.pypandoc.convert_text') as mock_convert:
                export_to_pdf(md_file_path)
                
                # Verify pypandoc was NOT called
                assert not mock_convert.called
    
    finally:
        # Clean up
        if os.path.exists(md_file_path):
            os.unlink(md_file_path)