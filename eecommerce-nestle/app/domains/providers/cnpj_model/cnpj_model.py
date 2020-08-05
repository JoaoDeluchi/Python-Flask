from app.domains.providers.cnpj_model import InvalidCnpjException

_values_to_multiply_first_digit = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
_values_to_multiply_second_digit = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
_required_divider = 11


class CNPJModel:
    def __init__(self, value: str):
        if not CNPJModel._is_valid(value):
            raise InvalidCnpjException()
        self._value = value

    def get_value(self) -> str:
        return self._value

    @staticmethod
    def _is_valid(value: str) -> bool:
        digit_list = _turn_out_a_string_to_be_a_list_of_integer(value)

        if not _cnpj_size_is_valid(value):
            return False
        if not _digit_is_valid(digit_list, _values_to_multiply_first_digit):
            return False
        if not _digit_is_valid(digit_list, _values_to_multiply_second_digit):
            return False
        return True


def _turn_out_a_string_to_be_a_list_of_integer(value: str) -> list:
    digit_list = []
    for i in range(len(value)):
        digit_list.append(int(value[i]))
    return digit_list


def _multiply_the_cnpj_digits_by_the_required_values(value: list, values_to_multiply: list) -> list:
    list_of_multiplies_values = []

    for i in range(len(values_to_multiply)):
        list_of_multiplies_values.append(int(value[i] * values_to_multiply[i]))
    return list_of_multiplies_values


def _digit_is_valid(value: list, values_to_multiply: list) -> bool:
    list_of_multiplies_values = _multiply_the_cnpj_digits_by_the_required_values(value, values_to_multiply)
    rest_of_division = _calculate_rest_of_division(list_of_multiplies_values)
    digit_value = _verify_digit_value(rest_of_division)
    if value[len(values_to_multiply)] != digit_value:
        return False
    return True


def _calculate_rest_of_division(list_of_multiplies_values: list) -> int:
    module = sum(list_of_multiplies_values) % _required_divider
    return module


def _cnpj_size_is_valid(value: str) -> bool:
    cnpj_size = 14
    if not value.isdigit() or len(value) != cnpj_size or len(set(value)) == 1:
        return False
    return True


def _verify_digit_value(rest_of_division) -> int:
    return 0 if rest_of_division < 2 else _required_divider - rest_of_division
