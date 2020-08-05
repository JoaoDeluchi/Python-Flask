from app.exceptions import BadRequestException


class NullOrNoneValueException(BadRequestException):
    def __init__(self, msg: str = 'value cant be null'):
        super().__init__(msg=msg)
        self.code = 400


class ProviderDoNotExistException(BadRequestException):
    def __init__(self, msg: str = 'Provider do not exist'):
        super().__init__(msg=msg)
        self.code = 404


class ProviderInactiveException(BadRequestException):
    def __init__(self, msg: str = 'Unable to update an inactive provider'):
        super().__init__(msg=msg)
        self.code = 403
