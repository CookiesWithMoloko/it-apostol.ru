from models import User
from perms.group import PermissionGroup
from perms import PermissionValidator
from app import db

class PermissionUser(PermissionValidator):
    def __init__(self, user: User):
        self.user: User = user
        self.group: PermissionGroup = PermissionGroup(user.group)

    def has_permission(self, perm: str):
        t = self.group.has_permission(perm)
        for i in list(self.user.permissions):
            r = self.check_mask(perm, i)
            if r is not None:
                t = r
        return t

    def add_permission(self, perm: str) -> None:
        if perm not in list(self.user.permissions):
            self.user.permissions += [perm]
            db.session.commit()

    def take_permission(self, perm: str) -> None:
        self.user.permissions = list(filter(
            lambda a: a != perm,
            list(self.user.permissions)
        ))
        db.session.commit()


