from datetime import datetime

from flask import send_file

from app.domains.product_line.models import ProductLine
from app.domains.products import ProductDoNotExistException, ProductInactiveException, ProductFieldInvalidException, \
     NoDataToExportException
from openpyxl import load_workbook
from app.domains.excel.import_excel.models import ImportExcel
from app.domains.products.models import Product
from app.domains.products.validate_product import ValidateCreateProduct
from app.exceptions import ProductExceptions
from database.repository import save, commit
from typing import NoReturn, List, Tuple, Any
from app.domains.excel.export_excel.models import ExportExcel
from app.domains.product_line.actions import get_by_id as get_by_id_product_line


def create(data: dict):
    except_list = ValidateCreateProduct(data).check_if_product_is_valid()
    try:
        return save(Product(**data))
    except Exception:
        raise ProductExceptions(except_list)


def get(filters: dict) -> List[Product]:
    return Product.query.filter_by(**filters).all()


def get_by_name(name: str) -> Product:
    return Product.query.filter(Product.name == name).first()


def get_by_id(id: str) -> Product:
    product = Product.query.get(id)
    if product is None:
        raise ProductDoNotExistException('Product do not exist in database')
    return product


def update(id: str, data: dict) -> Product:
    product = get_by_id(id)
    if not product.is_active:
        raise ProductInactiveException
    product.name = data.get('name')
    product.cost_values = data.get('cost_values')
    product.unit_per_box = data.get('unit_per_box')
    product.weight_per_unit = data.get('weight_per_unit')
    product.measure_unit = data.get('measure_unit')
    product.shelf_life = data.get('shelf_life')
    product.sku = data.get('sku')
    product.description = data.get('description')
    product.id_product_line = data.get('id_product_line')
    commit()
    return product


def delete(id: str) -> NoReturn:
    product = get_by_id(id)
    product.is_active = False
    product.deleted_at = str(datetime.now())
    commit()


def rename_headers() -> tuple:
    excel = ExportExcel('products')
    products = get({})
    headers = [i for i in products[0].serialize().keys()]
    headers.remove('id')
    headers.remove('id_product_line')
    headers.append('product_line')
    [excel.save_table_sheet(1, i, headers[i - 1]) for i in range(1, len(headers) + 1)]
    return excel, products


def export_product() -> str:
    try:
        excel, products = rename_headers()
    except Exception:
        raise NoDataToExportException()
    row = 2
    for products in products:
        column = 1
        data_products = products.serialize()
        data_products.pop('id')
        product_line = get_by_id_product_line(data_products['id_product_line'])
        data_products['product_line'] = product_line.name
        data_products.pop('id_product_line')

        for value in data_products.values():
            excel.save_table_sheet(row, column, value)
            column += 1
        row += 1
    return excel.file_name


def upload_file(file: List[dict]):
    parameters = ('name', 'cost_values',
                  'product_line', 'unit_per_box',
                  'unit_per_box', 'weight_per_unit',
                  'measure_unit', 'shelf_life', 'sku',
                  'description')
    list_of_products = ImportExcel(load_workbook(file))
    list_of_products = list_of_products.read_cells(*parameters)
    list_of_exceptions = []
    list_of_saved_products = []
    for product in list_of_products:
        list_of_exceptions.append(ValidateCreateProduct(product).check_if_product_of_excel_is_valid())
    try:
        for product in list_of_products:
            list_of_saved_products.append(save(Product(**product)))
    except Exception:
        raise ProductExceptions(list_of_exceptions)
    return list_of_saved_products


