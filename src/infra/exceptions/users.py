from infra.exceptions.base import RepositoryException


class UserNotFoundDBException(RepositoryException):
    def __init__(self, user_id: str | None = None, user_email: str | None = None):
        self.user_id = user_id
        self.user_email = user_email

    @property
    def message(self):
        if self.user_id:
            return f"Пользователь с ID {self.user_id} не найден!"
        if self.user_email:
            return f"Пользователь с email {self.user_email} не найден!"
        return f"Пользователь не найден!"


class UserAlreadyExistsDBException(RepositoryException):
    def __init__(self, user_email: str):
        self.user_email = user_email

    @property
    def message(self):
        return f"Пользователь с email {self.user_email} уже существует!"
