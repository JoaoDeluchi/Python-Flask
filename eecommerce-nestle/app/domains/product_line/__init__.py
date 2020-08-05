from app.exceptions import BadRequestException


class NullValueException(BadRequestException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class ProductLineDoNotExistException(BadRequestException):
    def __init__(self, msg: str = 'Product line do not exist'):
        super().__init__(msg=msg)
        self.code = 404

class ProductLineInactiveException(BadRequestException):
    def __init__(self, msg: str = 'Unable to update an inactive product line'):
        super().__init__(msg=msg)
        self.code = 403
