import unittest
import pytest
from unittest.mock import MagicMock
from app.domains.products import NullValueException
from app.domains.products.models import Product


class TestProductModels(unittest.TestCase):
    def test_products_should_be_serialized(self):
        # Arrange
        product = Product(id='1827169419',
                           name='name',
                           cost_values='cost_values',
                           unit_per_box='123',
                           weight_per_unit='weight_per_unit',
                           shelf_life='shelf_life',
                           sku='sku',
                           description='description'
                           )

        # Action
        json = product.serialize()

        # Assert
        self.assertEqual(json['id'], '1827169419')
        self.assertEqual(json['name'], 'name')
        self.assertEqual(json['cost_values'], 'cost_values')
        self.assertEqual(json['unit_per_box'], 123)
        self.assertEqual(json['weight_per_unit'], 'weight_per_unit')
        self.assertEqual(json['shelf_life'], 'shelf_life')
        self.assertEqual(json['sku'], 'sku')
        self.assertEqual(json['description'], 'description')

    def test_products_should_not_be_serialized_because_no_have_value(self):
        # Arrange

        # Action
        with pytest.raises(NullValueException) as exception:
            Product(id='1827169419',
                     name='name',
                     cost_values='',
                     unit_per_box='unit_per_box',
                     weight_per_unit='weight_per_unit',
                     shelf_life='shelf_life',
                     sku='sku',
                     description='description'
                     )

        # Assert
        self.assertEqual(exception.value.description, 'The field cost_values can not be null')
        self.assertEqual(exception.value.code, 400)

    def test_products_should_not_be_serialized_because_value_is_none(self):
        # Arrange

        # Action
        with pytest.raises(NullValueException) as exception:
            Product(id='1827169419',
                     name='name',
                     cost_values=None,
                     unit_per_box='unit_per_box',
                     weight_per_unit='weight_per_unit',
                     shelf_life='shelf_life',
                     sku='sku',
                     description='description'
                     )

        # Assert
        self.assertEqual(exception.value.description, 'The field cost_values can not be null')
        self.assertEqual(exception.value.code, 400)
