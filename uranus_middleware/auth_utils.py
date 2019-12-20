from http import HTTPStatus

from flask_jwt_simple import get_jwt, jwt_required

from uranus_middleware.error import error


unauthorized = error(HTTPStatus.UNAUTHORIZED)


def admin_required(fn):
    @jwt_required
    def wrapper(*args, **kwargs):
        user = get_jwt()
        return fn(*args, **kwargs) if user['role'] == 'administrator' else unauthorized
    return wrapper


def staff_required(fn):
    @jwt_required
    def wrapper(*args, **kwargs):
        user = get_jwt()
        return fn(*args, **kwargs) if user['role'] == 'staff' else unauthorized
    return wrapper


def passenger_required(fn):
    @jwt_required
    def wrapper(*args, **kwargs):
        user = get_jwt()
        return fn(*args, **kwargs) if user['role'] == 'passenger' else unauthorized
    return wrapper


def get_user_id():
    return get_jwt().get('identifier')
