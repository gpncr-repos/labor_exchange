import enum


class OrderBy(str, enum.Enum):
    ASC = 1
    DESC = 2


class FilterBy(str, enum.Enum):
    MIN = 'Минимальная зарплата'
    MAX = 'Максимальная зарплата'
