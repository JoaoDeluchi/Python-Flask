from app.exceptions import BadRequestException, ConflictException, AlreadyInDbException, UnprocessableException


class NullValueException(BadRequestException):
    def __init__(self, msg):
        super().__init__(msg=msg)
        self.code = 400


class ProductFieldInvalidException(AlreadyInDbException):
    def __init__(self, description, code):
        super().__init__(msg=self.description)
        self.description = description
        self.code = code

    def serialize(self):
        return {'error': self.description, 'code': self.code}


class ProductDoNotExistException(BadRequestException):
    def __init__(self, msg: str):
        super().__init__(msg=msg)
        self.code = 404


class ProductInactiveException(BadRequestException):
    def __init__(self, msg: str = 'Unable to update an inactive product'):
        super().__init__(msg=msg)
        self.code = 403


class NoDataToExportException(UnprocessableException):
    def __init__(self, msg: str = 'No data to export'):
        super().__init__(msg=msg)
