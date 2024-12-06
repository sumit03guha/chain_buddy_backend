from werkzeug.exceptions import HTTPException


class BaseExceptionClass(HTTPException):
    code: int
    description: str
