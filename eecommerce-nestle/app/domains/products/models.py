from uuid import uuid4

from sqlalchemy import func

from app.domains.products import NullValueException
from database import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(36), unique=True)
    cost_values = db.Column(db.Float(20))
    unit_per_box = db.Column(db.Numeric(6))
    weight_per_unit = db.Column(db.String(10))
    measure_unit = db.Column(db.String(10), nullable=False)
    shelf_life = db.Column(db.String(10))
    sku = db.Column(db.String(10), unique=True)
    description = db.Column(db.String(70))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), default=None)
    is_active = db.Column(db.Boolean(10), default=True)
    id_product_line = db.Column(
        db.String(36),
        db.ForeignKey('product_line.id')
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for keys in kwargs:
            if kwargs[keys] is None or kwargs[keys] == '':
                raise NullValueException(f'The field {keys} can not be null')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cost_values": self.cost_values,
            "unit_per_box": int(self.unit_per_box),
            "weight_per_unit": self.weight_per_unit,
            'measure_unit': self.measure_unit,
            "shelf_life": self.shelf_life,
            "sku": self.sku,
            "description": self.description,
            "id_product_line": self.id_product_line,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
        }
