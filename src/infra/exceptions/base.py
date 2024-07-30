from dataclasses import dataclass

from core.exceptions import ApplicationException


@dataclass
class RepositoryException(ApplicationException):
    @property
    def message(self):
        return "Произошла ошибка при записи или получении данных"
