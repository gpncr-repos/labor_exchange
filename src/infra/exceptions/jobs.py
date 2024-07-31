from dataclasses import dataclass

from infra.exceptions.base import RepositoryException


@dataclass
class JobNotFoundDBException(RepositoryException):
    job_id: str

    @property
    def message(self):
        return f"Вакансия с id {self.job_id} не найденa!"
