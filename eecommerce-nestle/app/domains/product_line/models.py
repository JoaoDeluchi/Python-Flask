from uuid import uuid4

from sqlalchemy import func

from app.domains.product_line import NullValueException
from database import db


class ProductLine(db.Model):
    __tablename__ = 'product_line'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(30))
    id_category = db.Column(
        db.String(36),
        db.ForeignKey('category.id')
    )
    profit_percent = db.Column(db.Float(2), default=0.0)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    is_active = db.Column(db.Boolean, unique=False, default=True)
    deleted_at = db.Column(db.DateTime(timezone=True), default=None)
    product = db.relationship(
        'Product',
        backref='product_line'
    )

    def __init__(self, **kwargs):
        super(ProductLine, self).__init__(**kwargs)
        for keys in kwargs:
            if (kwargs[keys] is None) or (kwargs[keys] == ''):
                raise NullValueException(f'The field {keys} cannot be null!')

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "id_category": self.id_category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "deleted_at": self.deleted_at
        }
