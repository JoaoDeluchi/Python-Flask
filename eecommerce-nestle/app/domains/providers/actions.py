import datetime
from typing import NoReturn, List

from app.domains import category
from app.domains.category.models import Category
from app.domains.category.actions import get_by_id as get_category_by_id
from database import db

from app.domains.providers import ProviderDoNotExistException, ProviderInactiveException
from app.domains.providers.address.actions import create as create_address
from app.domains.providers.address.address_validator import ValidateAddress
from app.domains.providers.models import Provider, provider_category
from app.domains.category.actions import get_by_id as get_category_by_id
from database.repository import save, commit


def create(data: dict) -> Provider:
    address = data.pop("address")
    provider = Provider(**data)
    ValidateAddress(address)
    provider_saved = save(provider)
    address.update({"provider_id": provider.id})
    create_address(address)
    return provider_saved


def get(filters: dict) -> list:
    return Provider.query.filter_by(**filters).all()


def get_by_id(id: str) -> Provider:
    provider = Provider.query.get(id)
    if provider is None:
        raise ProviderDoNotExistException
    return provider


def update(id: str, data: dict) -> Provider:
    provider = get_by_id(id)
    if not provider.is_active:
        raise ProviderInactiveException
    provider.name = data.get('name')
    provider.cnpj = data.get('cnpj')
    provider.fantasy_name = data.get('fantasy_name')
    provider.phone1 = data.get('phone1')
    provider.phone2 = data.get('phone2')
    provider.phone3 = data.get('phone3')
    provider.email = data.get('email')
    commit()
    return provider


def delete(id: str) -> NoReturn:
    provider = get_by_id(id)
    provider.is_active = False
    provider.deleted_at = str(datetime.datetime.now())
    commit()


def populate_table_provider_category_association(data: dict) -> Provider:
    provider = get_by_id(data['provider_id'])
    provider.category.append(get_category_by_id(data['category_id']))
    provider_category = save(provider)
    return provider_category


def get_categories_from_provider(id: str) -> List:
    provider_categories = Provider.query.get(id).category
    return [{'id': category.serialize()['id'], 'name': category.serialize()['name']} for category in provider_categories]
