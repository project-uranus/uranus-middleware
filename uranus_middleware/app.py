from flask import Flask
from uranus_middleware.resources import health

app = Flask(__name__)
app.register_blueprint(health.health_blueprint)
