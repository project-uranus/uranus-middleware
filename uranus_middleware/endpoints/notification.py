from uranus_middleware.auth_utils import get_data_from_token
from uranus_middleware.models.user import Role

from . import SocketHolder, sockets

notification = SocketHolder()


@sockets.route('/notification/<token>')
def notification_socket(socket, token):
    data = get_data_from_token(token)
    user_id = data.get('identifier')
    user_role = data.get('role')
    print(f'notification role: {user_role}')
    if user_role != Role.PASSENGER.value:
        print(f'role != {Role.PASSENGER}')
        return socket.close()
    notification.add(user_id, socket)   # key: user id (int)
    while not socket.closed:
        message = socket.receive()
        print(f'message from notification: {message}')
        # notification.notify(user_id, message)  # echo
    notification.remove(user_id)
