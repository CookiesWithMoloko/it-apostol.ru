from typing import Optional

from models import Group
from perms import PermissionValidator

from app import db

class PermissionGroup(PermissionValidator):
    def __init__(self, group: Group):
        self.group: Group = group

    def has_permission(self, permission: str) -> Optional[bool]:
        if self.group is None:
            return
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
        if self.group is None:
            return
        list(self.group.permissions).append(perm)
        db.session.commit()

    def take_permission(self, perm: str) -> None:
        if self.group is None:
            return
        self.group.permissions = list(filter(
            lambda a: a != perm,
            list(self.group.permissions)
        ))
        db.session.commit()
