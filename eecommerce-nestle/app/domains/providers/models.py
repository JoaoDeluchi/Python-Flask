from uuid import uuid4
from sqlalchemy import func
from app.domains.providers import NullOrNoneValueException
from database import db
from app.domains.providers.emails.emails import Email
from app.domains.providers.cnpj_model.cnpj_model import CNPJModel
from app.domains.providers.telephone.telephone import Telephone

provider_category = db.Table(
    'provider_category',
    db.Column('provider_id', db.String(36), db.ForeignKey("provider.id"), primary_key=True),
    db.Column('category_id', db.String(36), db.ForeignKey("category.id"), primary_key=True),
)


class Provider(db.Model):
    __tablename__ = 'provider'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(80))
    fantasy_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    cnpj = db.Column(db.String(18), unique=True)
    phone1 = db.Column(db.String(12))
    phone2 = db.Column(db.String(12), default=None)
    phone3 = db.Column(db.String(12), default=None)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=None, onupdate=func.now())
    is_active = db.Column(db.Boolean, unique=False, default=True)
    deleted_at = db.Column(db.DateTime(timezone=True), default=None)
    address = db.relationship(
        'Address',
        backref='provider',
        uselist=False
    )
    category = db.relationship(
        'Category',
        secondary=provider_category,
        backref='provider',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for keys in kwargs:
            if keys != 'phone2' or keys != 'phone3':
                if kwargs[keys] is None or kwargs[keys] == '':
                    raise NullOrNoneValueException(f'the field {keys} is empty')
            Email(kwargs['email'])
            CNPJModel(kwargs['cnpj'])
            Telephone(kwargs['phone1'])
            Telephone(kwargs['phone2'])
            Telephone(kwargs['phone3'])

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "fantasy_name": self.fantasy_name,
            "email": self.email,
            "cnpj": self.cnpj,
            "phone1": self.phone1,
            "phone2": self.phone2,
            "phone3": self.phone3,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "deleted_at": self.deleted_at,
            "address": self.address.serialize()
        }

    def minimum_serialize(self):
        return {
            "id": self.id,
            "fantasy_name": self.fantasy_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
