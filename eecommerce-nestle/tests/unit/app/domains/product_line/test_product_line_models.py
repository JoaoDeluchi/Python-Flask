import unittest

import pytest


from app.domains.product_line import NullValueException
from app.domains.product_line.models import ProductLine


class TestProductLineModels(unittest.TestCase):

    def test_product_line_model_should_be_serialized(self):
        # Arrange
        product_line = ProductLine(id='123', name='Mucilon Arroz', id_category='45325864')

        # Actions
        json = product_line.serialize()

        # Assert
        self.assertEqual(json['name'], 'Mucilon Arroz')
        self.assertEqual(json['id_category'], '45325864')

    def test_product_line_model_exception_because_name_null(self):
        # Arrange
        # Action
        with pytest.raises(NullValueException) as ex:
            ProductLine(id='123', name='', id_category='896479')

        # Assert
        self.assertEqual(str(ex.value.description), 'The field name cannot be null!')
        self.assertEqual(ex.value.code, 400)

    def test_product_line_model_exception_because_category_id_null(self):
        # Arrange
        # Action
        with pytest.raises(NullValueException) as ex:
            ProductLine(id='123', name='Mucilon', id_category='')

        # Assert
        self.assertEqual(str(ex.value.description), 'The field id_category cannot be null!')
        self.assertEqual(ex.value.code, 400)
