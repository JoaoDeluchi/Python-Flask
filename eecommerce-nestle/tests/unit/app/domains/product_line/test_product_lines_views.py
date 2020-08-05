from tests.unit import AbstractViewUnitTest
from unittest.mock import patch, MagicMock, Mock


class TestUsersViews(AbstractViewUnitTest):

    @patch('app.domains.product_line.views.get_product_line')
    def test_get_product_line_should_be_1(self, get_product_line_mock):
        # Arrange
        product_line = Mock()
        product_line.serialize = MagicMock(return_value={})
        get_product_line_mock.return_value = [product_line]

        # Action
        response = self._client.get('/product_lines')
        data = response.get_json()

        # Assert
        self.assertEqual(len(data), 1)
        self.assertEqual(response.status_code, 200)
        get_product_line_mock.assert_called_once()

    @patch('app.domains.product_line.views.get_product_line_by_id')
    def test_get_product_line_by_id_should_be_1(self, get_by_id_mock):
        # Arrange
        product_line = Mock()
        product_line.serialize = MagicMock(return_value={})
        get_by_id_mock.return_value = product_line
        _id = '3567993'

        # Action
        response = self._client.get('/product_lines/{}'.format(_id))

        # Assert
        self.assertEqual(response.status_code, 200)
        get_by_id_mock.assert_called_once_with(_id)

    @patch('app.domains.product_line.views.create_product_line')
    def test_post_product_line_should_be_created(self, create_product_line_mock):
        # Arrange
        product_line = Mock()
        product_line.serialize = MagicMock(return_value={})
        create_product_line_mock.return_value = product_line

        # Action
        response = self._client.post('/product_lines', json={
            'name': 'AAAA',
            'category': 'category',
        })

        # Assert
        self.assertEqual(response.status_code, 201)
        create_product_line_mock.assert_called_once_with({
            'name': 'AAAA',
            'category': 'category',
        })

    @patch('app.domains.product_line.views.update_product_line')
    def test_put_product_line_should_be_updated(self, update_mock):
        # Arrange
        _id = '94568734'
        obj = Mock()
        obj.serialize = MagicMock(return_value={})

        # Action
        update_mock.return_value = obj
        response = self._client.put('/product_lines/{}'.format(_id), json={
            'name': 'BBBB',
        })

        # Assert
        self.assertEqual(response.status_code, 200)
        update_mock.assert_called_once_with(_id, {
            'name': 'BBBB',
        })

    @patch('app.domains.product_line.views.delete_product_line')
    def test_delete_product_line_should_be_deleted(self, delete_mock):
        # Arrange
        _id = '489563'
        delete_mock.return_value = _id

        # Action
        response = self._client.delete('/product_lines/{}'.format(_id))

        # Assert
        self.assertEqual(response.status_code, 204)
        delete_mock.assert_called_once_with(_id)