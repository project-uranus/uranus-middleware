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
