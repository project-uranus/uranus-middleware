from dataclasses import dataclass

from uranus_middleware.models.model import Model


@dataclass
class Passenger(Model):
    user: dict  # composed
    flight: dict  # composed
    seat: str

    __slots__ = ('user', 'flight', 'seat')
