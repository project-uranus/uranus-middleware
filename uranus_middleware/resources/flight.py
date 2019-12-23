from http import HTTPStatus

from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import admin_required, get_user_id, get_user_role, roles_required
from uranus_middleware.error import error
from uranus_middleware.models.airport import get_airport_detail, get_airport_with_pos
from uranus_middleware.models.boarding_pass import Pass as BoardingPassModel
from uranus_middleware.models.flight import Flight as FlightModel, FlightStatus
from uranus_middleware.models.luggage import Luggage as LuggageModel, filter_luggage_information
from uranus_middleware.models.passenger import Passenger as PassengerModel
from uranus_middleware.models.user import Role

flight_blueprint = Blueprint('flights', __name__)
flight_api = Api(flight_blueprint)


class Flight(Resource):

    @roles_required((Role.ADMINISTRATOR, Role.PASSENGER, Role.STAFF))
    def get(self, id=None):
        if id:
            # get flight detail
            found = BoardingPassModel.find({'Pass.passenger.flight.id': id})
            if len(found) == 0:
                return {
                    'value': {}
                }
            else:
                found_pass = found[0]
                found_flight = found[0].get('passenger', {}).get('flight')
                result = {
                    'value': {
                        'flight': {
                            **found_flight,
                            'origin_airport': get_airport_detail(found_flight.get('origin_airport')),
                            'destination_airport': get_airport_detail(found_flight.get('destination_airport'))
                        },
                        'spec': {
                            'compartment_code': found_pass.get('compartment_code'),
                            'seat_number': found_pass.get('seat_number')
                        }
                    }
                }
                if get_user_role() == Role.PASSENGER:
                    # we can get luggage only for passenger
                    user_id = get_user_id()
                    luggages = LuggageModel.find({'Luggage.passenger.user.id': user_id})
                    luggages = list(filter(lambda x: x.get('passenger', {}).get('flight', {}).get('id') == int(id), luggages))
                    luggages = [filter_luggage_information(luggage) for luggage in luggages]
                    result['value']['spec']['luggages'] = luggages
                return result
        else:
            # get flight list
            role = get_user_role()
            if role == Role.PASSENGER:
                passenger_found = PassengerModel.find({'Passenger.user.id': get_user_id()})
                flights = [passenger.get('flight') for passenger in passenger_found]
                flights = sorted(flights, key=lambda x: x.get('date_of_flight'), reverse=True)
            else:
                parser = reqparse.RequestParser()
                parser.add_argument('passenger_id', required=False)
                data = parser.parse_args()
                passenger_id = data['passenger_id']
                if passenger_id:
                    passenger_found = PassengerModel.find({'Passenger.id': passenger_id})
                    flights = [passenger.get('flight') for passenger in passenger_found]
                else:
                    flights = FlightModel.find()
            flights_extended = [{
                **flight,
                'origin_airport': get_airport_with_pos(flight.get('origin_airport')),
                'destination_airport': get_airport_with_pos(flight.get('destination_airport'))
            } for flight in flights]
            return {
                'value': flights_extended
            }

    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('airline', required=True)
        parser.add_argument('flight_number', required=True)
        parser.add_argument('aircraft', required=True)
        parser.add_argument('date_of_flight', required=True)
        parser.add_argument('departure_time', required=True)
        parser.add_argument('arrival_time', required=True)
        parser.add_argument('origin_airport', required=True)
        parser.add_argument('destination_airport', required=True)
        parser.add_argument('boarding_time', required=True)
        parser.add_argument('boarding_gate', required=True)
        data = parser.parse_args()
        flight = FlightModel(
            data['airline'],
            data['flight_number'],
            data['aircraft'],
            data['date_of_flight'],
            data['departure_time'],
            data['arrival_time'],
            data['origin_airport'],
            data['destination_airport'],
            data['boarding_time'],
            data['boarding_gate'],
            FlightStatus.scheduled
        )
        # check duplicates
        found = FlightModel.find({
            'Flight.flight_number': data['flight_number'],
            'Flight.date_of_flight': data['date_of_flight']
        })
        if len(found) > 0:
            return {
                'message': 'duplicated'
            }, 409
        flight.save()
        return {
            'message': 'ok'
        }

    @admin_required
    def put(self, id=None):
        if id:
            parser = reqparse.RequestParser()
            parser.add_argument('airline', required=False)
            parser.add_argument('flight_number', required=False)
            parser.add_argument('aircraft', required=False)
            parser.add_argument('date_of_flight', required=False)
            parser.add_argument('departure_time', required=False)
            parser.add_argument('arrival_time', required=False)
            parser.add_argument('origin_airport', required=False)
            parser.add_argument('destination_airport', required=False)
            parser.add_argument('boarding_time', required=False)
            parser.add_argument('boarding_gate', required=False)
            parser.add_argument('status', required=False)
            data = parser.parse_args()
            params = {k: v for k, v in data.items() if v is not None}
            updated = FlightModel.update(id, params)
            return updated or error(HTTPStatus.NOT_FOUND)
        return error(HTTPStatus.NOT_FOUND)


flight_api.add_resource(Flight, '/flights', '/flights/<string:id>')
