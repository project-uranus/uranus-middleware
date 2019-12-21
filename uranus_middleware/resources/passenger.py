import csv
from io import StringIO

from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import admin_required
from uranus_middleware.models.boarding_pass import Pass as PassModel
from uranus_middleware.models.flight import Flight as FlightModel
from uranus_middleware.models.passenger import Passenger as PassengerModel
from uranus_middleware.models.user import User as UserModel

import werkzeug

passenger_blueprint = Blueprint('passenger', __name__)
passenger_api = Api(passenger_blueprint)


class Passenger(Resource):

    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
        data = parser.parse_args()
        file_storage = data['file']
        string_io = StringIO(file_storage.read().decode('utf-8'))  # convert binary I/O to text I/O
        reader = csv.DictReader(string_io)
        for row in reader:
            # create user if not exists
            name = row['name']
            first_name = row['first_name']
            last_name = row['last_name']
            email = row['email']
            flight_number = row['flight_number']
            date_of_flight = row['date_of_flight']
            id_number = row['id_number']
            seat = row['seat']
            compartment_code = row['compartment_code']
            found_user = UserModel.find({'User.id_number': id_number})
            if len(found_user) == 0:
                user = UserModel(name, first_name, last_name, id_number[-6:], id_number, email, 'passenger')
                user = user.save()
            else:
                user = found_user[0]
            # create passenger if not exists
            found_flight = FlightModel.find({'Flight.flight_number': flight_number, 'Flight.date_of_flight': date_of_flight})[0]
            found_passenger = PassengerModel.find({'Passenger.flight.id': found_flight['id']})
            if len(found_passenger) == 0:
                passenger = PassengerModel({'id': user['id']}, {'id': found_flight['id']}, seat)
                passenger = passenger.save()
            else:
                passenger = found_passenger[0]
            # create boarding pass
            boarding_pass = PassModel(
                {'id': passenger['id']},
                name,
                found_flight['origin_airport'],
                found_flight['destination_airport'],
                found_flight['flight_number'][:2],
                found_flight['flight_number'][2:],
                date_of_flight,
                compartment_code,
                seat,
                0  # Ticket issuance/passenger not checked in
            )
            boarding_pass.save()
        return {
            'message': 'ok'
        }

    @admin_required
    def get(self):
        return PassengerModel.find()


passenger_api.add_resource(Passenger, '/passengers')
