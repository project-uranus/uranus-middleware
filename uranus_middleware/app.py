from datetime import datetime, timedelta

from flask import Flask

from flask_cors import CORS

from flask_jwt_simple import JWTManager

from uranus_middleware.auth_utils import JWT_SECRET_KEY
from uranus_middleware.endpoints import init_app
from uranus_middleware.resources import (
    airport, auth, boarding_pass, check_in, flight, health, infomation, luggage, passenger, password, user
)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

JWT_EXPIRES = timedelta(days=30)
jwt = JWTManager(app)


@jwt.jwt_data_loader
def add_claims_to_access_token(user):
    now = datetime.utcnow()
    return {
        'iss': 'uranus',
        'exp': now + JWT_EXPIRES,
        'iat': now,
        'role': user['role'],
        'identifier': user['id']
    }


app.register_blueprint(health.health_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(airport.airport_blueprint)
app.register_blueprint(flight.flight_blueprint)
app.register_blueprint(passenger.passenger_blueprint)
app.register_blueprint(password.password_blueprint)
app.register_blueprint(infomation.info_blueprint)
app.register_blueprint(check_in.checkin_blueprint)
app.register_blueprint(luggage.luggage_blueprint)
app.register_blueprint(boarding_pass.boarding_pass_blueprint)
CORS(app)
init_app(app)

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
