from uranus_middleware.auth_utils import get_data_from_token
from uranus_middleware.models.counter_service import counter_service
from uranus_middleware.models.user import Role

from . import SocketHolder, sockets

counter = SocketHolder()


@sockets.route('/counter/<token>')
def counter_socket(socket, token):
    data = get_data_from_token(token)
    user_id = data.get('identifier')
    user_role = data.get('role')
    if user_role != Role.STAFF.value:
        return socket.close()
    counter_id = counter_service.find_by_staff(user_id).counter_id
    counter.add(counter_id, socket)  # key: counter id (int)
    while not socket.closed:
        message = socket.receive()
        print(f'message from counter: {message}')
        # counter.notify(user_id, message)  # echo
    counter.remove(counter_id)
    # counter_service.remove(counter_id)
