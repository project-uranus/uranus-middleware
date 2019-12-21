from http import HTTPStatus

from flask import Blueprint

from flask_jwt_simple import jwt_required

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import admin_required, get_user_id
from uranus_middleware.error import error
from uranus_middleware.models.user import User as UserModel

user_blueprint = Blueprint('user', __name__)
user_api = Api(user_blueprint)


class User(Resource):
    @admin_required
    def get(self):
        return {
            'value': UserModel.find()
        }

    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False)
        parser.add_argument('first_name', required=False)
        parser.add_argument('last_name', required=False)
        parser.add_argument('email', required=False)
        parser.add_argument('id_number', required=False)
        data = parser.parse_args()
        user_id = get_user_id()
        return UserModel.update(user_id, data)


class UserPassword(Resource):
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', required=True)
        data = parser.parse_args()
        data['password'] = UserModel.generate_digest(data['password'])
        user_id = get_user_id()
        return UserModel.update(user_id, data) or error(HTTPStatus.NOT_FOUND)


user_api.add_resource(User, '/users')
user_api.add_resource(UserPassword, '/users/password')
