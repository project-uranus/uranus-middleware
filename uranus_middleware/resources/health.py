from json import loads

from flask import Blueprint, request

from flask_restful import Api, Resource

from uranus_middleware.endpoints.notification import notification

health_blueprint = Blueprint('health', __name__)
health_api = Api(health_blueprint)


class Health(Resource):
    def get(self):
        return {'status': 'OK'}

    def post(self):
        notification.broadcast(loads(str(request.data, encoding='utf-8')))
        return {'message': 'ok'}


health_api.add_resource(Health, '/health')
