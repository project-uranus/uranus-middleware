from flask_socketio import SocketIO


socketio = SocketIO()


def init_app(app):
    # from . import test
    socketio.init_app(app, cors_allowed_origins='*')
