from tests.unit import AbstractViewUnitTest
from unittest.mock import patch, MagicMock, Mock


class TestUsersViews(AbstractViewUnitTest):
    @patch('app.domains.users.views.get_users')
    def test_get_users_should_be_1(self, get_user_mock):
        # Arrange
        obj = Mock()
        obj.serialize = MagicMock(return_value={})
        get_user_mock.return_value = [obj]

        # Action
        response = self._client.get('/users')
        data = response.get_json()

        # Assertions
        self.assertEqual(len(data), 1)
        get_user_mock.assert_called_once()

    @patch('app.domains.users.views.get_user_by_id')
    def test_get_user_by_id_should_be_1(self, get_user_by_id_mock):
        # Arrange
        obj = Mock()
        obj.serialize = MagicMock(return_value={})
        get_user_by_id_mock.return_value = obj
        id = '69875340'

        # Action
        response = self._client.get('/users/{}'.format(id))
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        get_user_by_id_mock.assert_called_once_with(id)

    @patch('app.domains.users.views.create_user')
    def test_post_user_should_be_created(self, create_user_mock):
        # Arrange
        payload = {
            'name': 'Lucas',
            'email': 'LucasPedrito@hbsis.com.br',
        }
        obj = Mock()
        obj.serialize = MagicMock(return_value={})
        create_user_mock.return_value = obj

        # Action
        response = self._client.post('/users', json=payload)

        # Assertions
        self.assertEqual(response.status_code, 201)
        create_user_mock.assert_called_once_with({
            'name': 'Lucas',
            'email': 'LucasPedrito@hbsis.com.br',
        })

    @patch('app.domains.users.views.update_user')
    def test_put_user_should_be_updated(self, update_user_mock):
        # Arrange
        _id = '78546375'
        obj = Mock()
        obj.serialize = MagicMock(return_value={'name': 'Lucas', 'email': 'robertinha123@hbsis.com.br'})
        update_user_mock.return_value = obj

        # Action
        response = self._client.put('/users/{}'.format(_id), json={
            'name': 'Robertinha',
            'email': 'robertinha123@hbsis.com.br',
        })

        # Assertions
        self.assertEqual(response.status_code, 200)
        update_user_mock.assert_called_once_with('78546375', {
            'name': 'Robertinha',
            'email': 'robertinha123@hbsis.com.br',
        })

    @patch('app.domains.users.views.delete_users')
    def test_delete_should_delete_user(self, delete_mock):
        # Arrange
        id_mock = MagicMock(return_value='8567756')

        # Act
        response = self._client.delete('/users/{}'.format(id_mock))

        # Assert
        self.assertEqual(response.status_code, 204)
        delete_mock.assert_called_once()