from database.repository import save, commit
from app.domains.providers.address.models import Address
from typing import List


def create(data: dict) -> Address:
    return save(Address(**data))


def get() -> List[Address]:
    return Address.query.all()


def get_by_id(id: str) -> Address:
    return Address.query.get(id)


def update(id: str, data: dict) -> Address:
    address = get_by_id(id)
    address.street = data.get('street')
    address.zipcode = data.get('zipcode')
    address.neighborhood = data.get('neighborhood')
    address.number = data.get('number')
    address.city = data.get('city')
    address.state = data.get('state')
    address.country = data.get('country')
    address.complement = data.get('complement')
    commit()
    return address


def delete(id: str) -> None:
    address = get_by_id(id)
    address.is_active = False
    commit()
