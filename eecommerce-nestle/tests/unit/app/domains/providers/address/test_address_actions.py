import unittest
from unittest.mock import patch, MagicMock, Mock
from app.domains.providers.address.actions import get_by_id, update, create, get, delete


class TestAddressActions(unittest.TestCase):
    @patch('app.domains.providers.address.actions.Address')
    @patch('app.domains.providers.address.actions.save')
    def test_action_create_should_be_created_new_address(self, save_mock, address_mock):
        # Arrange
        address_mock.street = 'Street'
        address_mock.number = '123'

        # Action
        save_mock.return_value = address_mock
        create({'street': 'Street', 'number': '123'})

        # Assert
        save_mock.assert_called_once_with(address_mock())
        self.assertEqual(address_mock.street, 'Street')
        self.assertEqual(address_mock.number, '123')
        self.assertEqual(save_mock.call_count, 1)

    @patch('app.domains.providers.address.actions.Address')
    def test_action_get_by_id_should_be_return_an_address(self, address_mock):
        # Arrange
        _id = '378423084'
        address_mock.street = 'Street'
        address_mock.number = '123'
        query = Mock()
        query.get = MagicMock(return_value=address_mock)
        address_mock.query = query

        # Action
        address_mock()
        address = get_by_id(_id)

        # Assert
        address_mock.query.get.assert_called_once_with(_id)
        self.assertEqual(address_mock, address)
        self.assertEqual(address_mock.call_count, 1)

    @patch('app.domains.providers.address.actions.Address')
    def test_action_get_should_be_return_address(self, address_mock):
        # Arrange
        address_mock.id = '245897502735'
        address_mock.street = 'Street'
        address_mock.number = '123'
        address_mock.query.get.return_value = address_mock

        # Action
        address = address_mock.query.all
        get_address = get()
        address_mock()

        # Assert
        self.assertEqual(get_address, address())
        self.assertEqual(address_mock.call_count, 1)

    @patch('app.domains.providers.address.actions.Address')
    @patch('app.domains.providers.address.actions.get_by_id')
    @patch('app.domains.providers.address.actions.commit')
    def test_action_update_should_be_updated_address(self, commit_mock, get_by_id_mock, address_mock):
        # Arrange
        id = '245897502735'
        address_saved = address_mock()
        address_saved.street = 'Street'
        address_saved.number = '123'
        get_by_id_mock.return_value = address_saved

        # Action
        address = update(id, {'street': 'rua dos bobos', 'number': '0'})

        # Assert
        get_by_id_mock.assert_called_once_with(id)
        commit_mock.assert_called_once()
        self.assertEqual(address.street, 'rua dos bobos')
        self.assertEqual(address.number, '0')
        self.assertEqual(address_mock.call_count, 1)

    @patch('app.domains.providers.address.actions.Address')
    @patch('app.domains.providers.address.actions.get_by_id')
    @patch('app.domains.providers.address.actions.commit')
    def test_action_delete_address_column_is_active_should_be_false(self, commit_mock, get_by_id_mock, address_mock):
        # Arrange
        _id = '025739-68294'
        address_mock.is_active = True
        get_by_id_mock.return_value = address_mock
        get_by_id_mock.return_value = address_mock

        # Action
        delete(_id)
        address_mock()

        # Assert
        commit_mock.assert_called_once()
        get_by_id_mock.assert_called_once_with(_id)
        self.assertEqual(address_mock.is_active, False)
        self.assertEqual(address_mock.call_count, 1)
