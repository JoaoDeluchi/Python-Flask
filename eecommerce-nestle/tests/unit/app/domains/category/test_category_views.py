import io
from unittest.mock import patch, MagicMock, Mock

from app.domains.category import ErrorCategory
from tests.unit import AbstractViewUnitTest


class TestCategoryViews(AbstractViewUnitTest):

    @patch('app.domains.category.views.get_category')
    def test_get_category_should_be_1(self, get_category_mock):
        # Arrange
        category = Mock()
        category.serialize = MagicMock(return_value={})
        get_category_mock.return_value = [category]

        # Action
        response = self._client.get('/categories')
        data = response.get_json()

        self.assertEqual(len(data), 1)
        get_category_mock.assert_called_once()

    @patch('app.domains.category.views.get_category_by_id')
    def test_get_category_by_id_should_be_1(self, get_category_by_id_mock):
        # Arrange
        _id = 'gre7679bf'
        category = Mock()
        category.serialize = MagicMock(return_value={})
        get_category_by_id_mock.return_value = category

        # Action
        response = self._client.get('/categories/{}'.format(_id))

        # Assert
        self.assertEqual(response.status_code, 200)
        get_category_by_id_mock.assert_called_once_with(_id)

    @patch('app.domains.category.views.create_category')
    def test_post_category_should_be_created(self, create_category_mock):
        # Arrange
        category = Mock()
        category.serialize = MagicMock(return_value={})
        create_category_mock.return_value = category

        # Action
        response = self._client.post('/categories', json={})

        # Assert
        self.assertEqual(response.status_code, 201)
        create_category_mock.assert_called_once_with({})

    @patch('app.domains.category.views.update_category')
    def test_put_category_should_be_updated(self, update_category_mock):
        _id = '97546984'
        category = Mock()
        category.serialize = MagicMock(return_value={})
        update_category_mock.return_value = category

        # Action
        response = self._client.put('/categories/{}'.format(_id), json={
            'name': 'Chocolates',
        })

        # Assertions
        self.assertEqual(response.status_code, 200)
        update_category_mock.assert_called_once_with(_id, {
            'name': 'Chocolates',
        })

    @patch('app.domains.category.views.delete_category')
    def test_delete_should_delete_category(self, delete_mock):
        # Arrange
        _id = '34589t749'

        # Action
        response = self._client.delete('/categories/{}'.format(_id))

        # Assert
        self.assertEqual(response.status_code, 204)
        delete_mock.assert_called_once_with(_id)
        delete_mock.assert_called_once()

    @patch('app.domains.category.views.upload_file')
    def test_import_category_excel_sheet_should_import(self, upload_file_mock):
        # Arrange
        payload = {'name': 'premium'}
        obj = Mock()
        obj.serialize = MagicMock(return_value=payload)
        upload_file_mock.return_value = [obj]

        data = {'name': 'this is a name'}
        data = {key: str(value) for key, value in data.items()}
        data['file'] = (io.BytesIO(bytes(1)), 'test.xlsx')
        # Act
        response = self._client.post(
            '/categories:import', data=data, follow_redirects=True,
            content_type='multipart/form-data'
        )
        # Assert
        self.assertEqual(201, response.status_code)
        upload_file_mock.assert_called_once()

    @patch('app.domains.category.views.upload_file')
    def test_import_category_excel_sheet_should_return_Error_message(self, upload_file_mock):
        # Arrange
        upload_file_mock.return_value = [ErrorCategory('premium')]

        data = {'name': 'this is a name'}
        data = {key: str(value) for key, value in data.items()}
        data['file'] = (io.BytesIO(bytes(1)), 'test.xlsx')
        # Act
        response = self._client.post(
            '/categories:import', data=data, follow_redirects=True,
            content_type='multipart/form-data'
        )
        # Assert
        self.assertEqual(201, response.status_code)
        upload_file_mock.assert_called_once()

    @patch('app.domains.category.views.send_file')
    @patch('app.domains.category.views.export_file')
    def test_export_category_excel_sheet_should_export(self, export_mock, send_type_mock):
        export_mock.return_value = {}
        # Arrange
        send_type_mock.return_value = MagicMock({})
        # Act
        response = self._client.get('/categories:batchGet')
        # Assert
        self.assertEqual(200, response.status_code)
        export_mock.assert_called_once()
        send_type_mock.assert_called_once()
        send_type_mock.assert_called_once_with(export_mock(),
                                               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                               True)

    @patch('app.domains.category.views.get_association')
    def test_view_should_show_providers_associated_in_categories(self, get_association_mock):
        # Arrange
        return_list = [
            {"id": "f4b7994e-cb00-48a2-8a14-1653add51305", "name": "textil"},
            {"id": "046a17b5-8e67-4d7a-b987-afdd66faf5a4", "name": "manufaturados"},
            {"id": "f9f96f88-08e6-4428-a85b-502624a7e3fc", "name": "laticínios"}
        ]
        get_association_mock.return_value = return_list
        category_id = "68ecef70-e64b-4ac6-aa84-cac145915df5"

        # Action
        response = self._client.get(f'/categories/providers/{category_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), return_list)
        get_association_mock.assert_called_once_with(category_id)