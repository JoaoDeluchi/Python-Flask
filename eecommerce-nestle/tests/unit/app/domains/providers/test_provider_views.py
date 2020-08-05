from app.domains.providers.models import Provider
from tests.unit import AbstractViewUnitTest
from unittest.mock import patch, MagicMock, Mock


class TestProvidersViews(AbstractViewUnitTest):
    @patch('app.domains.providers.views.create_provider')
    def test_post_provider_should_be_created(self, create_provider_mock):
        # Arrange
        payload = {
            'name': 'name',
            'id': 'id'
        }
        provider = Mock()

        # Action
        provider.serialize = MagicMock(return_value={})
        create_provider_mock.return_value = provider
        response = self._client.post('/providers', json=payload)

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {})
        create_provider_mock.assert_called_once_with({
            'name': 'name',
            'id': 'id'
        })

    @patch('app.domains.providers.views.update_provider')
    def test_put_provider_should_be_updated(self, update_provider_mock):
        # Arrange
        id = '1'
        obj = Mock()

        # Action
        obj.serialize = MagicMock(return_value={'name': 'name'})
        update_provider_mock.return_value = obj
        response = self._client.put('/providers/{}'.format(id), json={
            'name': 'new_name',
        })

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'name': 'name'})
        update_provider_mock.assert_called_once_with('1', {
            'name': 'new_name'
        })

    @patch('app.domains.providers.views.get_provider')
    def test_get_providers_should_get_only_one_time(self, get_provider_mock):
        # Arrange
        obj = Mock()
        obj.minimum_serialize = MagicMock(return_value={})
        get_provider_mock.return_value = [obj]
        response = self._client.get('/providers')

        # Action
        data = response.get_json()

        # Assert
        get_provider_mock.assert_called_once()
        self.assertEqual(len(data), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{}])

    @patch('app.domains.providers.views.get_provider_by_id')
    def test_get_providers_by_id_should_be_one(self, get_user_by_id_mock):
        # Arrange
        obj = Mock()

        # Action
        obj.serialize = MagicMock(return_value={})
        get_user_by_id_mock.return_value = obj
        id = '1'
        response = self._client.get('/providers/{}'.format(id))

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})
        get_user_by_id_mock.assert_called_once_with(id)

    @patch('app.domains.providers.views.delete_provider')
    def test_delete_providers_should_be_deleted(self, mock_delete_provider):
        # Arrange
        mock_id = MagicMock(return_value='832197')

        # Action
        response = self._client.delete('/providers/{}'.format(mock_id))

        # Assert
        self.assertEqual(response.status_code, 204)
        mock_delete_provider.assert_called_once()

    @patch('app.domains.providers.views.create_association')
    def test_view_should_populate_provider_and_category_association_table(self, create_association_mock):
        # Arrange
        Provider = Mock()
        provider = Provider
        provider.serialize = MagicMock(return_value={})
        payload = {
            "provider_id": "910766e9-959f-45f1-83c5-b2b0ca21e203",
            "category_id": "edbc25b9-d8dd-4a6f-a879-c55ac3f55908"
        }
        create_association_mock.return_value = provider

        # Action
        response = self._client.post('/providers/categories', json=payload)

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {})
        create_association_mock.assert_called_once_with(payload)

    @patch('app.domains.providers.views.get_association')
    def test_view_should_show_categories_associated_in_providers(self, get_association_mock):
        # Arrange
        return_list = [
            {"id": "f4b7994e-cb00-48a2-8a14-1653add51305", "name": "textil"},
            {"id": "046a17b5-8e67-4d7a-b987-afdd66faf5a4", "name": "manufaturados"},
            {"id": "f9f96f88-08e6-4428-a85b-502624a7e3fc", "name": "laticínios"}
        ]

        get_association_mock.return_value = return_list
        provider_id = "68ecef70-e64b-4ac6-aa84-cac145915df5"

        # Action
        response = self._client.get(f'/providers/categories/{provider_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), return_list)
        get_association_mock.assert_called_once_with(provider_id)