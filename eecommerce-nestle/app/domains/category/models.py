from uuid import uuid4
from app.domains.category import NullOrNoneValueException
from database import db
from sqlalchemy import func


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(80))
    profit_percent = db.Column(db.Float(2), default=0.0)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    is_active = db.Column(db.Boolean, unique=False, default=True)
    deleted_at = db.Column(db.DateTime(timezone=True), default=None)
    product_line = db.relationship('ProductLine', backref='product_line')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for keys in kwargs:
            if keys == 'id' or keys == 'name':
                if kwargs[keys] is None or kwargs[keys] == '':
                    raise NullOrNoneValueException(f'The {keys} is empty')

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "profit_percent": self.profit_percent,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "deleted_at": self.deleted_at
        }

