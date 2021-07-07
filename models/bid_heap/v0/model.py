from typing import Optional

from models.bid.v0.model import Bid
from models.bid_heap.v0.heapify_iteratively import build_heap


class BidHeap:
    def __init__(self, reserve_bid: Bid):
        self._bids: list[Optional[Bid]] = [reserve_bid]
        self._reserve_bid: Bid = reserve_bid
        self._size: int = 1

    def _get_size(self) -> int:
        return self._size

    def _heapify(self) -> None:
        build_heap(self._bids, self._get_size())

    def number_of_bids(self) -> int:
        return self._get_size() - 1

    def reserve_bid(self) -> Bid:
        return self._reserve_bid

    def top_bid(self) -> Optional[Bid]:
        if self._get_size() > 0:
            return self._bids[0]
        else:
            return None

    def insert(self, bid: Bid) -> None:
        self._bids.append(bid)
        self._size += 1
        self._heapify()

    def pop(self) -> Optional[Bid]:
        if self._get_size() == 0:
            return None
        popped_bid: Bid = self._bids.pop(0)
        self._size -= 1
        if self._get_size() > 0:
            self._heapify()
        return popped_bid
