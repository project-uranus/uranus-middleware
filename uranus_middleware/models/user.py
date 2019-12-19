from dataclasses import dataclass
from hashlib import md5

from uranus_middleware.models.model import Model


@dataclass
class User(Model):
    name: str
    password: str
    id_number: str
    email: str
    role: str

    __slots__ = ('name', 'password', 'id_number', 'email', 'role')

    def __post_init__(self):
        self.password = md5(self.password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_digest(password: str, digest: str) -> bool:
        return md5(password.encode('utf-8')).hexdigest() == digest
