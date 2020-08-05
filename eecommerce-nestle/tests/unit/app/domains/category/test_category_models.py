from unittest.mock import Mock
import unittest
import pytest
from app.domains.category import NullOrNoneValueException
from app.domains.category.models import Category


class TestCategoryModels(unittest.TestCase):
    def test_category_model_should_be_serialized(self):
        # Arrange
        mock_uuid = Mock()
        mock_uuid.uuid = 'uuid4'

        # Action
        category = Category(id=mock_uuid, name='Laticínios')
        json = category.serialize()

        # Assert
        self.assertEqual(json['id'], mock_uuid)
        self.assertEqual(json['name'], 'Laticínios')

    def test_category_model_raise_exception_if_name_is_none(self):
        # Action
        with pytest.raises(NullOrNoneValueException) as var:
            Category(name=None)
        # Assert
        self.assertEqual(str(var.value.description), 'The name is empty')
        self.assertEqual(str(var.value.code), '400')

    def test_category_model_raise_exception_if_name_is_empty(self):
        # Action
        with pytest.raises(NullOrNoneValueException) as var:
            Category(name='')
        # Assert
        self.assertEqual(str(var.value.description), 'The name is empty')
        self.assertEqual(str(var.value.code), '400')

