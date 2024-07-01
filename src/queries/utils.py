import enum


class OrderBy(str, enum.Enum):
    ASC = 1
    DESC = 2

class IdentifiedUser(str, enum.Enum):
    COM = 1
    PER = 2