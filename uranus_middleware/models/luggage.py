from dataclasses import dataclass
from enum import Enum

from uranus_middleware.models.model import Model


class LuggageStatus(Enum):
    NOT_CHECKED = 'notChecked'
    CHECKED = 'checked'
    CHECK_FAILED = 'checkFailed'


@dataclass
class Luggage(Model):
    passenger: dict
    weight: float
    status: str

    __slots__ = ('passenger', 'weight', 'status')


def filter_luggage_information(luggage: dict) -> dict:
    return {
        'luggage_id': luggage.get('id'),
        'weight': luggage.get('weight'),
        'status': luggage.get('status')
    }
