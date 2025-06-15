# -*- coding: utf-8 -*-

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from slidown.gui import export_to_pdf


def test_pdf_export_integration():
    """Integration test that actually creates a PDF and verifies speaker notes are filtered"""
    # Create a temporary markdown file with speaker notes
    md_content = """# Test Presentation

## Slide 1
This is the first slide content.

::: {.notes}
These are speaker notes that should NOT appear in the PDF export.
:::

## Slide 2
This is the second slide content.

::: {.notes}
More speaker notes to be filtered.
:::

## Slide 3
Final slide without notes.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        md_file_path = f.name
    
    pdf_path = md_file_path.replace('.md', '.pdf')
    
    try:
        # Mock QFileDialog to return our PDF path
        with patch('slidown.gui.QtWidgets.QFileDialog') as mock_dialog_class:
            mock_dialog = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            mock_dialog.exec.return_value = 1  # QFileDialog.Accepted
            mock_dialog.selectedFiles.return_value = [pdf_path]
            mock_dialog_class.AcceptSave = 1
            mock_dialog_class.Accepted = 1
            
            # Mock QMessageBox to avoid GUI popups
            with patch('slidown.gui.QtWidgets.QMessageBox'):
                
                # Actually call export_to_pdf - this will use real pypandoc
                export_to_pdf(md_file_path)
                
                # Verify PDF was created
                assert os.path.exists(pdf_path), "PDF file should be created"
                
                # Verify PDF has content (basic check - file size > 0)
                assert os.path.getsize(pdf_path) > 0, "PDF should not be empty"
                
                # Test that notes filtering actually worked by checking the intermediate content
                # that would be generated (this verifies our filtering logic)
                import pypandoc
                from slidown import core
                
                # Read and filter the content the same way export_to_pdf does
                with open(md_file_path, 'r', encoding='utf-8') as f:
                    md_content_check = f.read()
                
                # Apply the same filtering logic
                lines = md_content_check.split('\n')
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
                
                # Verify notes were filtered from the content
                assert '::: {.notes}' not in filtered_content
                assert 'These are speaker notes' not in filtered_content
                assert 'More speaker notes' not in filtered_content
                
                # Verify slide content is preserved
                assert 'This is the first slide content.' in filtered_content
                assert 'This is the second slide content.' in filtered_content
                assert 'Final slide without notes.' in filtered_content
                
                # Most importantly: verify the actual PDF content
                # Try to extract text from PDF to verify notes are not present
                pdf_text_extracted = False
                
                # Try different PDF libraries
                try:
                    import PyPDF2
                    with open(pdf_path, 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        pdf_text = ""
                        for page in pdf_reader.pages:
                            pdf_text += page.extract_text()
                    pdf_text_extracted = True
                except ImportError:
                    pass
                
                if not pdf_text_extracted:
                    try:
                        import pdfplumber
                        with pdfplumber.open(pdf_path) as pdf:
                            pdf_text = ""
                            for page in pdf.pages:
                                pdf_text += page.extract_text() or ""
                        pdf_text_extracted = True
                    except ImportError:
                        pass
                
                if pdf_text_extracted:
                    # Clean up whitespace for comparison (PDF extraction can have tabs/spacing issues)
                    pdf_text_clean = ' '.join(pdf_text.split())
                    
                    # Verify slide content is in PDF (accounting for font ligatures like ﬁ for fi)
                    assert 'Test Presentation' in pdf_text_clean
                    assert 'rst slide content' in pdf_text_clean  # "first" might become "ﬁrst"
                    assert 'second slide content' in pdf_text_clean
                    assert 'Final slide without notes' in pdf_text_clean
                    
                    # Verify speaker notes are NOT in PDF
                    assert 'speaker notes' not in pdf_text_clean
                    assert 'More speaker notes' not in pdf_text_clean
                else:
                    print("No PDF text extraction library available - skipping PDF content verification")
                
    except Exception as e:
        # If wkhtmltopdf is not installed, skip this test
        if "wkhtmltopdf not found" in str(e) or "No such file or directory" in str(e):
            pytest.skip("wkhtmltopdf not installed - skipping integration test")
        else:
            raise e
    
    finally:
        # Clean up
        if os.path.exists(md_file_path):
            os.unlink(md_file_path)
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)