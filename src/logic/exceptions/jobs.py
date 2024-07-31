from dataclasses import dataclass

from logic.exceptions.base import ServiceException


@dataclass
class JobNotFoundException(ServiceException):
    job_id: str

    @property
    def message(self):
        return f"Вакансия с id {self.job_id} не найденa!"


@dataclass
class OnlyCompanyCanCreateJobException(ServiceException):
    @property
    def message(self):
        return f"Создать вакансию может только компания"
