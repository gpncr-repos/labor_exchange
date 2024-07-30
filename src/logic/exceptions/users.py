from dataclasses import dataclass

from logic.exceptions.base import ServiceException


@dataclass
class UserNotFoundException(ServiceException):
    user_id: str | None = None
    user_email: str | None = None

    @property
    def message(self):
        if self.user_id:
            return f"Пользователь с ID {self.user_id} не найден!"
        if self.user_email:
            return f"Пользователь с email {self.user_email} не найден!"
        return f"Пользователь не найден!"


@dataclass
class UserAlreadyExistsException(ServiceException):
    user_email: str

    @property
    def message(self):
        return f"Пользователь с email {self.user_email} уже существует!"


@dataclass
class UpdateOtherUserException(ServiceException):
    user_email: str

    @property
    def message(self):
        return f"Невозможно изменить чужого пользователя с email {self.user_email}!"


@dataclass
class WrongCredentialsException(ServiceException):

    @property
    def message(self):
        return f"Неверные имя пользователя или пароль!"
