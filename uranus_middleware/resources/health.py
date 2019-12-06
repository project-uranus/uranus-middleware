from flask import Blueprint
from flask_restful import Api, Resource

health_blueprint = Blueprint('health', __name__)
health_api = Api(health_blueprint)


class Health(Resource):
    def get(self):
        return {'status': 'OK'}


health_api.add_resource(Health, '/health')
