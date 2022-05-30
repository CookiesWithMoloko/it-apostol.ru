from __future__ import annotations

import datetime
from typing import Optional, List, Callable
from flask import request
import functools
from random import choice
from string import ascii_letters
from flask import abort
from hashlib import md5
from perms.exc import *
from models import User
from perms import PermissionManager
from perms.user import PermissionUser
from perms.pwd_manager import PasswordManager
from perms.md5_pwd import Md5Manager
from app import db


class AuthUser:
    password_manager: PasswordManager = Md5Manager()

    def __init__(self, token: str) -> None:
        self.user: User = User.query.filter_by(token=token).first()
        self.perm: Optional[PermissionUser] = None
        if self.user is not None:
            self.perm = PermissionManager.get_user(self.user.id)

    def is_authorized(self) -> bool:
        return self.user is not None

    def has_permission(self, perm: str) -> Optional[bool]:
        if self.user is None:
            return False
        return self.perm.has_permission(perm)

    @staticmethod
    def register(email: str, password: str, display_name=None) -> bool:
        if display_name is None:
            display_name = email
        u = User(
            email=email,
            password=AuthUser.password_manager.hash_password(password),
            display_name=display_name,
            token=email
        )
        try:
            db.session.add(u)
            db.session.commit()
        except:
            db.session.rollback()
            return False
        return True

    @staticmethod
    def get_user() -> AuthUser:
        token = request.cookies.get('token', None, str)
        return AuthUser(token)

    @staticmethod
    def hash_password(pwd: str) -> str:
        return AuthUser.password_manager.hash_password(pwd)

    @staticmethod
    def check_password(pwd: str, pwd_hash: str) -> bool:
        return AuthUser.password_manager.check_hash(pwd, pwd_hash)

    @staticmethod
    def generate_token(user: User) -> str:
        return '%s:%s' % (
            md5(str(user.id).encode()).hexdigest(),
            ''.join(choice(list(ascii_letters)) for _ in range(64))
        )

    @staticmethod
    def auth_user(email: str, password: str) -> str | InvalidPasswordException | EmailNotFoundException:
        """

        :param email:
        :param password:
        :return: token
        """
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise EmailNotFoundException()
        if not AuthUser.password_manager.check_hash(password, user.password):
            raise InvalidPasswordException()
        token: str = AuthUser.generate_token(user)
        user.token = token
        user.ip = str(request.remote_addr)
        user.auth_date = datetime.datetime.now()
        db.session.commit()
        return token

    @staticmethod
    def auth_required(
            permissions: List[str] = [],
            on_error: Optional[Callable[[AuthorizationException], None]] = None,
            permission_error_code: int = 403,
            authorization_error_code: int = 401):
        def r(f: Callable):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                user = AuthUser.get_user()
                if not user.is_authorized():
                    if on_error is None:
                        return abort(authorization_error_code)
                    return on_error(AuthorizationRequiredException())
                for i in permissions:
                    if not user.perm.has_permission(i):
                        if on_error is None:
                            return abort(permission_error_code)
                        return on_error(PermissionDeniedException(i))
                return f(*args, **kwargs)

            return wrapper

        return r
