from app.domains.products import ProductFieldInvalidException
from app.domains.products.models import Product
from app.exceptions import ProductExceptions
from database.repository import save
from app.domains.product_line.models import ProductLine


def get_product_line_by_name_and_return_id(name: str) -> ProductLine:
    product_line = ProductLine.query.filter(ProductLine.name == name).first()
    return product_line.id


def get_product_line_by_id(id: str) -> ProductLine:
    return ProductLine.query.filter(ProductLine.id == id).first()


def get_by_name(name: str) -> Product:
    return Product.query.filter(Product.name == name).first()


def get_by_sku(sku: str) -> Product:
    return Product.query.filter(Product.sku == sku).first()


class ValidateCreateProduct:
    def __init__(self, product):
        self._product = product
        self._name = self._product['name']
        self._shelf_life = self._product['shelf_life']
        self.product_exceptions = []

    def check_if_product_is_valid(self):
        list_of_validations = [self._name_is_duplicated(), self._description_is_valid(),
                               self._sku_is_valid(), self._sku_is_duplicated(),
                               self._shelf_life_is_string(),
                               self._shelf_life_only_number_and_letters(),
                               self._shelf_life_not_is_null(), self._weight_per_unit_is_valid(),
                               self._cost_values_is_valid(),
                               self._measure_unit_is_valid(),
                               self._check_if_name_is_not_null(),
                               self._validate_foreign_key(),
                               ]
        for validation in list_of_validations:
            if validation is not True:
                self.product_exceptions.append(ProductFieldInvalidException(validation[0], validation[1]).serialize())
        return self.product_exceptions

    def check_if_product_of_excel_is_valid(self):
        list_of_validations = [self._name_is_duplicated(), self._description_is_valid(),
                               self._sku_is_valid(), self._sku_is_duplicated(),
                               self._shelf_life_is_string(),
                               self._shelf_life_only_number_and_letters(),
                               self._shelf_life_not_is_null(), self._weight_per_unit_is_valid(),
                               self._cost_values_is_valid(),
                               self._measure_unit_is_valid(),
                               self._check_if_name_is_not_null(),
                               self._delete_product_line_and_insert_id_product_line_on_dict(),
                               self._validate_foreign_key(),
                               ]
        for validation in list_of_validations:
            if validation is not True:
                self.product_exceptions.append(ProductFieldInvalidException(validation[0], validation[1]).serialize())
        return self.product_exceptions

    def _name_is_duplicated(self):
        if get_by_name(self._name):
            return f'product already in database {self._name}', 409
        return True

    def _check_if_name_is_not_null(self):
        flag = False
        if self._name == '' or self._name is None:
            return f'name of product cant be null {self._name}', 422
        for char in self._name:
            if char.isalpha():
                flag = True
        if flag is False:
            return f'name of product cant be null {self._name}', 422
        return True

    def _sku_is_valid(self):
        if len(str(self._product['sku'])) != 10:
            return f'invalid size of sku in product {self._name}', 422
        return True

    def _sku_is_duplicated(self):
        sku = str(self._product['sku'])
        sku = get_by_sku(sku)
        if sku:
            return f'sku already in database {self._name} ', 409
        return True

    def _description_is_valid(self):
        if not self._product['description'].isalpha() and not self._product['description'] != ' ':
            return f'{self._name} - description just accept letters and spaces', 422
        return True

    def _shelf_life_only_number_and_letters(self):
        for char in str(self._shelf_life):
            if not char.isalpha() and not char.isnumeric():
                return f'{self._name} - shelf life just accept letters and Numbers', 422
        return True

    def _shelf_life_is_string(self):
        if not type(self._shelf_life) is str:
            return f'{self._name} - shelf life need to be a string', 409
        return True

    def _shelf_life_not_is_null(self):
        if self._shelf_life == '' or self._shelf_life is None:
            return f'shelf life of product cant be null {self._name}', 422
        return True

    def _weight_per_unit_is_valid(self):
        if type(self._product['weight_per_unit']) != int:
            return f'{self._name} - weight per unit must be an integer', 422
        return True

    def _cost_values_is_valid(self):
        cost_values = str(self._product['cost_values'])
        for char in cost_values:
            if not char.isnumeric() and char != '.':
                return f'{self._name} - cost values must be an string with number', 422
            return True

    def _measure_unit_is_valid(self):
        measure_unit = str(self._product['measure_unit'])
        if not measure_unit.isalpha():
            return f'product {self._name} - measure unit just accept letters', 422
        return True

    def _validate_foreign_key(self):
        product_line = str(self._product['id_product_line'])
        if not get_product_line_by_id(product_line):
            return f'{self._name} - product line {product_line} do not exist', 404
        return True

    def _delete_product_line_and_insert_id_product_line_on_dict(self):
        _id = get_product_line_by_name_and_return_id(self._product['product_line'])
        if _id:
            self._product['id_product_line'] = _id
            del self._product['product_line']
            return True
        return f'{self._name} - product line id - {_id} do not exist', 404
