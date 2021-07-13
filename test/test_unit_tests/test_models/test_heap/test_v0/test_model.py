from random import randint
from typing import Optional

from models.heap.v0.model import Heap


def create_ascending_list(start: int = 0, end: int = 10) -> list[int]:
    return [n for n in range(start, end, 1)]


def create_descending_list(start: int = 9, end: int = 0) -> list[int]:
    return [n for n in range(start, end - 1, -1)]


def test_init_and_pop_work():
    ascending_list: list[int] = create_ascending_list()
    size: int = len(ascending_list)
    max_heap: Heap = Heap(fnc_child_parent=lambda x, y: x > y, data=ascending_list)
    assert max_heap.size == size
    assert max_heap.peek() == 9

    max_values_in_order: list[int] = list()
    current_max: Optional[int] = max_heap.pop()
    size -= 1
    while current_max is not None:
        assert max_heap.size == size
        max_values_in_order.append(current_max)
        current_max = max_heap.pop()
        size -= 1
    assert max_values_in_order == create_descending_list()
    assert max_heap.size == 0


def test_insert_and_pop_work():
    descending_list: list[int] = create_descending_list()
    min_heap: Heap = Heap(fnc_child_parent=lambda x, y: x < y, data=descending_list)

    min_heap.insert(value=10)
    assert min_heap.size == 11
    assert min_heap.peek() == 0

    min_heap.insert(value=-1)
    assert min_heap.size == 12
    assert min_heap.peek() == -1

    min_values_in_order: list[int] = list()
    current_min: Optional[int] = min_heap.pop()
    while current_min is not None:
        min_values_in_order.append(current_min)
        current_min = min_heap.pop()
    assert min_values_in_order == create_ascending_list(start=-1, end=11)
    assert min_heap.size == 0

    min_heap.insert(5)
    min_heap.insert(0)
    assert min_heap.pop() == 0
    assert min_heap.pop() == 5
    assert min_heap.pop() is None


def test_remove_works_as_pop():
    data: list[int] = create_descending_list()
    min_heap: Heap = Heap(fnc_child_parent=lambda x, y: x < y, data=data)

    ascending_list: list[int] = create_ascending_list()
    for _ in range(10):
        assert min_heap.pop() == ascending_list.pop(0)


def test_remove_works_with_known_values():
    data: list[int] = create_descending_list()
    min_heap: Heap = Heap(fnc_child_parent=lambda x, y: x < y, data=data)

    for index in range(5):
        min_heap.remove(index)
    assert min_heap.size == 5

    current: Optional[int] = min_heap.pop()
    subsequent: Optional[int] = min_heap.pop()
    while current is not None and subsequent is not None:
        assert current <= subsequent
        current = subsequent
        subsequent = min_heap.pop()


def test_remove_works_with_random_values():
    min_size: int = 0
    max_size: int = 100
    for size in range(min_size, max_size + 1):
        value_list: list[int] = [randint(min_size, max_size) for _ in range(size)]
        min_heap: Heap = Heap(fnc_child_parent=lambda x, y: x < y, data=value_list)

        for index in range(size // 2):
            min_heap.remove(index=index)
        current: Optional[int] = min_heap.pop()
        subsequent: Optional[int] = min_heap.pop()
        while current is not None and subsequent is not None:
            assert current <= subsequent
            current = subsequent
            subsequent = min_heap.pop()


def test_random_values_on_min_heap():
    min_size: int = 0
    max_size: int = 100
    for size in range(min_size, max_size + 1):
        value_list: list[int] = [randint(min_size, max_size) for _ in range(size)]
        min_heap: Heap = Heap(fnc_child_parent=lambda x, y: x < y, data=value_list)
        current: Optional[int] = min_heap.pop()
        subsequent: Optional[int] = min_heap.pop()
        while current is not None and subsequent is not None:
            assert current <= subsequent
            current = subsequent
            subsequent = min_heap.pop()


def test_random_values_on_max_heap():
    min_size: int = 0
    max_size: int = 100
    for size in range(min_size, max_size + 1):
        value_list: list[int] = [randint(min_size, max_size) for _ in range(size)]
        min_heap: Heap = Heap(fnc_child_parent=lambda x, y: x > y, data=value_list)
        current: Optional[int] = min_heap.pop()
        subsequent: Optional[int] = min_heap.pop()
        while current is not None and subsequent is not None:
            assert current >= subsequent
            current = subsequent
            subsequent = min_heap.pop()
