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

    @staticmethod
    def _get_left_child_index(parent_index: int) -> int:
        return 2 * parent_index + 1

    @staticmethod
    def _get_right_child_index(parent_index: int) -> int:
        return 2 * parent_index + 2

    @staticmethod
    def _get_parent_index(child_index: int) -> int:
        return (child_index - 1) // 2

    def _increment_size(self) -> None:
        self.size += 1

    def _decrement_size(self) -> None:
        self.size -= 1

    def _insert(self, value: T) -> None:
        self.data.append(value)
        self._increment_size()

    def _pop(self, index: int) -> Optional[T]:
        if self.size > 0:
            self._decrement_size()
            return self.data.pop(index)
        else:
            return None

    def _swap(self, index_a: int, index_b: int) -> None:
        self.data[index_a], self.data[index_b] = self.data[index_b], self.data[index_a]

    def _heapify_down(self, index: int = 0) -> None:
        while 0 <= index < self.size:
            parent_index: int = index
            left_index: int = self._get_left_child_index(parent_index)
            right_index: int = self._get_right_child_index(parent_index)

            if left_index < self.size and self.fnc(self.data[left_index], self.data[parent_index]):
                parent_index = left_index

            if right_index < self.size and self.fnc(self.data[right_index], self.data[parent_index]):
                parent_index = right_index

            if parent_index != index:
                self._swap(parent_index, index)
                index = parent_index
            else:
                index = self.size

    def _heapify_up(self, index: Optional[int] = None) -> None:
        index = self.size - 1 if index is None else index
        while 0 <= index < self.size:
            child_index: int = index
            parent_index: int = self._get_parent_index(child_index)
            if parent_index > -1 and self.fnc(self.data[child_index], self.data[parent_index]):
                self._swap(parent_index, child_index)
                index = parent_index
            else:
                index = self.size

    def _build_heap(self) -> None:
        for i in range(self._get_parent_index(self.size - 1), -1, -1):
            self._heapify_down(index=i)

    def insert(self, value: T) -> None:
        self._insert(value)
        self._heapify_up()

    def remove(self, index: int) -> Optional[T]:
        if index < 0 or self.size <= index:
            return None
        else:
            self._swap(index, self.size - 1)
            result: T = self._pop(self.size - 1)
            self._heapify_up(index)
            self._heapify_down(index)
            return result

    def pop(self) -> Optional[T]:
        return self.remove(0)

    def peek(self) -> Optional[T]:
        return self.data[0] if self.size > 0 else None
