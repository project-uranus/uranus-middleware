from http import HTTPStatus

from flask import Blueprint

from flask_jwt_simple import jwt_required

from flask_restful import Api, Resource, reqparse

from uranus_middleware.auth_utils import get_user_id
from uranus_middleware.error import error
from uranus_middleware.models.user import User as UserModel

info_blueprint = Blueprint('information', __name__)
info_api = Api(info_blueprint)


class Information(Resource):
    @jwt_required
    def get(self):
        return {
            'value': UserModel.find({'User.id': get_user_id()})[0]
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
        updated = UserModel.update(user_id, data)
        return {'message': 'ok'} if updated else error(HTTPStatus.NOT_FOUND)


info_api.add_resource(Information, '/information')
