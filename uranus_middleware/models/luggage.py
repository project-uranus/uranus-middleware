from dataclasses import dataclass

from uranus_middleware.models.model import Model


@dataclass
class Luggage(Model):
    passenger: dict
    weight: float
    status: str

    __slots__ = ('passenger_id', 'weight', 'status')
