from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import get_user_id, roles_required, security_required, staff_required
from uranus_middleware.endpoints.notification import notification
from uranus_middleware.endpoints.security import security
from uranus_middleware.models.boarding_pass import Pass as BoardingPassModel
from uranus_middleware.models.counter_service import counter_service
from uranus_middleware.models.luggage import Luggage as LuggageModel, LuggageStatus
from uranus_middleware.models.passenger import PassengerStatus
from uranus_middleware.models.user import Role, filter_information

luggage_blueprint = Blueprint('luggage', __name__)
luggage_api = Api(luggage_blueprint)


class Luggage(Resource):
    @roles_required((Role.STAFF, Role.PASSENGER, Role.SECURITY))
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=False)
        data = parser.parse_args()
        if data['id']:
            return {
                'value':
                LuggageModel.find({'Luggage.passenger.id': data['id']})
            }
        return {'value': LuggageModel.find()}, 404

    @staff_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('weight', type=float, required=True)
        parser.add_argument('passenger_id', required=True)
        data = parser.parse_args()
        luggage = LuggageModel({'id': data['passenger_id']}, data['weight'],
                               LuggageStatus.NOT_CHECKED.value)
        saved = luggage.save()
        # push to security (broadcast?)
        ws_data = {
            'type': 'luggage',
            'message': {
                'information':
                filter_information(saved.get('passenger', {}).get('user', {})),
                'luggages':
                saved.get('id')
            }
        }
        security.broadcast(ws_data)
        # notify passenger
        notification.notify(
            saved.get('passenger', {}).get('user', {}).get('id'), {
                'type': 'notification',
                'message': {
                    'title': 'Passenger status changed',
                    'body': 'Check-in succeeded!'
                }
            })

        # remove from counter queue
        counter_service.length_sub(get_user_id())
        # update boarding pass status
        boarding_pass = BoardingPassModel.find(
            {'Pass.passenger.id': data['passenger_id']})[0]
        BoardingPassModel.update(
            boarding_pass.get('id'), {
                'passenger_status':
                PassengerStatus.TICKET_ISSUANCE_PASSENGER_CHECKED_IN.value
            })
        return {'message': 'ok'}

    @security_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('passed', type=bool, required=True)
        parser.add_argument('message', required=False)
        parser.add_argument('id', required=True)
        data = parser.parse_args()
        luggage_found = LuggageModel.find({'Luggage.id': data['id']})
        passed = data['passed']
        message = data['message']
        if len(luggage_found) == 0:
            return {'message': 'not found'}, 404
        luggage = luggage_found[0]
        # update luggage status
        LuggageModel.update(
            luggage.get('id'), {
                **luggage, 'status':
                LuggageStatus.CHECKED.value
                if passed else LuggageStatus.CHECK_FAILED.value
            })
        # update boarding pass status
        boarding_pass = BoardingPassModel.find(
            {'Pass.passenger.id': luggage.get('passenger', {}).get('id')})[0]
        BoardingPassModel.update(
            boarding_pass.get('id'), {
                'passenger_status':
                (PassengerStatus.BAG_CHECKED_PASSENGER_CHECKED_IN.value
                 if passed else
                 PassengerStatus.TICKET_ISSUANCE_PASSENGER_CHECKED_IN.value)
            })

        # notify passenger
        notify_msg = {
            'type': 'notification',
            'message': {
                'title':
                'Luggage status changed',
                'body':
                'Your luggage has passed the check!' if passed else
                f'Your luggage has failed the check, reason: {message}'
            }
        }
        notification.notify(
            luggage.get('passenger', {}).get('user', {}).get('id'), notify_msg)
        return {'message': 'ok'}


luggage_api.add_resource(Luggage, '/luggages')
