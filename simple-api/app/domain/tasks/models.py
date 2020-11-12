from database import db
from sqlalchemy import func
from uuid import uuid4


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    is_active = db.Column(db.Boolean, unique=False, default=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for keys in kwargs:
            if kwargs[keys] is None or kwargs[keys] == '':
                raise NullValueException(f'The field {keys} can not be null')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'updated_at': self.updated_at,
            'created': self.created_at,
        }