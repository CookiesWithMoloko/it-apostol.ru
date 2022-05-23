from abc import abstractmethod

class PasswordManager:
    @staticmethod
    @abstractmethod
    def hash_password(pwd: str) -> str:
        """

        :param pwd: Password
        :return: Password hash
        """
        return
    @staticmethod
    @abstractmethod
    def check_hash(pwd: str, pwd_hash: str) -> bool:
        """

        :param pwd: Password
        :param pwd_hash: Password hash
        :return: Matches the password to the given hash
        """
        return