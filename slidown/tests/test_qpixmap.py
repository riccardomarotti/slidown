# -*- coding: utf-8 -*-

import unittest
import unittest.mock

from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])

from .. import qimage


class QImageTest(unittest.TestCase):

    def test_image_from_html(self):
        mock_webkit = unittest.mock.Mock(name='webkit')
        mock_painter = unittest.mock.Mock(name='painter')
        mock_page = unittest.mock.Mock(name='page')
        mock_frame = unittest.mock.Mock(name='frame')

        mock_webkit.page.return_value = mock_page
        mock_page.mainFrame.return_value = mock_frame
        mock_frame.contentsSize.return_value = 'a content size'

        with unittest.mock.patch('PyQt5.QtGui.QImage') as mock_qimage:
            actual_image_result = qimage.from_html('<h1> A Title </h1>',
                                                   mock_webkit,
                                                   mock_painter)

            mock_webkit.setHtml.assert_called_with('<h1> A Title </h1>')
            mock_painter.begin.assert_called_with(mock_qimage.return_value)
            mock_frame.render.assert_called_with(mock_painter)
            mock_painter.end.assert_called_with()

            self.assertEqual(mock_qimage.return_value, actual_image_result)






if __name__ == "__main__":
    unittest.main()
