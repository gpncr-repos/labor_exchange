from src.logic.exceptions.base import ServiceException


class InvalidTokenException(ServiceException):
    @property
    def message(self):
        return f"Невалидный токен!"


class InvalidTokenTypeException(ServiceException):
    def __init__(self, token_type: str):
        self.token_type = token_type

    @property
    def message(self):
        return f"Неверный тип токена, ожидается {self.token_type!r}"


class WrongCredentialsException(ServiceException):

    @property
    def message(self):
        return f"Неверные имя пользователя или пароль!"
