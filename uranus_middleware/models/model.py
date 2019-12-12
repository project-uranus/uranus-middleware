import json

import requests


url = 'http://47.100.198.206:8080/Entity/U1a69a8752399e8/demo_2'


class Model(object):
    def _as_dict(self) -> dict:
        _dict = {}
        for prop in self.__slots__:
            _dict[prop] = self.__getattribute__(prop)
        return _dict

    # post
    def save(self) -> dict:
        return json.loads(requests.post(f'{url}/{type(self).__name__}', json=self._as_dict()).text)

    # get
    @classmethod
    def find(cls, params) -> list:
        response_dict = json.loads(requests.get(f'{url}/{cls.__name__}', params=params).text)
        return response_dict[cls.__name__] if len(response_dict) > 0 else []
