from typing import Optional

from models.bid.v1.model import Bid


class BidHeap:
    def __init__(
            self,
            reserve_bid: Bid):
        self._bid_id: int = -1
        self.reserve_bid: Bid = reserve_bid
        self.bids: list[Bid] = list()
        self.size: int = 0
        self.bids_by_bidder_id: dict[str, list[Bid]] = dict()
        self.heap_index_by_bid_id: dict[int, int] = dict()
        self._init_helper(reserve_bid)

    @staticmethod
    def _left_child_index(parent_index: int) -> int:
        return 2 * parent_index + 1

    @staticmethod
    def _right_child_index(parent_index: int) -> int:
        return 2 * parent_index + 2

    @staticmethod
    def _parent_index(child_index: int) -> int:
        return (child_index - 1) // 2

    def _get_bid_id(self) -> int:
        self._bid_id += 1
        return self._bid_id

    def _init_helper(self, reserve_bid: Bid) -> None:
        self.reserve_bid = Bid(
            amount=reserve_bid.amount,
            auction_id=reserve_bid.auction_id,
            bidder_id=reserve_bid.bidder_id,
            made_at=reserve_bid.made_at,
            id=self._get_bid_id(),
        )
        self.bids.append(self.reserve_bid)
        self._increment_size()
        self.bids_by_bidder_id[self.reserve_bid.bidder_id] = [self.reserve_bid]
        self.heap_index_by_bid_id[self.reserve_bid.id] = 0

    def _increment_size(self) -> None:
        self.size += 1

    def _decrement_size(self) -> None:
        self.size -= 1

    def _insert_into_bids_by_bidder_id(self, bid: Bid) -> None:
        if bid.bidder_id in self.bids_by_bidder_id:
            self.bids_by_bidder_id[bid.bidder_id].append(bid)
        else:
            self.bids_by_bidder_id[bid.bidder_id] = [bid]

    def _insert_into_heap_index_by_bid_id(self, bid: Bid) -> None:
        self.heap_index_by_bid_id[bid.id] = self.size - 1

    def _insert(self, bid: Bid) -> None:
        self._increment_size()
        self.bids.append(bid)
        self._insert_into_bids_by_bidder_id(bid)
        self._insert_into_heap_index_by_bid_id(bid)

    def _swap(self, index_a: int, index_b: int) -> None:
        self.bids[index_a], self.bids[index_b] = self.bids[index_b], self.bids[index_a]
        self.heap_index_by_bid_id[self.bids[index_a].id] = index_a
        self.heap_index_by_bid_id[self.bids[index_b].id] = index_b

    def _heapify_down(self, index: int = 0) -> None:
        while 0 <= index < self.size:
            parent_index: int = index
            left_index: int = self._left_child_index(parent_index)
            right_index: int = self._right_child_index(parent_index)

            if left_index < self.size and self.bids[parent_index] < self.bids[left_index]:
                parent_index = left_index

            if right_index < self.size and self.bids[parent_index] < self.bids[right_index]:
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
            parent_index: int = self._parent_index(child_index)
            if parent_index > -1 and self.bids[parent_index] < self.bids[child_index]:
                self._swap(parent_index, child_index)
                index = parent_index
            else:
                index = self.size

    def insert(self, bid: Bid) -> int:
        bid.id = self._get_bid_id()
        self._insert(bid)
        self._heapify_up()
        return bid.id

    def remove(self, bid_id: int) -> bool:
        if bid_id in self.heap_index_by_bid_id:
            index: int = self.heap_index_by_bid_id[bid_id]
            self.bids[index].remove()
            self._heapify_up(index)
            self._heapify_down(index)
            return True
        else:
            return False

    def pop(self) -> Optional[Bid]:
        if self.size == 0:
            return None
        else:
            self._swap(0, self.size - 1)
            best_bid: Bid = self.bids.pop()
            self._decrement_size()
            del self.heap_index_by_bid_id[best_bid.id]
            self.bids_by_bidder_id[best_bid.bidder_id].pop()
            self._heapify_down(index=0)
            return best_bid

    def peek(self) -> Optional[Bid]:
        return self.bids[0] if self.size > 0 else None
