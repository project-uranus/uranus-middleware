from uranus_middleware.auth_utils import get_data_from_token
from uranus_middleware.models.user import Role

from . import SocketHolder, sockets

security = SocketHolder()


@sockets.route('/security/<token>')
def security_socket(socket, token):
    data = get_data_from_token(token)
    user_id = data.get('identifier')
    user_role = data.get('role')
    if user_role != Role.SECURITY.value:
        return socket.close()
    security.add(user_id, socket)  # key: user id (int)
    while not socket.closed:
        message = socket.receive()
        print(f'message from security: {message}')
    security.remove(user_id)
