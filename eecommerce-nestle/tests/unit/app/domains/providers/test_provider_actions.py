import unittest
from unittest.mock import patch, MagicMock, Mock

from app.domains.category.models import Category
from app.domains.providers import ProviderDoNotExistException, ProviderInactiveException
from app.domains.providers.actions import create, get_by_id, get, update, delete, \
    populate_table_provider_category_association, get_categories_from_provider
from app.domains.providers.models import Provider


class TestProviderActions(unittest.TestCase):

    def setUp(self):
        self.data = dict(name='HBSIS',
                         cnpj='10414111215',
                         fantasy_name='HBSIS BLUMENAU',
                         phone1='984244178',
                         phone2='984244158',
                         phone3='854525224',
                         email='joao.raiser@hbsis.com.br',
                         address={'street': 'ABC',
                                  'neighborhood': 'Vila Nova',
                                  'zip': '89068060',
                                  'number': '1223',
                                  'city': 'Blumenau',
                                  'state': 'Santa Catarina',
                                  'complement': 'Empresa', })

    @patch('app.domains.providers.actions.save')
    @patch('app.domains.providers.actions.ValidateAddress')
    @patch('app.domains.providers.actions.create_address')
    @patch('app.domains.providers.actions.Provider')
    def test_action_create_should_be_created_new_provider(self, provider_mock, create_address_mock,
                                                          validate_address_mock, save_mock):
        provider_mock.return_value = MagicMock(id='1')
        # Actions
        create(self.data)

        # Assert
        provider_mock.assert_called_once()
        save_mock.assert_called_once()
        validate_address_mock.assert_called_once_with({
            'street': 'ABC',
            'neighborhood': 'Vila Nova',
            'zip': '89068060',
            'number': '1223',
            'city': 'Blumenau',
            'state': 'Santa Catarina',
            'complement': 'Empresa',
            'provider_id': '1'
        })
        calls_provider = provider_mock.call_args.kwargs
        create_address_mock.assert_called_once()
        self.assertEqual(calls_provider['name'], 'HBSIS')
        self.assertEqual(calls_provider['cnpj'], '10414111215')
        self.assertEqual(calls_provider['fantasy_name'], 'HBSIS BLUMENAU')
        self.assertEqual(calls_provider['phone1'], '984244178')
        self.assertEqual(calls_provider['phone2'], '984244158')
        self.assertEqual(calls_provider['phone3'], '854525224')
        self.assertEqual(calls_provider['email'], 'joao.raiser@hbsis.com.br')

    @patch('app.domains.providers.actions.Provider')
    def test_action_get_by_id_should_return_provider(self, provider_mock):
        # Arrange
        _id = '267354289'
        provider_mock.fantasy_name = 'HBSIS'
        provider_mock.email = 'hb@hb.com.br'
        query = Mock()
        query.get = MagicMock(return_value=provider_mock)
        provider_mock.query = query

        # Action
        provider = get_by_id(_id)

        # Assert
        provider_mock.query.get.assert_called_once_with(_id)
        self.assertEqual(provider_mock, provider)

    @patch('app.domains.providers.actions.Provider')
    def test_action_get_should_return_providers(self, provider_mock):
        # Arrange
        provider_mock.fantasy_name = 'HBSIS'
        provider_mock.email = 'hb@hb.com.br'
        query = Mock()
        query.filter_by().all = MagicMock(return_value=[provider_mock])
        provider_mock.query = query

        # Action
        providers = get({})

        # Assertions
        provider_mock.query.filter_by().all.assert_called_once()
        self.assertEqual(len(providers), 1)

    @patch('app.domains.providers.actions.Provider')
    @patch('app.domains.providers.actions.get_by_id')
    @patch('app.domains.providers.actions.commit')
    def test_action_update_should_update_provider(self, commit_mock, get_by_id_mock, provider_mock):
        # Arrange
        provider_mock.fantasy_name = 'HBSIS'
        provider_mock.email = 'hb@hb.com.br'
        get_by_id_mock.return_value = provider_mock

        # Action
        provider = update('id', {'fantasy_name': 'Ambev', 'email': 'joaorraiser@gmail.com'})

        # Assertions
        get_by_id_mock.assert_called_once_with('id')
        commit_mock.assert_called_once()
        self.assertEqual(provider.fantasy_name, 'Ambev')
        self.assertEqual(provider.email, 'joaorraiser@gmail.com')

    @patch('app.domains.providers.actions.commit')
    @patch('app.domains.providers.actions.get_by_id')
    def test_action_should_delete_provider(self, get_by_id_mock, commit_mock):
        # Arrange
        _id = '584356789'
        get_by_id_mock.return_value = MagicMock(is_active=True, deleted_at='15/01/2020')

        # Action
        delete(_id)

        # Assert
        commit_mock.assert_called_once()
        get_by_id_mock.assert_called_once_with(_id)

    @patch('app.domains.providers.actions.Provider')
    def test_should_raise_exception_when_try_to_get_by_id_an_inactive_provider(self, provider_mock):
        # Arrange
        query = Mock()
        query.get = MagicMock(return_value=None)
        provider_mock.query = query

        # Action
        with self.assertRaises(ProviderDoNotExistException) as ex:
            get_by_id('None')

        # Assert
        self.assertEqual(str(ex.exception.code), '404')
        self.assertEqual(str(ex.exception.description), 'Provider do not exist')

    @patch('app.domains.providers.actions.Provider')
    @patch('app.domains.providers.actions.get_by_id')
    def test_should_raise_exception_when_try_to_update_an_inactive_provider(self, get_by_id_mock,
                                                                            provider_mock):
        # Arrange
        get_by_id_mock.return_value = provider_mock
        provider_mock.is_active = False

        # Action
        with self.assertRaises(ProviderInactiveException) as ex:
            update('', {})

        # Assert
        get_by_id_mock.assert_called_once()
        self.assertEqual(str(ex.exception.code), '403')
        self.assertEqual(str(ex.exception.description), 'Unable to update an inactive provider')

    @patch("app.domains.providers.actions.save")
    @patch("app.domains.providers.actions.get_by_id")
    @patch("app.domains.providers.actions.get_category_by_id")
    def test_providers_and_categories_associations(self, get_category_by_id_mock, get_provider_by_id_mock, save_mock):
        # Arrange
        data = {
            "provider_id": "910766e9-959f-45f1-83c5-b2b0ca21e203",
            "category_id": "edbc25b9-d8dd-4a6f-a879-c55ac3f55908"
        }

        provider_mock = MagicMock(id="910766e9-959f-45f1-83c5-b2b0ca21e203")
        get_provider_by_id_mock.return_value = provider_mock

        category_mock = MagicMock(id="edbc25b9-d8dd-4a6f-a879-c55ac3f55908")
        category_mock.append = MagicMock()
        provider_mock.category = category_mock

        get_category_by_id_mock.return_value = category_mock
        save_mock.return_value = provider_mock

        # Action
        response = populate_table_provider_category_association(data)

        # Assert
        self.assertEqual(provider_mock, response)
        get_provider_by_id_mock.assert_called_once_with(data['provider_id'])
        get_category_by_id_mock.assert_called_once_with(data['category_id'])
        provider_mock.category.append.assert_called_once_with(get_category_by_id_mock(data['category_id']))
        save_mock.assert_called_once_with(provider_mock)

    @patch('app.domains.providers.actions.Provider')
    def test_get_categories_from_provider_by_association(self, provider_mock):
        # Arrange
        provider_id = "152d3621-2b5d-450a-b751-d58e74d0c296"
        laticinios_category_mock = MagicMock()
        laticinios_category_mock.serialize.return_value = {
            'id': '4d459ea0-7171-45b2-8f44-c551a7c33593',
            'name': 'Laticinios'
        }

        texteis_category_mock = MagicMock()
        texteis_category_mock.serialize.return_value = {
            'id': '21146ed1-c6cf-4dda-85a8-ec26337fce18',
            'name': 'Têxteis'
        }

        category_list = [laticinios_category_mock, texteis_category_mock]

        provider_categories_mock = MagicMock(category=category_list)
        provider_mock.query.get = MagicMock()
        provider_mock.query.get.return_value = provider_categories_mock


        # Action
        response = get_categories_from_provider(provider_id)

        # Assert
        self.assertIsInstance(response, list)
        self.assertEqual(response, [{'id': '4d459ea0-7171-45b2-8f44-c551a7c33593', 'name': 'Laticinios'},
 {'id': '21146ed1-c6cf-4dda-85a8-ec26337fce18', 'name': 'Têxteis'}])
        provider_mock.query.get.assert_called_once_with(provider_id)