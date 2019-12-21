from dataclasses import dataclass

from uranus_middleware.models.model import Model


@dataclass
class Pass(Model):
    passenger: dict
    passenger_name: str
    from_city_airport_code: str
    to_city_airport_code: str
    operating_carrier_designator: str
    flight_number: str
    date_of_flight: str
    compartment_code: str
    seat_number: str
    passenger_status: int

    __fixed_fields = {
        'format_code': 'M',
        'number_of_legs_encoded': '1',
        'electronic_ticket_indicator': 'E',
        'field_size_of_variable_size_field': '00'
    }

    __slots__ = (
        'passenger',
        'passenger_name',
        'from_city_airport_code',
        'to_city_airport_code',
        'operating_carrier_designator',
        'flight_number',
        'date_of_flight',
        'compartment_code',
        'seat_number',
        'passenger_status'
    )

    # return a dict with fixed fields
    def build(self) -> dict:
        return {**self._as_dict(), **self.__fixed_fields}
