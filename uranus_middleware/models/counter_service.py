from dataclasses import dataclass
from random import choice


@dataclass
class Counter(object):
    counter_id: int
    staff_id: str
    is_available: bool
    length: int

    __slots__ = ('counter_id', 'staff_id', 'is_available', 'length')


class CounterService(object):
    def __init__(self):
        self.__counters = {}  # key: counter id (int), value: counter object
        self.__id = 0

    def allocate_counter(self, number_of_luggages, fellows) -> int:
        # algorithm goes here
        counter_ids = self.__counters.keys()
        return choice(list(counter_ids)) if len(counter_ids) > 0 else None

    def add(self, staff_id: str) -> int:
        self.__id += 1
        counter = Counter(self.__id, staff_id, True, 0)
        self.__counters[counter.counter_id] = counter
        return counter.counter_id

    def remove(self, counter_id: int):
        del self.__counters[counter_id]

    def length_add(self, counter_id: int):
        counter = self.__counters[counter_id]
        counter.length += 1

    def length_sub(self, staff_id: str):
        counter = self.find_by_staff(staff_id)
        counter.length -= 1

    def find_by_staff(self, staff_id: str) -> Counter:
        return next(filter(lambda counter: counter.staff_id == staff_id, self.__counters.values()))


counter_service = CounterService()
