from perms.pwd_manager import PasswordManager
from hashlib import sha256
from string import ascii_letters
from random import choice
class Sha256WSManager(PasswordManager):
    STATIC_SALT: str = 'Sha256WS'
    @staticmethod
    def hash_password_salt(pwd: str, salt: str) -> str:
        return sha256((salt + pwd + Sha256WSManager.STATIC_SALT).encode()).hexdigest()
    @staticmethod
    def hash_password(pwd: str) -> str:
        salt: str = ''.join(choice(list(ascii_letters)) for _ in range(16))
        return '$SHA$%s$%s' % (
            salt,
            Sha256WSManager.hash_password_salt(pwd, salt)
        )
    @staticmethod
    def check_hash(pwd: str, pwd_hash: str) -> bool:
        _, salt, pwd_hash = pwd_hash.split('$')
        return pwd_hash == Sha256WSManager.hash_password_salt(pwd, salt)

