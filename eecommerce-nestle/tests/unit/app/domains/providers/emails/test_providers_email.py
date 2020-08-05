from app.domains.providers.emails.emails import Email
from unittest.mock import patch
import unittest
import pytest
from app.domains.providers.emails.exceptions import EmailNotValidException


class TestEmail(unittest.TestCase):
    @patch('app.domains.providers.emails.emails.validate_email')
    def test_email_response_should_be_raise_exception(self, validate_email_mock):
        validate_email_mock.return_value = False
        with pytest.raises(EmailNotValidException) as var:
            Email('euoedu00@googlengui.com')
        self.assertEqual(str(var.value.description), 'invalid email')
        self.assertEqual(str(var.value.code), '422')

    @patch('app.domains.providers.emails.emails.validate_email')
    def test_email_response_should_be_valid(self, validate_email_mock):
        validate_email_mock.return_value = True
        email = Email('euoedu00@gmail.com')
        self.assertTrue(email)
        self.assertEqual('euoedu00@gmail.com', email.get_email())




