from json import dumps

from flask_sockets import Sockets

sockets = Sockets()


class SocketHolder(object):
    def __init__(self):
        self.__connections = {}

    def add(self, key, ws):
        self.__connections[key] = ws

    def notify(self, key, message):
        key = int(key)
        message = dumps(message, ensure_ascii=False)
        if key in self.__connections:
            self.__connections[key].send(message)

    def broadcast(self, message):
        message = dumps(message, ensure_ascii=False)
        for socket in self.__connections.values():
            if not socket.closed:
                socket.send(message)

    def remove(self, key):
        key = int(key)
        if key in self.__connections:
            del self.__connections[key]


def init_app(app):
    from . import notification, security, counter
    sockets.init_app(app)
