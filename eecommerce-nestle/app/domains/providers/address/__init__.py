from app.exceptions import BadRequestException


class NullOrNoneValueException(BadRequestException):
    def __init__(self, msg: str = 'value null or invalid'):
        super().__init__(msg=msg)
        self.code = 400