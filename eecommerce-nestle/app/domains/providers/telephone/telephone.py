import re
from app.domains.providers.telephone.exceptions import InvalidTelephoneException, InvalidSizeTelephoneException


class Telephone:
    def __init__(self, value: str):
        Telephone._validate(value)
        self._number = value

    @staticmethod
    def _validate(value: str) -> None:
        _check_len_is_valid(value)
        _check_if_the_value_is_in_telephone_format(value)

    def get_number(self) -> str:
        return self._number


def _is_match(match: str, number_sliced: str) -> bool:
    return re.findall(match, number_sliced)


def _check_len_is_valid(value: str) -> None:
    min_size = 11
    max_size = 12
    if len(value) not in [min_size, max_size]:
        raise InvalidSizeTelephoneException()


def _check_if_the_value_is_in_telephone_format(value: str) -> None:
    value_sliced = value[3:]
    match_if_number_sliced_has_9_digit = _is_match("\\d{9}", value_sliced)
    match_if_number_sliced_has_8_digit = _is_match("\\d{8}", value_sliced)
    if not match_if_number_sliced_has_8_digit and not match_if_number_sliced_has_9_digit:
        raise InvalidTelephoneException()
