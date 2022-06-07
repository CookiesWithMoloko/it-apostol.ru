class TextException(Exception):
    def __init__(self, text: str):
        self.text = text
    def __str__(self):
        return self.text

class AuthorizationException(Exception):
    pass

class PermissionDeniedException(AuthorizationException):
    def __init__(self, permission: str):
        self.permission = permission
    def __str__(self):
        return f'Permission denied. ({self.permission})'

class AuthorizationRequiredException(AuthorizationException):
    pass

class InvalidPasswordException(AuthorizationException):
    pass

class EmailNotFoundException(AuthorizationException):
    pass

class InvalidArgumentException(AuthorizationException):
    def __init__(self, name: str):
        self.argument_name = name
class MissedArgumentException(InvalidArgumentException):
    def __init__(self, name: str):
        super().__init__(name)
    def __str__(self):
        return f'Missed <{self.argument_name}> argument'
class InvalidArgumentTypeException(InvalidArgumentException):
    def __init__(self, name: str, argument_type):
        super().__init__(name)
        self.argument_type = argument_type
    def __str__(self):
        return f'Argument {self.argument_name} must be of type {self.argument_type.name}'
