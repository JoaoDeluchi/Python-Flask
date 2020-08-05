import unittest
from unittest.mock import patch, MagicMock, Mock

from app.domains.product_line import ProductLineDoNotExistException, ProductLineInactiveException
from app.domains.product_line.actions import get_by_id, update, create, get, delete, get_by_name


class TestProductLineActions(unittest.TestCase):

    @patch('app.domains.product_line.actions.ProductLine')
    @patch('app.domains.product_line.actions.save')
    def test_action_create_should_be_created_new_product_line(self, save_mock, product_line_mock):
        # Arrange
        product_line_mock.name = 'product_line'
        product_line_mock.category_line = 'category_line'
        save_mock.return_value = product_line_mock

        # Action
        create({'name': 'product_line',
                'category_line': 'category_line'})

        # Assert
        save_mock.assert_called_once_with(product_line_mock())
        self.assertTrue(save_mock.called)
        self.assertEqual(product_line_mock.name, 'product_line')
        self.assertEqual(product_line_mock.category_line, 'category_line')
        self.assertEqual(save_mock.call_count, 1)

    @patch('app.domains.product_line.actions.ProductLine')
    def test_action_get_by_id_should_be_return_an_product_line(self, product_line_mock):
        # Arrange
        _id = '259830-582'
        product_line_mock.name = 'Name'
        product_line_mock.category = 'category'
        query = Mock()
        query.get = MagicMock(return_value=product_line_mock)
        product_line_mock.query = query

        # Action
        product_line = get_by_id(_id)
        product_line_mock()

        # Assert
        product_line_mock.query.get.assert_called_once_with(_id)
        self.assertEqual(product_line_mock, product_line)
        self.assertEqual(product_line_mock.call_count, 1)

    @patch('app.domains.product_line.actions.ProductLine')
    def test_action_get_by_name_should_be_return_an_product_line(self, product_line_mock):
        # Arrange
        name = 'Name'
        product_line_mock.id = '259830-582'
        product_line_mock.name = name
        product_line_mock.category = 'category'

        product_line_mock.query = MagicMock()
        query_mock = MagicMock()
        query_mock.first.return_value = product_line_mock
        product_line_mock.query.filter.return_value = query_mock

        product_line = get_by_name('Name')
        product_line_mock(name)

        product_line_mock.query.filter.assert_called_once_with(True)
        self.assertEqual(product_line_mock, product_line)
        self.assertEqual(product_line_mock.call_count, 1)

    @patch('app.domains.product_line.actions.ProductLine')
    def test_action_get_should_be_return_product_line(self, product_line_mock):
        # Arrange
        product_line_mock.name = 'Name'
        product_line_mock.category = 'category'
        query = Mock()
        query.filter_by().all = MagicMock(return_value=[product_line_mock])
        product_line_mock.query = query

        # Action
        product_line_mock.get = get({})
        product_line_mock()

        # Assert
        self.assertTrue(product_line_mock.query.filter_by().all.called)
        self.assertEqual(len(product_line_mock.get), 1)
        self.assertEqual(product_line_mock.call_count, 1)

    @patch('app.domains.product_line.actions.ProductLine')
    @patch('app.domains.product_line.actions.get_by_id')
    @patch('app.domains.product_line.actions.commit')
    def test_action_update_should_be_updated_product_line(self, commit_mock, get_by_id_mock, product_line_mock):
        # Arrange
        _id = '7389213'
        product_line_mock.name = 'Name'
        product_line_mock.category_line = 'category_line'
        get_by_id_mock.return_value = product_line_mock

        # Action
        product_line_mock = update(_id, {'name': 'NotName', 'category_line': 'Lactobacilos_vivos'})

        # Assert
        get_by_id_mock.assert_called_once_with(_id)
        self.assertTrue(commit_mock.called)
        self.assertEqual(product_line_mock.name, 'NotName')
        self.assertEqual(product_line_mock.category_line, 'Lactobacilos_vivos')
        self.assertEqual(get_by_id_mock.call_count, 1)

    @patch('app.domains.product_line.actions.ProductLine')
    @patch('app.domains.product_line.actions.get_by_id')
    @patch('app.domains.product_line.actions.commit')
    def test_action_delete_product_line_column_is_active_should_be_false(self, commit_mock, get_by_id_mock,
                                                                         product_line_mock):
        # Arrange
        _id = '7389213'
        product_line_mock.is_active = True
        get_by_id_mock.return_value = product_line_mock

        # Action
        delete(_id)

        # Assert
        commit_mock.assert_called_once()
        get_by_id_mock.assert_called_once_with(_id)
        self.assertFalse(product_line_mock.is_active)
        self.assertEqual(commit_mock.call_count, 1)

    @patch('app.domains.product_line.actions.ProductLine')
    def test_should_raise_exception_when_try_to_get_by_id_an_inexistent_product_line(self, product_line_mock):
        # Arrange
        query = Mock()
        query.get = MagicMock(return_value=None)
        product_line_mock.query = query

        # Action
        with self.assertRaises(ProductLineDoNotExistException) as ex:
            get_by_id('juicy')

        # Assert
        self.assertEqual(str(ex.exception.code), '404')
        self.assertEqual(str(ex.exception.description), 'Product line do not exist')

    @patch('app.domains.product_line.actions.ProductLine')
    @patch('app.domains.product_line.actions.get_by_id')
    def test_should_raise_exception_when_try_to_update_an_inactive_product_line(self, get_by_id_mock,
                                                                                product_line_mock):
        # Arrange
        get_by_id_mock.return_value = product_line_mock
        product_line_mock.is_active = False

        # Action
        with self.assertRaises(ProductLineInactiveException) as ex:
            update('', {})

        # Assert
        get_by_id_mock.assert_called_once()
        self.assertEqual(str(ex.exception.code), '403')
        self.assertEqual(str(ex.exception.description), 'Unable to update an inactive product line')
