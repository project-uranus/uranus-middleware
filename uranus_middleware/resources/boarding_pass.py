from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import passenger_required, staff_required
from uranus_middleware.endpoints.notification import notification
from uranus_middleware.models.boarding_pass import Pass as BoardingPassModel
from uranus_middleware.models.passenger import PassengerStatus


boarding_pass_blueprint = Blueprint('boardingPass', __name__)
boarding_pass_api = Api(boarding_pass_blueprint)


class BoardingPass(Resource):

    @passenger_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('flight_id', required=True)
        data = parser.parse_args()
        found_boarding_pass = BoardingPassModel.find({'Pass.passenger.flight.id': data['flight_id']})
        if len(found_boarding_pass) == 0:
            return {
                'message': 'not found'
            }, 404
        boarding_pass = found_boarding_pass[0]
        # encode boarding pass
        return {
            'token': 'M1EWING/SHAUN MR       1A11A1 BNESYDQF 551  107Y26J 37    00'
        }

    @staff_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('passenger_status', required=True)
        parser.add_argument('flight_id', required=True)
        data = parser.parse_args()
        boarding_pass = BoardingPassModel.find({'Pass.passenger.flight.id': data['flight_id']})[0]
        BoardingPassModel.update(boarding_pass.get('id'), {'passenger_status': int(data['passenger_status'])})
        if data['passenger_status'] == PassengerStatus.BOARDING_DATA_REVALIDATION_DONE.value:
            notification.notify(int(data['passenger_id']), 'Boarding data revalidation done, wish you a good trip :)')
        return {
            'token': 'M1DESMARAIS/LUC       EABC123 YULFRAAC 0834 226F001A0025 100'
        }


boarding_pass_api.add_resource(BoardingPass, '/boardingPass')
