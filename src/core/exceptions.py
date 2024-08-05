class ApplicationException(Exception):
    @property
    def message(self):
        return "Произошла ошибка приложения"
