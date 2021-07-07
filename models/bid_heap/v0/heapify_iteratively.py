from typing import Callable, Generic, TypeVar

from models.bid.v0.model import Bid

T = TypeVar('T')


class Heap(Generic[T]):
    def __init__(self, fnc: Callable[[T, T], bool]):
        self.data: list[T] = list()
        self.fnc: Callable[[T, T], bool] = fnc
        self.size: int = 0

    def heapify(self, index: int = 0) -> None:
        while 0 <= index < self.size:
            parent: int = index
            left: int = 2 * parent + 1
            right: int = 2 * parent + 2

            if left < self.size and self.fnc(self.data[parent], self.data[left]):
                parent = left

            if right < self.size and self.fnc(self.data[parent], self.data[right]):
                parent = right

            if parent != index:
                self.data[parent], self.data[index] = self.data[index], self.data[parent]
                index = parent
            else:
                index = self.size


def heapify(
        bids: list[Bid],
        size: int,
        index: int,
) -> None:
    while index < size:
        largest: int = index
        left: int = 2 * index + 1
        right: int = 2 * index + 2

        if left < size and bids[largest] < bids[left]:
            largest = left

        if right < size and bids[largest] < bids[right]:
            largest = right

        if largest != index:
            bids[largest], bids[index] = bids[index], bids[largest]
            index = largest
        else:
            index = size


def build_heap(
        bids: list[Bid],
        size: int,
) -> None:
    for i in range(size // 2, -1, -1):
        heapify(bids=bids, size=size, index=i)


def insert(
        bid: Bid,
        bids: list[Bid],
        size: int,
) -> None:
    bids.append(bid)
    size += 1
    child_index: int = size - 1
    parent_index: int = child_index // 2
    while 0 <= parent_index and bids[parent_index] < bids[child_index]:
        bids[parent_index], bids[child_index] = bids[child_index], bids[parent_index]
        child_index = parent_index
        parent_index: int = child_index // 2
