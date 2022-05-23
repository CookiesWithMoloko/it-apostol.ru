from perms.pwd_manager import PasswordManager
from hashlib import md5

class Md5Manager(PasswordManager):
    @staticmethod
    def hash_password(pwd: str) -> str:
        return md5(pwd.encode()).hexdigest()

    @staticmethod
    def check_hash(pwd: str, pwd_hash: str) -> bool:
        return Md5Manager.hash_password(pwd) == pwd_hash

