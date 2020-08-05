import unittest

import pytest

from app.domains.products import ProductFieldInvalidException


class TestProductExceptions(unittest.TestCase):
    def test_product_field_invalid_exception_serialize(self):
        description = 'msg of error'
        code = 400
        test_serialize = ProductFieldInvalidException(description, code).serialize()
        self.assertEqual(test_serialize, {'error': 'msg of error', 'code': 400})


