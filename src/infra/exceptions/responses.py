from infra.exceptions.base import RepositoryException


class ResponseNotFoundDBException(RepositoryException):
    def __init__(self, response_id: str):
        self.response_id = response_id

    @property
    def message(self):
        return f"Отклик с id {self.response_id} не найден!"
