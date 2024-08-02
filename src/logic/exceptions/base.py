from core.exceptions import ApplicationException


class ServiceException(ApplicationException):
    @property
    def message(self):
        return "Произошла ошибка при обработке данных"
