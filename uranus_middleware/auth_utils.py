from http import HTTPStatus

from flask_jwt_simple import get_jwt, jwt_required

from uranus_middleware.error import error
from uranus_middleware.models.user import Role


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


def roles_required(roles):
    def decorator(fn):
        @jwt_required
        def wrapper(*args, **kwargs):
            user = get_jwt()
            return fn(*args, **kwargs) if user['role'] in [role.value for role in roles] else unauthorized
        return wrapper
    return decorator


def get_user_id():
    return get_jwt().get('identifier')


def get_user_role():
    return Role(get_jwt().get('role'))
