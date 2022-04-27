from __future__ import annotations
from typing import Optional, List, Callable
from flask import request
import functools
from flask import abort
from models import User
from perms import PermissionManager

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
            error: Optional[Callable] = None,
            error_code: int = 401):
        def r(f: Callable):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                user = AuthUser.get_user()
                if not user.is_authorized():
                    if error is None:
                        return abort(error_code)
                    return error("Not Authorized", False)
                for i in permissions:
                    if not user.perm.has_permission(i):
                        if error is None:
                            return abort(error_code)
                        return error("Dont have '%s' permission" % i, True)
                f(*args, **kwargs)
            return wrapper
        return r



