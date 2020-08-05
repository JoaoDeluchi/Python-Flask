from app.exceptions import BadRequestException, ConflictException, NotFoundException


class NullOrNoneValueException(BadRequestException):
    def __init__(self, msg: str = 'value cant be null'):
        super().__init__(msg=msg)
        self.code = 400

class AlreadyExistsException(ConflictException):
    def __init__(self, msg : str = 'Name already exists in Database'):
        super().__init__(msg=msg)
        self.code = 409

class ErrorCategory():
    def __init__(self,name):
        self.name = name
    def serialize(self):
        return {'Error':'Category {} already exists in Database'.format(self.name)}

class CategoryInactiveException(BadRequestException):
    def __init__(self, msg: str = 'Unable to update an inactive category'):
        super().__init__(msg=msg)
        self.code = 403

class CategoryDoNotExistException(NotFoundException):
    def __init__(self, msg: str = 'Category do not exist'):
        super().__init__(msg=msg)
        self.code = 404