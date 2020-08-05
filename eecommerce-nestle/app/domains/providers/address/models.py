from uuid import uuid4
from app.domains.providers.address import NullOrNoneValueException
from database import db


class Address(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    street = db.Column(db.String(150))
    zipcode = db.Column(db.String(8))
    neighborhood = db.Column(db.String(60))
    number = db.Column(db.String(20))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    country = db.Column(db.String(80))
    complement = db.Column(db.String(80))
    provider_id = db.Column(db.String, db.ForeignKey('provider.id'), nullable=False, index=True)
    providers = db.relationship('Provider', backref='addresses', foreign_keys=[provider_id])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for keys in kwargs:
            if kwargs[keys] is None or kwargs[keys] == '':
                raise NullOrNoneValueException()

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "street": self.street,
            "zipcode": self.zipcode,
            "neighborhood": self.neighborhood,
            "number": self.number,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "complement": self.complement
        }
