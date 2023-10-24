class UserPermissionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InteractionWithInactiveObject(Exception):
    def __init__(self, message):
        super().__init__(message)
