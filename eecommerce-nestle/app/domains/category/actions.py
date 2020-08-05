from datetime import datetime
from typing import NoReturn, List

from openpyxl import load_workbook

from app.domains.category import ErrorCategory, AlreadyExistsException, CategoryInactiveException, \
    CategoryDoNotExistException
from app.domains.category.models import Category
from app.domains.excel.export_excel.models import ExportExcel
from app.domains.excel.import_excel.models import ImportExcel, BadRequestException
from database.repository import save, commit


def _verify_category_name(data:dict):
    if data['name'] in [categories.name for categories in get({})]:
        raise AlreadyExistsException()

def create(data: dict) -> Category:
    _verify_category_name(data)
    return save(Category(**data))


def get(filters: dict) -> List[Category]:
    return Category.query.filter_by(**filters).all()


def get_by_id(id: str) -> Category:
    category = Category.query.get(id)
    if category is None:
        raise CategoryDoNotExistException()
    return category


def update(id: str, data: dict) -> Category:
    category = get_by_id(id)
    if category.is_active == False:
        raise CategoryInactiveException()
    category.name = data.get('name')
    category.profit_percent = data.get('profit_percent')
    _verify_category_name(data)
    commit()
    return category


def delete(id: str) -> NoReturn:
    category = get_by_id(id)
    category.is_active = False
    category.deleted_at = str(datetime.now())
    commit()


def upload_file(file: object) -> List[Category]:
    try:
        excel = ImportExcel(load_workbook(file))
    except:
        raise BadRequestException
    result = excel.read_cells('name', 'profit_percent')
    return [create(category) if all(category.values()) and category['name'] not in [categories.name for categories in get({})] else ErrorCategory(category['name']) for category in result]


def export_file() -> str:
    excel = ExportExcel('categories')
    categories = get({})
    headers = [i for i in categories[0].serialize().keys()]
    headers.remove('id')
    [excel.save_table_sheet(1, i, headers[i - 1]) for i in range(1, len(headers) + 1)]
    row = 2
    for category in categories:
        column = 1
        data_category = category.serialize()
        data_category.pop('id')
        for value in data_category.values():
            excel.save_table_sheet(row, column, value)
            column += 1
        row += 1
    return excel.file_name


def get_providers_from_category(id: str) -> List:
    categories_providers = Category.query.get(id).provider
    return [{'id': provider.serialize()['id'], 'name': provider.serialize()['name']} for provider in categories_providers]