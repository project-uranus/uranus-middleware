from http import HTTPStatus

from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import admin_required, passenger_required
from uranus_middleware.error import error
from uranus_middleware.models.flight import Flight as FlightModel, FlightStatus

flight_blueprint = Blueprint('flights', __name__)
flight_api = Api(flight_blueprint)


class Flight(Resource):

    @passenger_required
    def get(self, id=None):
        if id:
            found = FlightModel.find({'Flight.id': id})
            return {
                'value': {} if len(found) == 0 else found[0]
            }
        else:
            return {
                'value': FlightModel.find()
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
