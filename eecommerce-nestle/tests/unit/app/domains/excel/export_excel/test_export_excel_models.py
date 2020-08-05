import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from app.domains.excel.export_excel.models import ExportExcel
from app.exceptions import BadRequestException


class TestExportExcelModels(unittest.TestCase):

    def setUp(self) -> None:
        self._test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self._test_dir)

    @patch.object(tempfile,'mkdtemp')
    def test_save_table_sheet_with_3_parameters(self,mock_temp_dir):
        #Arrange
        mock_temp_dir.return_value = self._test_dir
        excel = ExportExcel('new_file')
        #act
        result = excel.save_table_sheet(2,2,2*2)
        #Assert
        mock_temp_dir.assert_called_once()
        self.assertEqual(result, os.path.join(self._test_dir,'new_file.xlsx'))

    @patch.object(tempfile,'mkdtemp')
    @patch('app.domains.excel.export_excel.models.Workbook.save')
    def test_save_table_sheet_with_2_parameters_check_file_name(self, mock_save,mock_temp_dir):
        #Arrange
        mock_temp_dir.return_value = self._test_dir
        excel = ExportExcel('new_file')
        #Act
        result = excel.save_table_sheet('A2',97)
        #Assert
        self.assertTrue(result)
        self.assertEqual(result, os.path.join(mock_temp_dir.return_value,'new_file.xlsx'))
        mock_save.assert_called_once_with((os.path.join(self._test_dir, 'new_file.xlsx')))

    def test_save_should_fail_save_table_sheet(self):

        with self.assertRaises(BadRequestException) as ex:
            excel = ExportExcel('new_file')
            excel.save_table_sheet()

        self.assertEqual(str(ex.exception.description), 'Bad Request Exception')
        self.assertEqual(str(ex.exception.code), '400')

    def test_save_should_fail_on_init(self):

        with self.assertRaises(BadRequestException) as ex:
            excel = ExportExcel('')
            excel.save_table_sheet(2,2,2*2)

        self.assertEqual(str(ex.exception.description), 'Bad Request Exception')
        self.assertEqual(str(ex.exception.code), '400')
