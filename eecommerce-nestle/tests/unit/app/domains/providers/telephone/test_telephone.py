import unittest
import pytest

from app.domains.providers.telephone.exceptions import InvalidSizeTelephoneException, InvalidTelephoneException
from app.domains.providers.telephone.telephone import Telephone


class TestTelephone(unittest.TestCase):

    def test_telephone_should_be_raise_invalid_size_with_many_characters(self):
        with pytest.raises(InvalidSizeTelephoneException) as ex:
            Telephone('479842131232131231231')

        # Assert
        self.assertEqual(str(ex.value.description), 'The size of telephone is invalid!')
        self.assertEqual(str(ex.value.code), '422')

    def test_telephone_should_be_raise_invalid_size_with_few_characters(self):
        with pytest.raises(InvalidSizeTelephoneException) as ex:
            Telephone('  ')

        # Assert
        self.assertEqual(str(ex.value.description), 'The size of telephone is invalid!')
        self.assertEqual(str(ex.value.code), '422')

    def test_telephone_should_be_raise_invalid_with_number_and_letters(self):
        with pytest.raises(InvalidTelephoneException) as ex:
            Telephone('479842441ab2')

        # Assert
        self.assertEqual(str(ex.value.description), 'This telephone is invalid!')
        self.assertEqual(str(ex.value.code), '422')

    def test_telephone_should_be_raise_invalid_with_only_letters(self):
        with pytest.raises(InvalidTelephoneException) as ex:
            Telephone('abcdefghjasb')

        # Assert
        self.assertEqual(str(ex.value.description), 'This telephone is invalid!')
        self.assertEqual(str(ex.value.code), '422')

    def test_should_be_return_number(self):
        # Arrange
        telephone = Telephone('047984244178')

        # Assert
        self.assertEqual(telephone.get_number(), '047984244178')
