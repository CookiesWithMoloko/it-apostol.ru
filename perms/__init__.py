import re
from typing import Optional
from perms.user import PermissionUser
from models import User
class PermissionValidator:
    def check_mask(self, permission: str, pattern: str) -> bool:
        if pattern.startswith('-'):
            return not self.check_mask(permission, pattern[1:])
        return bool(re.match(
            pattern.replace('.', r'\.').replace('*', '[a-zA-Z0-9]+'),
            permission))

    def has_permission(self, permission: str) -> Optional[bool]:
        pass

class PermissionManager:
    def __init__(self):
        pass
    @staticmethod
    def get_user(id: int) -> PermissionUser:
        return PermissionUser(User.query.filter_by(id=id).first())
