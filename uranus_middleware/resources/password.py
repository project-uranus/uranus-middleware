from http import HTTPStatus

from flask import Blueprint

from flask_jwt_simple import jwt_required

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import get_user_id
from uranus_middleware.error import error
from uranus_middleware.models.user import User as UserModel

password_blueprint = Blueprint('password', __name__)
password_api = Api(password_blueprint)


class Password(Resource):
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', required=True)
        data = parser.parse_args()
        data['password'] = UserModel.generate_digest(data['password'])
        user_id = get_user_id()
        return UserModel.update(user_id, data) or error(HTTPStatus.NOT_FOUND)


password_api.add_resource(Password, '/password')
