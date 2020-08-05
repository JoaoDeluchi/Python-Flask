import flask

import io

from flask import request, Flask
from werkzeug.local import LocalProxy

from tests.unit import AbstractViewUnitTest
from unittest.mock import patch, MagicMock, Mock


class TestProductViews(AbstractViewUnitTest):
    @patch('app.domains.products.views.create_product')
    def test_post_product_should_be_created(self, create_product_mock):
        # Arrange
        product = Mock()
        product.serialize = MagicMock(return_value={})
        create_product_mock.return_value = product

        # Act
        response = self._client.post('/products')

        # Assert
        self.assertEqual(response.status_code, 201)
        create_product_mock.assert_called_once()

    @patch('app.domains.products.views.update_product')
    def test_put_product_should_be_updated(self, update_product_mock):
        # Arrange
        _id = '59863450'
        product = Mock()
        product.serialize = MagicMock(return_value={})
        update_product_mock.return_value = product

        # Act
        response = self._client.put('/products/{}'.format(_id), json={
            'name': 'Korona',
        })

        # Assert
        self.assertEqual(response.status_code, 200)
        update_product_mock.assert_called_once_with(_id, {
            'name': 'Korona'
        })

    @patch('app.domains.products.views.get_product')
    def test_get_should_get_all_available_products(self, get_product_mock):
        # Arrange
        product = Mock()
        product.serialize = MagicMock(return_value={})
        get_product_mock.return_value = [product]

        # Act
        response = self._client.get('/products')
        data = response.get_json()

        # Assert
        self.assertEqual(len(data), 1)
        self.assertEqual(response.status_code, 200)
        get_product_mock.assert_called_once()

    @patch('app.domains.products.views.get_product_by_id')
    def test_get_by_id_should_get_products_by_their_id(self, get_by_id_mock):
        # Arrange
        _id = '9057849'
        product = Mock()
        product.serialize = MagicMock(return_value={})
        get_by_id_mock.return_value = product

        # Act
        response = self._client.get('/products/{}'.format(_id))

        # Assert
        self.assertEqual(response.status_code, 200)
        get_by_id_mock.assert_called_once_with(_id)

    @patch('app.domains.products.views.delete_product')
    def test_delete_should_delete_product(self, delete_mock):
        # Arrange
        _id = '40563905630'

        # Act
        response = self._client.delete('/products/{}'.format(_id))

        # Assert
        self.assertEqual(response.status_code, 204)
        delete_mock.assert_called_once_with(_id)

    @patch('app.domains.products.views.send_file')
    @patch('app.domains.products.views.export_product')
    def test_export_product_excel_sheet_should_export(self, export_mock, send_type_mock):
        export_mock.return_value = {}
        # Arrange
        send_type_mock.return_value = MagicMock({})
        # Act
        response = self._client.get('/products:batchGet')
        # Assert
        self.assertEqual(200, response.status_code)
        export_mock.assert_called_once()
        send_type_mock.assert_called_once()
        send_type_mock.assert_called_once_with(export_mock(),
                                               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                               True)

    @patch('app.domains.products.views.upload_product')
    def test_upload_excel_should_be_imported_xlsx(self, upload_file_mock):
        payload = {'name': 'premium'}
        obj = Mock()
        obj.serialize = MagicMock(return_value=payload)
        upload_file_mock.return_value = [obj]
        upload_file_mock.serialize.return_value = [obj]
        data = {'name': 'this is a name'}
        data = {key: str(value) for key, value in data.items()}
        data['file'] = (io.BytesIO(bytes(1)), 'test.xlsx')
        response = self._client.post(
            '/products:import', data=data, follow_redirects=True,
            content_type='multipart/form-data'
        )
        self.assertEqual(201, response.status_code)
        upload_file_mock.assert_called_once()
