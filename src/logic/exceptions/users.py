from logic.exceptions.base import ServiceException


class UpdateOtherUserException(ServiceException):
    def __init__(self, user_email: str):
        self.user_email = user_email

    @property
    def message(self):
        return f"Невозможно изменить чужого пользователя с email {self.user_email}!"
