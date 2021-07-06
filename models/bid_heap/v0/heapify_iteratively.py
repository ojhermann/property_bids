from models.bid.v0.model import Bid


def heapify_inner(
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


def heapify(
        bids: list[Bid],
        size: int,
) -> None:
    for i in range(size // 2, -1, -1):
        heapify_inner(bids=bids, size=size, index=i)