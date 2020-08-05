import unittest
from app.exceptions import BadRequestException
from app.domains.providers.address.address_validator import ValidateAddress


class TestAddressValidator(unittest.TestCase):
    def setUp(self) -> None:
        self._validator = ValidateAddress

    def test_validate_invalid_address(self):
        # Arrange
        address = {'street': '123123', 'zipcode': '11111-11123121', 'neighborhood': '',
                   'state': 'SCA', 'number': 'aaaa', 'city': '', 'comment': '', 'cotry': '132654',
                   }

        address2 = {'street': '123123', 'zip': '11111-11123121', 'neighborhd': '',
                    'state': 'SCA', 'number': 'aaaa', 'city': '', 'comment': ''
                    }

        # Assert
        with self.assertRaises(BadRequestException) as var:
            self._validator(address)

        self.assertEqual(str(var.exception.description), 'value null or invalid')
        self.assertEqual(str(var.exception.code), '400')

        with self.assertRaises(BadRequestException) as var:
            self._validator(address2)

        self.assertEqual(str(var.exception.description), 'value null or invalid')
        self.assertEqual(str(var.exception.code), '400')

    def test_validate_valid_address(self):
        # Arrange
        address_test = {'street': 'theodoro lueders', 'zipcode': '89031490', 'neighborhood': 'escola agricola',
                        'state': 'SC', 'number': '136', 'city': 'Blumenau', 'country': 'Brazil',
                        'id': '123'
                        }

        # Action
        address = ValidateAddress(address_test)

        # Assert
        self.assertIsInstance(address, ValidateAddress)
