from abc import ABC, abstractmethod


class ISQLAlchemy(ABC):

    @abstractmethod
    def Session(self):  # noqa
        raise NotImplementedError

    @abstractmethod
    def get_db(self):
        raise NotImplementedError

    @abstractmethod
    def _build_engine(self):
        raise NotImplementedError
