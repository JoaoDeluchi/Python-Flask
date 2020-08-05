from app.domains.users.models import User
from database.repository import save, commit
from uuid import uuid4
from typing import NoReturn


def create(data):
    return save(User(id=str(uuid4()), name=data['name'], email=data['email']))


def get():
    return User.query.all()


def get_by_id(id):
    return User.query.get(id)


def update(id, data):
    user = get_by_id(id)
    user.name = data.get('name')
    commit()
    return user


def delete(id: str) -> NoReturn:
    user = get_by_id(id)
    user.is_active = False
    commit()

