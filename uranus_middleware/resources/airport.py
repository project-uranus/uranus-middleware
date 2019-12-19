from flask import Blueprint

from flask_restful import Api, Resource

from uranus_middleware.auth_utils import admin_required
from uranus_middleware.models.airport import Airport as AirportModel

airport_blueprint = Blueprint('airport', __name__)
airport_api = Api(airport_blueprint)


class Airport(Resource):
    @admin_required
    def get(self):
        return {
            "value": list(map(lambda x: x.get('iata'), AirportModel.find()))
        }


airport_api.add_resource(Airport, '/airports')
