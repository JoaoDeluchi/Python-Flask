import re

from app.domains.providers.address import NullOrNoneValueException

_MIN_FIELDS_ACCEPTABLE = 8
_MAX_FIELDS_ACCEPTABLE = 9
_ZIPCODE_SIZE = 8
_WORD_STATE_SIZE = 2


class ValidateAddress:

    def __init__(self, address: dict):
        self._address = address
        if not self._is_all_valid():
            raise NullOrNoneValueException

    def _is_all_valid(self) -> bool:
        if self._are_fields_valid():
            result = [
                self._is_zip_valid(),
                self._is_city_valid(),
                self._is_street_valid(),
                self._is_number_valid(),
                self._is_neighborhood_valid(),
                self._is_state_valid(),
                self._is_country_valid()
            ]
            return all(result)
        return False

    def _are_fields_valid(self) -> bool:
        if len(self._address) >= _MIN_FIELDS_ACCEPTABLE and len(self._address) <= _MAX_FIELDS_ACCEPTABLE:
            if not self._are_field_names_valid():
                return False
            return True
        return False

    def _are_field_names_valid(self) -> bool:
        names = ['zipcode', 'state', 'city', 'street', 'number', 'neighborhood', 'country']
        for name in names:
            if not name in self._address:
                return False
        return True

    def _is_zip_valid(self) -> bool:
        code = find_numbers(self._address['zipcode'])
        zipcode = ''.join(code)
        return len(zipcode) == _ZIPCODE_SIZE

    def _is_number_valid(self) -> bool:
        list_number = find_numbers(self._address['number'])
        number = ''.join(list_number)
        return is_not_empty(number)

    def _is_street_valid(self) -> bool:
        street = ''.join(find_letters(self._address['street']))
        return is_not_empty(street)

    def _is_neighborhood_valid(self) -> bool:
        return is_not_empty(find_letters(self._address['neighborhood']))

    def _is_city_valid(self) -> bool:
        city = ''.join(find_letters(self._address['city']))
        return is_not_empty(city)

    def _is_state_valid(self) -> bool:
        state = ''.join(find_letters(self._address['state']))
        return len(state) == _WORD_STATE_SIZE

    def _is_country_valid(self) -> bool:
        country = ''.join(find_letters(self._address['country']))
        return is_not_empty(country)


def is_not_empty(typee: str) -> bool:
    return len(typee)


def find_letters(typee: str) -> list:
    return re.findall("[a-zA-Z]+", typee)


def find_numbers(typee: str) -> list:
    return re.findall("[0-9]+", typee)
