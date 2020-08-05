from unittest.mock import Mock
import unittest
import pytest
from app.domains.providers.address import NullOrNoneValueException
from app.domains.providers.address.models import Address


class TestProvidersModelsAddress(unittest.TestCase):
    def test_providers_model_should_be_serialized(self):
        # Arrange
        mock_uuid = Mock()
        mock_uuid.uuid = 'uuid'

        # Action
        address = Address(id=mock_uuid, street='juca s/a',
                          zipcode='89374747', neighborhood='santa fé',
                          number='737', city='Blumenau',
                          state='SC', country='Brasil',
                          complement='7th floor',
                          )
        json = address.serialize()

        # Assert
        self.assertEqual(json['id'], mock_uuid)
        self.assertEqual(json['id'], mock_uuid)
        self.assertEqual(json['street'], 'juca s/a')
        self.assertEqual(json['zipcode'], '89374747')
        self.assertEqual(json['neighborhood'], 'santa fé')
        self.assertEqual(json['number'], '737')
        self.assertEqual(json['city'], 'Blumenau')
        self.assertEqual(json['state'], 'SC')
        self.assertEqual(json['country'], 'Brasil')
        self.assertEqual(json['complement'], '7th floor')

    def test_providers_model_address_raise_exception_if_name_is_none(self):
        # Action
        with pytest.raises(NullOrNoneValueException) as var:
            Address(street=None)
        # Assert
        self.assertEqual(str(var.value.description), 'value null or invalid')
        self.assertEqual(str(var.value.code), '400')

    def test_providers_model_address_raise_exception_if_name_is_empty(self):
        # Action
        with pytest.raises(NullOrNoneValueException) as var:
            Address(street='')
        # Assert
        self.assertEqual(str(var.value.description), 'value null or invalid')
        self.assertEqual(str(var.value.code), '400')

