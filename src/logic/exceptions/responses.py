from logic.exceptions.base import ServiceException


class OnlyNotCompanyUsersCanMakeResponsesException(ServiceException):
    @property
    def message(self):
        return "Только пользователи не являющиеся компаниями могут делать отклик на вакансию"
