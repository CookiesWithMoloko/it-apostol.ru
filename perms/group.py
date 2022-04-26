from typing import Optional

from models import Group
from perms import PermissionValidator

from app import db

class PermissionGroup(PermissionValidator):
    def __init__(self, group: Group):
        self.group: Group = group

    def has_permission(self, permission: str) -> Optional[bool]:
        t = None
        for i in list(self.group.inheritance):
            r = PermissionGroup(Group.query.filter_by(id=i).first())
            if r is not None:
                t = r

        for i in list(self.group.permissions):
            r = self.check_mask(permission, i)
            if r is not None:
                t = r
        return t
    def add_permission(self, perm: str) -> None:
        list(self.group.permissions).append(perm)
        db.session.commit()

    def take_permission(self, perm: str) -> None:
        self.group.permissions = list(filter(
            lambda a: a != perm,
            list(self.group.permissions)
        ))
        db.session.commit()
