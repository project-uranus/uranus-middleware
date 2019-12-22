from dataclasses import dataclass
from enum import Enum

from uranus_middleware.models.model import Model


class PassengerStatus(Enum):
    TICKET_ISSUANCE_PASSENGER_NOT_CHECKED_IN = 0
    TICKET_ISSUANCE_PASSENGER_CHECKED_IN = 1
    BAG_CHECKED_PASSENGER_NOT_CHECKED_IN = 2
    BAG_CHECKED_PASSENGER_CHECKED_IN = 3
    STANDBY = 7
    BOARDING_DATA_REVALIDATION_DONE = 8


@dataclass
class Passenger(Model):
    user: dict  # composed
    flight: dict  # composed
    seat: str

    __slots__ = ('user', 'flight', 'seat')


def filter_passenger_info(passenger: dict) -> dict:
    user = passenger.get('user', {})
    return {
        'id': passenger.get('id'),
        'seat': passenger.get('seat'),
        'name': user.get('name'),
        'email': user.get('email'),
        'id_number': user.get('id_number'),
        'first_name': user.get('first_name'),
        'last_name': user.get('last_name')
    }
