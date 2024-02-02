import dataclasses
from typing import Protocol, Any


class Command(Protocol):
    """Абстрактный класс для результатов запросов"""
    def __dict__(self):
        return self.__dict__

@dataclasses.dataclass
class CommandResult(Command):
    result: Any = None
    errors: list[Any] = dataclasses.field(default_factory=list)

    @classmethod
    def success(cls, result: Any):
        """Результат запроса получен"""
        return cls(result=result)

    @classmethod
    def fail(cls, message="Failure", exception=None):
        """Результат запроса НЕ получен"""
        error_message = [(message, exception)]
        return cls(errors=error_message)
