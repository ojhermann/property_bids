from random import randint
from typing import Optional

from models.bid.v0.model import Bid
from models.bid_heap.v0.model import BidHeap


def test_bid_heap_works():
    auction_id: str = "an_auction_id"
    bidder_id: str = "a_bidder_id"

    bid_zero: Bid = Bid(amount=0, auction_id=auction_id, bidder_id=bidder_id)
    bid_one: Bid = Bid(amount=1, auction_id=auction_id, bidder_id=bidder_id)
    bid_two: Bid = Bid(amount=2, auction_id=auction_id, bidder_id=bidder_id)
    bid_three: Bid = Bid(amount=3, auction_id=auction_id, bidder_id=bidder_id)

    bid_heap: BidHeap = BidHeap(reserve_bid=bid_one)
    assert bid_heap.peek() == bid_one

    bid_heap.insert(bid_zero)
    assert bid_heap.peek() == bid_one

    bid_heap.insert(bid_three)
    assert bid_heap.peek() == bid_three

    bid_heap.insert(bid_two)
    assert bid_heap.peek() == bid_three

    assert bid_heap.reserve_bid == bid_one


def test_random_values_on_bid_heap():
    min_size: int = 1
    max_size: int = 100
    for size in range(min_size, max_size + 1):
        bid_list: list[Bid] = [Bid(amount=randint(min_size, max_size), auction_id="a", bidder_id="b") for _ in
                               range(size)]
        bid_heap: BidHeap = BidHeap(reserve_bid=bid_list[0])
        for bid in bid_list[1:]:
            bid_heap.insert(bid)

        current: Optional[int] = bid_heap.pop()
        subsequent: Optional[int] = bid_heap.pop()
        while current is not None and subsequent is not None:
            assert subsequent <= current
            current = subsequent
            subsequent = bid_heap.pop()
