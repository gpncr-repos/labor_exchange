from dataclasses import dataclass

from core.exceptions import ApplicationException


@dataclass
class ServiceException(ApplicationException):
    @property
    def message(self):
        return "Произошла ошибка при обработке данных"
