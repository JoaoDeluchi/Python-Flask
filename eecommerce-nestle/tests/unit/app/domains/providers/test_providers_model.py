import unittest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.domains.providers import NullOrNoneValueException
from app.domains.providers.models import Provider


class TestProvidersModels(unittest.TestCase):

    def test_providers_model_should_be_serialized(self):
        # Arrange
        mock_uuid = Mock()
        mock_uuid.uuid = 'uuid'
        address_mock = MagicMock()
        address_mock.serialize = MagicMock(return_value={'street': 'Barata', 'zipcode': '11111-111', 'neighborhood': 'nenhuma',
                                    'state': 'SC', 'number': '123', 'city': 'Blumenau', 'country': 'Brazil',
                                    'id':'123'})

        # Action
        provider = Provider(id=mock_uuid, name='juca s/a',
                            fantasy_name='josé ltda', email='jose@yahoo.com',
                            cnpj='61215281000194', phone1='413782738273',
                            phone2='479898374958', phone3='479828393748',
                            address=address_mock
                            )
        json = provider.serialize()

        # Assert
        self.assertEqual(json['id'], mock_uuid)
        self.assertEqual(json['name'], 'juca s/a')
        self.assertEqual(json['fantasy_name'], 'josé ltda')
        self.assertEqual(json['email'], 'jose@yahoo.com')
        self.assertEqual(json['cnpj'], '61215281000194')
        self.assertEqual(json['phone1'], '413782738273')
        self.assertEqual(json['phone2'], '479898374958')
        self.assertEqual(json['phone3'], '479828393748')
        self.assertEqual(json['address'], {'street': 'Barata', 'zipcode': '11111-111', 'neighborhood': 'nenhuma',
                                    'state': 'SC', 'number': '123', 'city': 'Blumenau', 'country': 'Brazil',
                                    'id':'123'})

    def test_providers_model_should_be_minimum_serialize(self):
        # Arrange
        mock_uuid = Mock()
        mock_uuid.uuid = 'uuid'
        date = datetime.now()

        # Action
        provider = Provider(id=mock_uuid, name='juca s/a',
                            fantasy_name='josé ltda', email='jose@yahoo.com',
                            cnpj='61215281000194', phone1='413782738273',
                            phone2='479898374958', phone3='479828393748',
                            updated_at=date, created_at=date)

        json = provider.minimum_serialize()

        # Assert
        self.assertEqual(json['id'], mock_uuid)
        self.assertEqual(json['fantasy_name'], 'josé ltda')
        self.assertEqual(json['created_at'], date)
        self.assertEqual(json['updated_at'], date)

    def test_providers_model_raise_exception_if_name_is_none(self):
        # Action
        with pytest.raises(NullOrNoneValueException) as var:
            Provider(name=None)
        # Assert
        self.assertEqual(str(var.value.description), 'the field name is empty')
        self.assertEqual(str(var.value.code), '400')

    def test_providers_model_raise_exception_if_name_is_empty(self):
        # Action
        with pytest.raises(NullOrNoneValueException) as var:
            Provider(name='')
        # Assert
        self.assertEqual(str(var.value.description), 'the field name is empty')
        self.assertEqual(str(var.value.code), '400')

