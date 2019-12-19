from dataclasses import dataclass

from uranus_middleware.models.model import Model


class FlightStatus(object):
    scheduled = 'scheduled'
    delayed = 'delayed'
    boarding = 'boarding'
    departed = 'departed'
    arrived = 'arrived'
    cancelled = 'cancelled'
    no_takeoff_info = 'noTakeoffInfo'


@dataclass
class Flight(Model):
    airline: str
    flight_number: str
    aircraft: str
    date_of_flight: str
    departure_time: str
    arrival_time: str
    origin_airport: str
    destination_airport: str
    boarding_time: str
    boarding_gate: str
    status: str

    __slots__ = (
        'airline',
        'flight_number',
        'aircraft',
        'date_of_flight',
        'departure_time',
        'arrival_time',
        'origin_airport',
        'destination_airport',
        'boarding_time',
        'boarding_gate',
        'status'
    )
