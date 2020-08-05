from app.exceptions import UnprocessableException


class EmailNotValidException(UnprocessableException):
    def __init__(self, msg: str = 'invalid email'):
        super().__init__(msg=msg)



