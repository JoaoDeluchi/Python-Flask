import unittest
from app import create_app, db
from app.domains.providers.models import Provider
from app.domains.providers.address.models import Address
from app.domains.category.models import Category
from app.domains.products.models import Product
from app.domains.users.models import User
from app.domains.product_line.models import ProductLine


class AbstractViewUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self._app = create_app()
        db.create_all(app=self._app)
        self._client = self._app.test_client()

    def tearDown(self) -> None:
        db.drop_all(app=self._app)
