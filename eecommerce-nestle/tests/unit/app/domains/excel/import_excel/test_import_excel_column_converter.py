import pytest
import unittest
from app.domains.excel.import_excel.excel_column_converter import convert_column
class TestImportExcelColumnConverter(unittest.TestCase):

    def test_cell_by_position_should_be_True(self):
        #Arrange

        #Action
        cellA = convert_column(1)
        cellL = convert_column(12)
        cellZ = convert_column(26)
        cellAT = convert_column(46)

        #Assert
        self.assertEqual(cellA,'A')
        self.assertEqual(cellL,'L')
        self.assertEqual(cellZ,'Z')
        self.assertEqual(cellAT,'AT')

