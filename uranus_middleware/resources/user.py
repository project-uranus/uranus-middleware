from flask import Blueprint

from flask_jwt_simple import create_jwt

from flask_restful import Api, Resource, reqparse

from uranus_middleware.models.user import User as UserModel

user_blueprint = Blueprint('user', __name__)
user_api = Api(user_blueprint)


class User(Resource):
    def get(self):
        return UserModel.find(None)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('role', choices=('administrator', 'staff', 'passenger'), required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('id_number', required=True)
        data = parser.parse_args()
        # check if email duplicated
        users = UserModel.find({'User.email': data['email']})
        if len(users) > 0:
            return {
                'message': 'email duplicated'
            }, 400
        user = UserModel(data['name'], data['password'], data['id_number'], data['email'], data['role'])
        identity = user.save()
        return {
            'token': create_jwt(identity)
        }, 201


user_api.add_resource(User, '/user')
