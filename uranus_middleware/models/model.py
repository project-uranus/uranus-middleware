from typing import List

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
        return requests.post(f'{url}/{type(self).__name__}', json=self._as_dict()).json()

    # get
    @classmethod
    def find(cls, params=None) -> List[dict]:
        response_dict = requests.get(f'{url}/{cls.__name__}', params=params).json()
        return response_dict[cls.__name__] if len(response_dict) > 0 else []

    # put
    @classmethod
    def update(cls, id, params: dict = None) -> dict:
        found = cls.find({f'{cls.__name__}.id': id})
        if len(found) == 0:
            return None
        data = {**found[0], **params}
        return requests.put(f'{url}/{cls.__name__}/{id}', json=data).json()
