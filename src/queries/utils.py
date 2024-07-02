import enum


class OrderBy(str, enum.Enum):
    ASC = "По возрастанию"
    DESC = "По убыванию"
    NO = "Отсутствует"


class FilterBySalary(str, enum.Enum):
    MIN = 'Минимальная зарплата'
    MAX = 'Максимальная зарплата'
    NO = 'Отсутствует'


class FilterByActiveness(str, enum.Enum):
    YES = 'Есть'
    NO = 'Отсутствует'



