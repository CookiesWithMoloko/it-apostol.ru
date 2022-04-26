from typing import Optional, List, Callable
from flask import request, session
from flask import abort
from models import User
from perms import PermissionManager
from __future__ import annotations
class AuthUser:
    def __init__(self, token: str) -> None:
        self.user = User.query.filter_by(token=token).first()
        if self.user is not None:
            self.perm = PermissionManager.get_user(self.user.id)

    def is_authorized(self) -> bool:
        return self.user is not None

    def has_permission(self, perm: str) -> Optional[bool]:
        if self.user is None:
            return False
        return self.perm.has_permission(perm)

    @staticmethod
    def get_user() -> AuthUser:
        token = request.cookies.get('token', None, str)
        return AuthUser(token)

    @staticmethod
    def auth_required(
            permissions: List[str] = [],
            error: Callable = None,
            error_code: int = 400):
        def r(f: Callable):
            def wrapper(*args, **kwargs):
                user = AuthUser.get_user()
                if not user.is_authorized():
                    if error is None:
                        return abort(error_code)
                    return error("Not Authorized")
                for i in permissions:
                    if not user.perm.has_permission(i):
                        if error is None:
                            return abort(error_code)
                        return error("Dont have '%s' permission" % i)
                f(*args, **kwargs)
            return wrapper



