from dataclasses import dataclass
from enum import Enum
from hashlib import md5

from uranus_middleware.models.model import Model


class Role(Enum):
    ADMINISTRATOR = 'administrator'
    STAFF = 'staff'
    SECURITY = 'security'
    PASSENGER = 'passenger'


@dataclass
class User(Model):
    name: str
    first_name: str
    last_name: str
    password: str
    id_number: str
    email: str
    role: str

    __slots__ = ('name', 'first_name', 'last_name', 'password', 'id_number', 'email', 'role')

    def __post_init__(self):
        self.password = md5(self.password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_digest(password: str, digest: str) -> bool:
        return md5(password.encode('utf-8')).hexdigest() == digest

    @staticmethod
    def generate_digest(password: str) -> str:
        return md5(password.encode('utf-8')).hexdigest()


def filter_information(user: dict) -> dict:
    return {
        'email': user.get('email'),
        'name': user.get('name'),
        'first_name': user.get('first_name'),
        'last_name': user.get('last_name'),
        'id_number': user.get('id_number'),
    }
