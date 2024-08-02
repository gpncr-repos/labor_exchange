from logic.exceptions.base import ServiceException


class JobNotFoundException(ServiceException):
    def __init__(self, job_id: str):
        self.job_id = job_id

    @property
    def message(self):
        return f"Вакансия с id {self.job_id} не найденa!"


class OnlyCompanyCanCreateJobException(ServiceException):
    @property
    def message(self):
        return f"Создать вакансию может только компания"
