from models.bid.v0.model import Bid
from models.heap.v0.model import Heap


class BidHeap(Heap):
    def __init__(
            self,
            reserve_bid: Bid,
    ):
        super().__init__(
            fnc_child_parent=lambda child, parent: child > parent,
            data=[reserve_bid]
        )
        self.reserve_bid: Bid = reserve_bid

    def bid_count(self) -> int:
        return self.size - 1
