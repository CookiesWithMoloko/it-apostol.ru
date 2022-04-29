class AuthorizationException(Exception):
    pass

class PermissionDeniedException(AuthorizationException):
    def __init__(self, permission: str):
        self.permission = permission

class AuthorizationRequiredException(AuthorizationException):
    pass

class InvalidPasswordException(AuthorizationException):
    pass

class EmailNotFoundException(AuthorizationException):
    pass
