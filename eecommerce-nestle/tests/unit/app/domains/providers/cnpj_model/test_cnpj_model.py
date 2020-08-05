import unittest
import pytest
from app.domains.providers.cnpj_model.cnpj_model import CNPJModel
from app.domains.providers.cnpj_model import InvalidCnpjException


class TestCNPJModel(unittest.TestCase):
    def test_cnpj_should_be_exception(self):
        with pytest.raises(InvalidCnpjException) as ex:
            CNPJModel('')

        # Assert
        self.assertEqual(str(ex.value.description), 'Invalid CNPJ')
        self.assertEqual(str(ex.value.code), '400')

    def test_cnpj_should_be_create(self):
        cnpj = CNPJModel('54575673000107')

        # Assert
        self.assertEqual(cnpj.get_value(), '54575673000107')

    def test_cnpj_model_should_be_exception_because_first_digit_is_invalid(self):
        with pytest.raises(InvalidCnpjException) as ex:
            CNPJModel('54575673000187')

        # Assert
        self.assertEqual(str(ex.value.description), 'Invalid CNPJ')
        self.assertEqual(str(ex.value.code), '400')


    def test_cnpj_model_should_be_exception_because_second_digit_is_invalid(self):
        with pytest.raises(InvalidCnpjException) as ex:
            CNPJModel('54575673000105')

        # Assert
        self.assertEqual(str(ex.value.description), 'Invalid CNPJ')
        self.assertEqual(str(ex.value.code), '400')
