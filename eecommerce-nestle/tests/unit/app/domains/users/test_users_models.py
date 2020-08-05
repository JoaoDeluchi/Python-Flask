import unittest

from app.domains.users.models import User
from uuid import uuid4


class TestUsersModels(unittest.TestCase):
    def test_user_model_should_be_serialized(self):
        # Arrange
        _id = str(uuid4())
        user = User(id=_id, name='Teste', email='test@test.com')

        # Action
        json = user.serialize()

        # Assert
        self.assertEqual(json['id'], _id)
        self.assertEqual(json['name'], 'Teste')
