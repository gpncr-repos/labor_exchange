from logic.exceptions.base import ServiceException


class OnlyNotCompanyUsersCanMakeResponsesException(ServiceException):
    @property
    def message(self):
        return "Только пользователи не являющиеся компаниями могут делать отклик на вакансию"


class ResponseDeleteLogicException(ServiceException):
    @property
    def message(self):
        return "Удалить отклик может только пользователь, сделавший его, либо компания, на чью вакансию сделан отклик"


class OnlyCompanyCanGetJobResponses:
    @property
    def message(self):
        return "Только пользователь-компания может просматривать все отклики на вакансию"


class OnlyJobOwnerCanGetJobResponsesException:
    @property
    def message(self):
        return "Просматривать отклики на вакансию может только компания, разместившая вакансию!"
