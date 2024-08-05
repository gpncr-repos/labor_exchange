from logic.exceptions.base import ServiceException


class OnlyCompanyCanCreateJobException(ServiceException):
    @property
    def message(self):
        return f"Создать вакансию может только компания"


class OnlyCompanyCanDeleteJobException(ServiceException):
    @property
    def message(self):
        return f"Удалять вакансию может только пользователь-компания!"


class OnlyJobOwnerCanDeleteJobException(ServiceException):
    @property
    def message(self):
        return f"Удалять вакансию может только компания, разместившая вакансии!"
