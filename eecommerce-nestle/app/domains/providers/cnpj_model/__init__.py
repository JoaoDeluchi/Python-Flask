from app.exceptions import UnprocessableException


class InvalidCnpjException(UnprocessableException):
    def __init__(self, msg: str = 'Invalid CNPJ'):
        super().__init__(msg=msg)
        self.code = 400