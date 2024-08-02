from core.exceptions import ApplicationException


class RepositoryException(ApplicationException):
    @property
    def message(self):
        return "Произошла ошибка при записи или получении данных"
