from dataclasses import dataclass

from uranus_middleware.models.model import Model


@dataclass
class Passenger(Model):
    user: dict  # composed
    flight: dict  # composed
    boarding_pass: int
    luggage: int
    seat: str

    __slots__ = ('user', 'flight', 'boarding_pass', 'luggage', 'seat')
