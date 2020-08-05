import unittest
from unittest.mock import patch, Mock, MagicMock

import pytest

from app.domains.products import ProductFieldInvalidException
from app.domains.products.validate_product import get_product_line_by_id, ValidateCreateProduct, get_by_name, \
    get_by_sku, get_product_line_by_name_and_return_id


class TestValidateProduct(unittest.TestCase):

    @patch('app.domains.products.validate_product.ProductLine')
    def test_get_product_line_by_name_and_return_id_must_return_a_product(self, product_line_mock):
        name = 'name_of_product_line'
        data = Mock()
        data.name = name
        data.id = '3895423958-29235729hj82953'
        query = Mock()
        query.filter = Mock()
        product_line_mock.query.filter(name).first.return_value = data

        product_line_id = get_product_line_by_name_and_return_id(name)
        self.assertEqual(product_line_id, data.id)
        product_line_mock.query.filter(name).first.assert_called_once()

    @patch('app.domains.products.validate_product.ProductLine')
    def test_get_product_line_by_id_must_return_a_product(self, product_line_mock):
        _id = '126748219'
        data = {'name': 'product_line', 'id': _id}
        query = Mock()
        query.filter = Mock()

        return_product = MagicMock()
        return_product.id = data['id']
        return_product.name = data['name']

        product_line_mock.query.filter(_id).first.return_value = return_product

        product_line = get_product_line_by_id(_id)
        self.assertEqual(product_line.id, data['id'])
        self.assertEqual(product_line.name, data['name'])
        product_line_mock.query.filter(_id).first.assert_called_once()

    @patch('app.domains.products.validate_product.Product')
    def test_get_product_by_name_must_return_a_product(self, product_mock):
        name = 'product'
        data = {'name': name, 'id': '126748219'}
        query = Mock()
        query.filter = Mock()

        return_product = MagicMock()
        return_product.id = data['id']
        return_product.name = data['name']

        product_mock.query.filter(name).first.return_value = return_product
        product = get_by_name(name)
        self.assertEqual(product.id, data['id'])
        self.assertEqual(product.name, name)
        product_mock.query.filter(name).first.assert_called_once()

    @patch('app.domains.products.validate_product.Product')
    def test_get_product_by_sku_must_return_a_product(self, product_mock):
        sku = '1234567891'
        data = {'name': 'product', 'id': '126748219', 'sku': sku}
        query = Mock()
        query.filter = Mock()

        return_product = MagicMock()
        return_product.id = data['id']
        return_product.name = data['name']
        return_product.sku = data['sku']

        product_mock.query.filter(sku).first.return_value = return_product
        product = get_by_sku(sku)
        self.assertEqual(product.id, data['id'])
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.sku, data['sku'])
        product_mock.query.filter(sku).first.assert_called_once()

    @patch.object(ProductFieldInvalidException, 'serialize')
    @patch.object(ValidateCreateProduct, '_name_is_duplicated')
    @patch.object(ValidateCreateProduct, '_description_is_valid')
    @patch.object(ValidateCreateProduct, '_sku_is_valid')
    @patch.object(ValidateCreateProduct, '_sku_is_duplicated')
    @patch.object(ValidateCreateProduct, '_shelf_life_is_string')
    @patch.object(ValidateCreateProduct, '_shelf_life_only_number_and_letters')
    @patch.object(ValidateCreateProduct, '_shelf_life_not_is_null')
    @patch.object(ValidateCreateProduct, '_weight_per_unit_is_valid')
    @patch.object(ValidateCreateProduct, '_cost_values_is_valid')
    @patch.object(ValidateCreateProduct, '_measure_unit_is_valid')
    @patch.object(ValidateCreateProduct, '_validate_foreign_key')
    @patch.object(ValidateCreateProduct, '_check_if_name_is_not_null')
    def test_check_if_product_is_valid_all_mock_called(self, mock_name_is_duplicated, mock_description_is_valid,
                                       mock_sku_is_valid, mock_sku_is_duplicated, mock_shelf_life_is_string,
                                       mock_shelf_life_only_number_and_letters, mock_shelf_life_not_is_null,
                                       mock_weight_per_unit_is_valid, mock_cost_values_is_valid,
                                       mock_measure_unit_is_valid, mock_validate_foreign_key,
                                       mock_check_if_name_is_not_null, mock_serialize):
        _product = {'name': 'name',
                    'shelf_life': '12meses'}
        mock_serialize.return_value = ({'error': 'error', 'code': 'code'})
        mock_name_is_duplicated.return_value = True
        mock_description_is_valid.return_value = True
        mock_sku_is_valid.return_value = True
        mock_sku_is_duplicated.return_value = True
        mock_shelf_life_is_string.return_value = True
        mock_shelf_life_only_number_and_letters.return_value = True
        mock_shelf_life_not_is_null.return_value = True
        mock_weight_per_unit_is_valid.return_value = True
        mock_cost_values_is_valid.return_value = True
        mock_measure_unit_is_valid.return_value = True
        mock_validate_foreign_key.return_value = True
        mock_check_if_name_is_not_null.return_value = ('error', 'code')
        response = ValidateCreateProduct(_product).check_if_product_is_valid()
        mock_name_is_duplicated.assert_called_once()
        mock_description_is_valid.assert_called_once()
        mock_sku_is_valid.assert_called_once()
        mock_sku_is_duplicated.assert_called_once()
        mock_shelf_life_is_string.assert_called_once()
        mock_shelf_life_only_number_and_letters.assert_called_once()
        mock_shelf_life_not_is_null.assert_called_once()
        mock_weight_per_unit_is_valid.assert_called_once()
        mock_cost_values_is_valid.assert_called_once()
        mock_measure_unit_is_valid.assert_called_once()
        mock_validate_foreign_key.assert_called_once()
        mock_check_if_name_is_not_null.assert_called_once()
        mock_serialize.assert_called_once()
        self.assertEqual(response, [{'code': 'code', 'error': 'error'}])



    @patch.object(ValidateCreateProduct, '_delete_product_line_and_insert_id_product_line_on_dict')
    @patch.object(ProductFieldInvalidException, 'serialize')
    @patch.object(ValidateCreateProduct, '_name_is_duplicated')
    @patch.object(ValidateCreateProduct, '_description_is_valid')
    @patch.object(ValidateCreateProduct, '_sku_is_valid')
    @patch.object(ValidateCreateProduct, '_sku_is_duplicated')
    @patch.object(ValidateCreateProduct, '_shelf_life_is_string')
    @patch.object(ValidateCreateProduct, '_shelf_life_only_number_and_letters')
    @patch.object(ValidateCreateProduct, '_shelf_life_not_is_null')
    @patch.object(ValidateCreateProduct, '_weight_per_unit_is_valid')
    @patch.object(ValidateCreateProduct, '_cost_values_is_valid')
    @patch.object(ValidateCreateProduct, '_measure_unit_is_valid')
    @patch.object(ValidateCreateProduct, '_validate_foreign_key')
    @patch.object(ValidateCreateProduct, '_check_if_name_is_not_null')
    def test_check_if_product_of_excel_is_valid(self, mock_name_is_duplicated, mock_description_is_valid,
                                       mock_sku_is_valid, mock_sku_is_duplicated, mock_shelf_life_is_string,
                                       mock_shelf_life_only_number_and_letters, mock_shelf_life_not_is_null,
                                       mock_weight_per_unit_is_valid, mock_cost_values_is_valid,
                                       mock_measure_unit_is_valid, mock_validate_foreign_key,
                                       mock_check_if_name_is_not_null, mock_serialize, mock_insert_id_product_line_on_dict):
        _product = {'name': 'name',
                    'shelf_life': '12meses'}
        mock_serialize.return_value = ({'error': 'error', 'code': 'code'})
        mock_name_is_duplicated.return_value = True
        mock_description_is_valid.return_value = True
        mock_sku_is_valid.return_value = True
        mock_sku_is_duplicated.return_value = True
        mock_shelf_life_is_string.return_value = True
        mock_shelf_life_only_number_and_letters.return_value = True
        mock_shelf_life_not_is_null.return_value = True
        mock_weight_per_unit_is_valid.return_value = True
        mock_cost_values_is_valid.return_value = True
        mock_measure_unit_is_valid.return_value = True
        mock_validate_foreign_key.return_value = True
        mock_check_if_name_is_not_null.return_value = ('error', 'code')
        mock_insert_id_product_line_on_dict.return_value = True
        response = ValidateCreateProduct(_product).check_if_product_of_excel_is_valid()
        mock_insert_id_product_line_on_dict.assert_called_once()
        mock_name_is_duplicated.assert_called_once()
        mock_description_is_valid.assert_called_once()
        mock_sku_is_valid.assert_called_once()
        mock_sku_is_duplicated.assert_called_once()
        mock_shelf_life_is_string.assert_called_once()
        mock_shelf_life_only_number_and_letters.assert_called_once()
        mock_shelf_life_not_is_null.assert_called_once()
        mock_weight_per_unit_is_valid.assert_called_once()
        mock_cost_values_is_valid.assert_called_once()
        mock_measure_unit_is_valid.assert_called_once()
        mock_validate_foreign_key.assert_called_once()
        mock_check_if_name_is_not_null.assert_called_once()
        mock_serialize.assert_called_once()
        self.assertEqual(response,[{'code': 'code', 'error': 'error'}])

    @patch('app.domains.products.validate_product.get_by_name')
    def test_name_is_duplicated_must_be_true(self, mock_get_by_name):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'sku': '1234567890'}
        mock_get_by_name.return_value = False
        validate_name = ValidateCreateProduct(product)._name_is_duplicated()
        self.assertTrue(validate_name)
        mock_get_by_name.called_once_with(product)

    @patch('app.domains.products.validate_product.get_by_name')
    def test_name_is_duplicated_must_be_a_tuple(self, mock_get_by_name):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'sku': '1234567890'}
        mock_get_by_name.return_value = True
        validate_name = ValidateCreateProduct(product)._name_is_duplicated()
        self.assertEqual(('product already in database name', 409), validate_name)
        mock_get_by_name.called_once_with(product)

    def test_check_if_name_is_not_null_must_return_true(self):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'sku': '1234567890'}
        validate_name = ValidateCreateProduct(product)._check_if_name_is_not_null()
        self.assertTrue(validate_name)

    def test_check_if_name_is_null_must_return_tuple_because_name_is_null(self):
        product = {'name': '',
                   'shelf_life': '12meses',
                   'sku': '1234567890'}
        validate_name = ValidateCreateProduct(product)._check_if_name_is_not_null()
        self.assertEqual(('name of product cant be null ', 422), validate_name)

    def test_check_if_name_is_null_must_return_tuple_because_name_is_a_string_whithout_letters(self):
        product = {'name': '123',
                   'shelf_life': '12meses',
                   'sku': '1234567890'}
        validate_name = ValidateCreateProduct(product)._check_if_name_is_not_null()
        self.assertEqual(('name of product cant be null 123', 422), validate_name)

    def test_sku_is_valid_must_return_True(self):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'sku': '1234567890'}
        validate_sku = ValidateCreateProduct(product)._sku_is_valid()
        self.assertTrue(validate_sku)

    def test_sku_is_valid_must_return_a_tuple_with_message_and_code_of_error(self):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'sku': '12345670'}
        validate_sku = ValidateCreateProduct(product)._sku_is_valid()
        self.assertEqual(('invalid size of sku in product name', 422), validate_sku)

    @patch('app.domains.products.validate_product.get_by_sku')
    def test_sku_is_duplicated_must_return_True(self, mock_get_by_sku):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'sku': '1234567890'}
        mock_get_by_sku.return_value = False
        validate_sku = ValidateCreateProduct(product)._sku_is_duplicated()
        self.assertTrue(validate_sku)

    @patch('app.domains.products.validate_product.get_by_sku')
    def test_sku_is_duplicated_must_return_a_tuple_with_message_and_code_of_error(self, mock_get_by_sku):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'sku': '1234567890'}
        mock_get_by_sku.return_value = True
        validate_sku = ValidateCreateProduct(product)._sku_is_duplicated()
        self.assertEqual(('sku already in database name ', 409), validate_sku)
        mock_get_by_sku.called_once_with('1234567890')

    def test_description_is_valid_must_return_True(self):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'description': 'muito bom'}
        validate_shelf_life = ValidateCreateProduct(product)._description_is_valid()
        self.assertTrue(validate_shelf_life)

    def test_description_is_valid_must_return_tuple_with_message_and_code_of_error(self):
        product = {'name': 'name',
                   'shelf_life': '#$',
                   'description': ' '}
        validate_description = ValidateCreateProduct(product)._description_is_valid()
        self.assertEqual(('name - description just accept letters and spaces', 422), validate_description)




    def test_shelf_life_only_number_and_letters_must_return_True(self):
        product = {'name': 'name',
                   'shelf_life': '12meses',
                   'weight_per_unit': 2}
        validate_shelf_life = ValidateCreateProduct(product)._shelf_life_only_number_and_letters()
        self.assertTrue(validate_shelf_life)

    def test_shelf_life_only_number_and_letters_must_return_tuple_with_message_and_code_of_error(self):
        product = {'name': 'name',
                   'shelf_life': '#$',
                   'weight_per_unit': 2}
        validate_shelf_life = ValidateCreateProduct(product)._shelf_life_only_number_and_letters()
        self.assertEqual(('name - shelf life just accept letters and Numbers', 422), validate_shelf_life)



    def test_shelf_life_is_string_must_return_True(self):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'weight_per_unit': 2}
        validate_shelf_life = ValidateCreateProduct(product)._shelf_life_is_string()
        self.assertTrue(validate_shelf_life)

    def test_shelf_life_is_string_must_return_tuple_with_message_and_code_of_error(self):
        product = {'name': 'name',
                   'shelf_life': 214,
                   'weight_per_unit': 2}
        validate_shelf_life = ValidateCreateProduct(product)._shelf_life_is_string()
        self.assertEqual(('name - shelf life need to be a string', 409), validate_shelf_life)


    def test_shelf_life_not_is_null_must_return_True(self):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'weight_per_unit': 2}
        validate_shelf_life = ValidateCreateProduct(product)._shelf_life_not_is_null()
        self.assertTrue(validate_shelf_life)

    def test_shelf_life_not_is_null_must_return_tuple_with_message_and_code_of_error(self):
        product = {'name': 'name',
                   'shelf_life': '',
                   'weight_per_unit': '89243uj'}
        validate_shelf_life = ValidateCreateProduct(product)._shelf_life_not_is_null()
        self.assertEqual(('shelf life of product cant be null name', 422), validate_shelf_life)

    def test_weight_per_unit_is_valid_must_return_True(self):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'weight_per_unit': 2}
        validate_weight_per_unit = ValidateCreateProduct(product)._weight_per_unit_is_valid()
        self.assertTrue(validate_weight_per_unit)

    def test_weight_per_unit_is_valid_must_return_tuple_with_message_and_code_of_error(self):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'weight_per_unit': '89243uj'}
        validate_weight_per_unit = ValidateCreateProduct(product)._weight_per_unit_is_valid()
        self.assertEqual(('name - weight per unit must be an integer', 422), validate_weight_per_unit)

    def test_cost_values_is_valid_must_return_True(self):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'cost_values': 2}
        validate_cost_values = ValidateCreateProduct(product)._cost_values_is_valid()
        self.assertEqual(True, validate_cost_values)

    def test_cost_values_is_valid_must_return_a_tuple_with_message_and_code_of_error(self):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'cost_values': 'dahfva´vs'}
        validate_cost_values = ValidateCreateProduct(product)._cost_values_is_valid()
        self.assertEqual(('name - cost values must be an string with number', 422), validate_cost_values)

    def test_measure_unit_is_valid_must_return_True(self):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'measure_unit': 'SAYSGAYSGA'}
        validate_measure_unit = ValidateCreateProduct(product)._measure_unit_is_valid()
        self.assertTrue(validate_measure_unit)

    def test_measure_unit_is_valid_must_return_a_tuple_with_message_and_code_of_error(self):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'measure_unit': '123676543'}
        validate_measure_unit = ValidateCreateProduct(product)._measure_unit_is_valid()
        self.assertEqual(('product name - measure unit just accept letters', 422), validate_measure_unit)

    @patch('app.domains.products.validate_product.get_product_line_by_id')
    def test_validate_foreign_key_must_return_true(self, mock_get_product_line_by_id):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'id_product_line': '535'}
        mock_get_product_line_by_id.return_value = True
        validate_foreign_key = ValidateCreateProduct(product)._validate_foreign_key()
        self.assertTrue(validate_foreign_key)

        mock_get_product_line_by_id.assert_called_once_with(product['id_product_line'])

    @patch('app.domains.products.validate_product.get_product_line_by_id')
    def test_validate_foreign_key_must_return_a_tuple_with_message_and_code_of_error(self, mock_get_product_line_by_id):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'id_product_line': ''}
        mock_get_product_line_by_id.return_value = False
        validate_foreign_key = ValidateCreateProduct(product)._validate_foreign_key()
        self.assertEqual(('name - product line  do not exist', 404), validate_foreign_key)

        mock_get_product_line_by_id.assert_called_once_with(product['id_product_line'])

    @patch('app.domains.products.validate_product.get_product_line_by_name_and_return_id')
    def test_delete_key_product_line_and_insert_id_product_line_must_return_true(self, mock_get_product_line_by_name):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'product_line': 'nescau'}
        _id = '34897230423-89342'
        mock_get_product_line_by_name.return_value = _id
        product_ = ValidateCreateProduct(product)._delete_product_line_and_insert_id_product_line_on_dict()
        self.assertTrue(product_)
        self.assertEqual(product['id_product_line'], _id)
        self.assertEqual(product_, True)
        mock_get_product_line_by_name.assert_called_once_with('nescau')


    @patch('app.domains.products.validate_product.get_product_line_by_name_and_return_id')
    def test_delete_key_product_line_and_insert_id_product_line_must_return_a_tuple_with_message_and_code_of_error(self, mock_get_product_line_by_name):
        product = {'name': 'name',
                   'shelf_life': 'shelf_life',
                   'product_line': 'nescau'}
        _id = '34897230423-89342'
        mock_get_product_line_by_name.return_value = False
        product_ = ValidateCreateProduct(product)._delete_product_line_and_insert_id_product_line_on_dict()
        self.assertEqual(product_, ('name - product line id - False do not exist', 404))
        mock_get_product_line_by_name.assert_called_once_with('nescau')
