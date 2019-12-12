from hashlib import md5

from uranus_middleware.models.model import Model


class User(Model):
    __slots__ = ('name', 'password', 'id_number', 'email', 'role')

    @staticmethod
    def verify_digest(password: str, digest: str) -> bool:
        return md5(password.encode('utf-8')).hexdigest() == digest

    def __init__(self, name, password, id_number, email, role):
        self.name = name
        self.password = md5(password.encode('utf-8')).hexdigest()
        self.id_number = id_number
        self.email = email
        self.role = role
