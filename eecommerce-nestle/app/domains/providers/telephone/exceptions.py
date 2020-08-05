from app.exceptions import UnprocessableException


class InvalidTelephoneException(UnprocessableException):
    def __init__(self, msg: str = 'This telephone is invalid!'):
        super().__init__(msg=msg)


class InvalidSizeTelephoneException(UnprocessableException):
    def __init__(self, msg: str = 'The size of telephone is invalid!'):
        super().__init__(msg=msg)