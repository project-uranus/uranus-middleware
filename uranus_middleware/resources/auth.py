from flask import Blueprint

from flask_jwt_simple import create_jwt

from flask_restful import Api, Resource, reqparse

from uranus_middleware.models.counter_service import counter_service
from uranus_middleware.models.user import Role, User

auth_blueprint = Blueprint('auth', __name__)
auth_api = Api(auth_blueprint)


class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', required=True)
        parser.add_argument('id_number', required=True)
        parser.add_argument('User-Agent', location='headers')
        data = parser.parse_args()
        id_number = data['id_number']
        password = data['password']
        users = User.find({'User.id_number': id_number})
        if len(users) == 0:
            return {'message': 'no user found'}, 400
        user = users[0]
        if User.verify_digest(password, user['password']):
            user_agent = data['User-Agent']
            if user['role'] == Role.STAFF.value:
                if not ('iPhone' in user_agent or 'iPad' in user_agent):
                    # counter
                    counter_id = counter_service.add(user['id'])
                    return {
                        'token': create_jwt(user),
                        'counter_id': counter_id
                    }
            return {'token': create_jwt(user)}, 201
        return {'message': 'invalid id number or password'}, 400


auth_api.add_resource(Auth, '/auth')
