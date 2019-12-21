from flask import Blueprint

from flask_restful import Api, Resource

from uranus_middleware.auth_utils import admin_required
from uranus_middleware.models.user import User as UserModel

user_blueprint = Blueprint('user', __name__)
user_api = Api(user_blueprint)


class User(Resource):
    @admin_required
    def get(self):
        return {
            'value': UserModel.find()
        }


user_api.add_resource(User, '/users')
