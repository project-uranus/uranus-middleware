from dataclasses import dataclass

from uranus_middleware.models.model import Model


@dataclass
class Airport(Model):
    name: str
    iata: str
    position: str
    position_code: str
    latitude: str
    longitude: str

    __slots__ = ('name', 'iata', 'position', 'position_code', 'latitude', 'longitude')
