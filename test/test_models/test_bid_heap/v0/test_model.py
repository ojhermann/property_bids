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
    bid_heap.insert(bid_zero)
    assert bid_heap.peek() == bid_one
    bid_heap.insert(bid_three)
    assert bid_heap.peek() == bid_three
    bid_heap.insert(bid_two)
    assert bid_heap.peek() == bid_three

    assert bid_heap.reserve_bid == bid_one
