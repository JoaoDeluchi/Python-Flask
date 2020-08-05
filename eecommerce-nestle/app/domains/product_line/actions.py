from datetime import datetime
from typing import List

from app.domains.product_line import ProductLineDoNotExistException, ProductLineInactiveException
from app.domains.product_line.models import ProductLine
from database.repository import save, commit


def create(data: dict) -> ProductLine:
    return save(ProductLine(**data))


def get_by_id(id: str) -> ProductLine:
    product_line = ProductLine.query.get(id)
    if product_line is None:
        raise ProductLineDoNotExistException
    return product_line


def get(filters: dict) -> List[ProductLine]:
    return ProductLine.query.filter_by(**filters).all()


def get_by_name(name: str) -> ProductLine:
    return ProductLine.query.filter(ProductLine.name == name).first()


def update(id: str, data: dict) -> ProductLine:
    product_line = get_by_id(id)
    if product_line.is_active == False:
        raise ProductLineInactiveException
    product_line.name = data.get('name')
    product_line.category_line = data.get('category_line')
    commit()
    return product_line


def delete(id: str) -> None:
    product_line = get_by_id(id)
    product_line.is_active = False
    product_line.deleted_at = str(datetime.now())
    commit()