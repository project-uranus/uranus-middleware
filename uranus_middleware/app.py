from datetime import datetime, timedelta

from flask import Flask

from flask_jwt_simple import JWTManager

from uranus_middleware.resources import airport, auth, flight, health, user


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'uranus-secret'

JWT_EXPIRES = timedelta(days=1)
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
