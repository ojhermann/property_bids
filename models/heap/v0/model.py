from typing import Callable, Generic, TypeVar, Optional

T = TypeVar('T')


class Heap(Generic[T]):
    def __init__(
            self,
            fnc_child_parent: Callable[[T, T], bool],
            data: list[T] = [],
    ):
        self.fnc: Callable[[T, T], bool] = fnc_child_parent
        self.size: int = len(data)
        self.data: list[T] = data
        self._build_heap()

    def _swap(self, index_a: int, index_b: int) -> None:
        self.data[index_a], self.data[index_b] = self.data[index_b], self.data[index_a]

    def _heapify(self, index: int = 0) -> None:
        while 0 <= index < self.size:
            parent: int = index
            left: int = 2 * parent + 1
            right: int = 2 * parent + 2

            if left < self.size and self.fnc(self.data[left], self.data[parent]):
                parent = left

            if right < self.size and self.fnc(self.data[right], self.data[parent]):
                parent = right

            if parent != index:
                self._swap(parent, index)
                index = parent
            else:
                index = self.size

    def _build_heap(self) -> None:
        for i in range(self.size // 2, -1, -1):
            self._heapify(index=i)

    def insert(self, value: T) -> None:
        self.data.append(value)
        self.size += 1
        child_index: int = self.size - 1
        parent_index: int = child_index // 2
        while 0 <= parent_index and self.fnc(self.data[child_index], self.data[parent_index]):
            self._swap(parent_index, child_index)
            child_index = parent_index
            parent_index: int = child_index // 2

    def pop(self) -> Optional[T]:
        if self.size == 0:
            return None
        elif self.size == 1:
            self.size -= 1
            return self.data.pop()
        else:
            result: T = self.data[0]
            self.data[0] = self.data.pop()
            self.size -= 1
            self._heapify()
            return result

    def peek(self) -> Optional[T]:
        return self.data[0] if self.size > 0 else None
