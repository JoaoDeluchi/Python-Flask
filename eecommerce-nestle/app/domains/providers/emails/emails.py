from validate_email import validate_email
from app.domains.providers.emails.exceptions import EmailNotValidException


class Email:
    def __init__(self, value):
        if not self._is_valid(value):
            raise EmailNotValidException()
        self._value = value

    @staticmethod
    def _is_valid(value) -> bool:
        is_valid = validate_email(value)
        return is_valid

    def get_email(self) -> str:
        return self._value
