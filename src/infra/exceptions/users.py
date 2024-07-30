from dataclasses import dataclass

from infra.exceptions.base import RepositoryException


@dataclass
class UserNotFoundDBException(RepositoryException):
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
class UserAlreadyExistsDBException(RepositoryException):
    user_email: str

    @property
    def message(self):
        return f"Пользователь с email {self.user_email} уже существует!"
