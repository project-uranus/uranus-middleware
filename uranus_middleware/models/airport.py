from dataclasses import dataclass
from functools import reduce

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


airports = reduce(lambda cur, next: {**cur, next['iata']: next}, Airport.find(), {})  # dict


def get_airport_with_pos(iata: str) -> dict:
    found = airports.get(iata, {})
    return {
        'position': found.get('position'),
        'position_code': found.get('position_code')
    }


def get_airport_detail(iata: str) -> dict:
    found = airports.get(iata, {})
    return {
        'name': found.get('name'),
        'IATA': iata,
        'latitude': found.get('latitude'),
        'longitude': found.get('longitude')
    }
