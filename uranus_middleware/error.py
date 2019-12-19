from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class Error(object):
    code: str
    message: str


def error(status: HTTPStatus):
    return (Error(status.phrase, 'invalid token').__dict__, status)
