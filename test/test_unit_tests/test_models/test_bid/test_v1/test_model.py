from datetime import datetime, timedelta, timezone
from typing import Optional

import pytest

from models.bid.v1.model import Bid

amount_default: int = 0
auction_id_default: str = "auction_id"
bidder_id_default: str = "bidder_id"


def get_bid(
        amount: int = amount_default,
        auction_id: str = auction_id_default,
        bidder_id: str = bidder_id_default,
        made_at: datetime = datetime.now(tz=timezone.utc),
        removed_at: Optional[datetime] = None,
) -> Bid:
    return Bid(
        amount=amount,
        auction_id=auction_id,
        bidder_id=bidder_id,
        made_at=made_at,
        removed_at=removed_at,
    )


class TestInitAndAttributes:
    def test_init_works(self):
        bid: Bid = get_bid()
        assert bid.amount == 0
        assert bid.auction_id == auction_id_default
        assert bid.bidder_id == bidder_id_default
        assert bid.made_at is not None
        assert bid.removed_at is None

    def test_amount_is_immutable(self):
        with pytest.raises(TypeError):
            bid: Bid = get_bid()
            bid.amount = 1

    def test_auction_id_is_immutable(self):
        with pytest.raises(TypeError):
            bid: Bid = get_bid()
            bid.auction_id = "not_allowed"

    def test_bidder_id_is_immutable(self):
        with pytest.raises(TypeError):
            bid: Bid = get_bid()
            bid.bidder_id = "not_allowed"

    def test_made_at_is_immutable(self):
        with pytest.raises(TypeError):
            bid: Bid = get_bid()
            bid.made_at = datetime.now()

    def test_made_at_is_mutable(self):
        bid: Bid = get_bid()
        assert bid.removed_at is None
        bid.removed_at = datetime.now()
        assert bid.removed_at is not None


class TestRemove:
    def test_remove_works(self):
        bid: Bid = get_bid()
        assert bid.removed_at is None
        bid.remove()
        assert bid.removed_at is not None


class TestBidId:
    def test_bid_id_works(self):
        bid: Bid = get_bid()
        assert bid.id is None
        bid.id = 0
        assert bid.id == 0


class TestLessThan:
    def test_active_bids_identical_except_for_amount(self):
        made_at: datetime = datetime.now(tz=timezone.utc)

        lower_amount: Bid = get_bid(amount=0, made_at=made_at)
        higher_amount: Bid = get_bid(amount=1, made_at=made_at)
        assert lower_amount < higher_amount
        assert lower_amount != higher_amount
        assert not lower_amount > higher_amount

    def test_active_bids_identical_except_for_made_at(self):
        earlier: datetime = datetime.now(tz=timezone.utc)
        later: datetime = datetime.now(tz=timezone.utc) + timedelta(days=1)

        earlier_made_at: Bid = get_bid(made_at=earlier)
        later_made_at: Bid = get_bid(made_at=later)
        assert later_made_at < earlier_made_at
        assert later_made_at != earlier_made_at
        assert not later_made_at > earlier_made_at

    def test_inactive_bids_identical_except_for_amount(self):
        made_at: datetime = datetime.now(tz=timezone.utc)
        removed_at: datetime = made_at + timedelta(days=1)

        lower_amount: Bid = get_bid(amount=0, made_at=made_at, removed_at=removed_at)
        higher_amount: Bid = get_bid(amount=1, made_at=made_at, removed_at=removed_at)
        assert lower_amount < higher_amount
        assert lower_amount != higher_amount
        assert not lower_amount > higher_amount

    def test_inactive_bids_identical_except_for_made_at(self):
        earlier: datetime = datetime.now(tz=timezone.utc)
        later: datetime = earlier + timedelta(days=1)
        latest: datetime = later + timedelta(days=1)

        earlier_made_at: Bid = get_bid(made_at=earlier, removed_at=latest)
        later_made_at: Bid = get_bid(made_at=later, removed_at=latest)
        assert later_made_at < earlier_made_at
        assert later_made_at != earlier_made_at
        assert not later_made_at > earlier_made_at

    def test_active_always_bid_preferred(self):
        earlier: datetime = datetime.now(tz=timezone.utc)
        later: datetime = datetime.now(tz=timezone.utc) + timedelta(days=1)

        active_bid_otherwise_identical: Bid = get_bid(made_at=earlier)
        inactive_bid_otherwise_identical: Bid = get_bid(made_at=earlier, removed_at=later)
        assert inactive_bid_otherwise_identical < active_bid_otherwise_identical
        assert inactive_bid_otherwise_identical != active_bid_otherwise_identical
        assert not inactive_bid_otherwise_identical > active_bid_otherwise_identical

        active_bid_lower_amount: Bid = get_bid(amount=0)
        inactive_bid_higher_amount: Bid = get_bid(amount=1, removed_at=later)
        assert inactive_bid_higher_amount < active_bid_lower_amount
        assert inactive_bid_higher_amount != active_bid_lower_amount
        assert not inactive_bid_higher_amount > active_bid_lower_amount

        active_bid_later_made_at: Bid = get_bid(made_at=later)
        inactive_bid_earlier_made_at: Bid = get_bid(made_at=later, removed_at=later)
        assert inactive_bid_earlier_made_at < active_bid_later_made_at
        assert inactive_bid_earlier_made_at != active_bid_later_made_at
        assert not inactive_bid_earlier_made_at > active_bid_later_made_at


class TestEqualTo:
    def test_active_bids(self):
        made_at: datetime = datetime.now(tz=timezone.utc)

        a: Bid = get_bid(made_at=made_at)
        b: Bid = get_bid(made_at=made_at)
        assert not a < b
        assert a == b
        assert not a > b

    def test_inactive_bids(self):
        made_at: datetime = datetime.now(tz=timezone.utc)
        removed_at: datetime = made_at + timedelta(days=1)

        a: Bid = get_bid(made_at=made_at, removed_at=removed_at)
        b: Bid = get_bid(made_at=made_at, removed_at=removed_at)
        assert not a < b
        assert a == b
        assert not a > b
