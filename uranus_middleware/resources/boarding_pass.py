from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import passenger_required, staff_required, get_user_id
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
        print(f'flight id: {data["flight_id"]}')
        found_boarding_pass = BoardingPassModel.find({'Pass.passenger.flight.id': data['flight_id']})
        if len(found_boarding_pass) == 0:
            return {
                'message': 'not found'
            }, 404
        found_boarding_pass = list(filter(lambda x: x.get('passenger', {}).get('user', {}).get('id', 0) == get_user_id(), found_boarding_pass))
        print(f'length of found pass: {len(found_boarding_pass)}')
        boarding_pass = found_boarding_pass[0]
        # encode boarding pass
        passenger_id = boarding_pass.get('passenger', {}).get('id', 'none')
        print(f'returning token: M1ZHOU/XIN MR          1A11A1 BNESYDQF 551  107Y26J 37    00>{passenger_id}')
        return {
            'token': f'M1ZHOU/XIN MR          1A11A1 BNESYDQF 551  107Y26J 37    00>{passenger_id}'
        }

    @staff_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('passenger_status', required=True)
        parser.add_argument('passenger_id', required=True)
        # parser.add_argument('flight_id', required=True)
        data = parser.parse_args()
        found_boarding_pass = BoardingPassModel.find({'Pass.passenger.id': data['passenger_id']})
        if len(found_boarding_pass) == 0:
            return {
                'message': 'not found'
            }, 404
        boarding_pass = found_boarding_pass[0]
        print(f'found pass for {data["passenger_id"]}')
        BoardingPassModel.update(boarding_pass.get('id'), {'passenger_status': int(data['passenger_status'])})
        if int(data['passenger_status']) == PassengerStatus.BOARDING_DATA_REVALIDATION_DONE.value:
            user_id = boarding_pass.get('passenger', {}).get('user', {}).get('id', 0)
            message = {
                'type': 'notification',
                'message': {
                    'title': 'Boarding data revalidation done',
                    'body': 'Wish you a good trip :)'
                }
            }
            print('notifying success')
            print(f'user id: {user_id}')
            notification.notify(user_id, message)
        return {
            'token': 'M1DESMARAIS/LUC       EABC123 YULFRAAC 0834 226F001A0025 100'
        }


boarding_pass_api.add_resource(BoardingPass, '/boardingPass')
