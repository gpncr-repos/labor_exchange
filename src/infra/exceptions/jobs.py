from infra.exceptions.base import RepositoryException


class JobNotFoundDBException(RepositoryException):
    def __init__(self, job_id: str):
        self.job_id = job_id

    @property
    def message(self):
        return f"Вакансия с id {self.job_id} не найденa!"
