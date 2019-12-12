from flask import Blueprint

from flask_jwt_simple import create_jwt

from flask_restful import Api, Resource, reqparse

from uranus_middleware.models.user import User

auth_blueprint = Blueprint('auth', __name__)
auth_api = Api(auth_blueprint)


class Auth(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', required=True)
        parser.add_argument('email', required=True)
        data = parser.parse_args()
        email = data['email']
        password = data['password']
        users = User.find({'User.email': email})
        if len(users) == 0:
            return {
                'message': 'no user found'
            }, 400
        user = users[0]
        if User.verify_digest(password, user['password']):
            return {
                'token': create_jwt(user)
            }, 201
        return 'error', 400


auth_api.add_resource(Auth, '/auth')
