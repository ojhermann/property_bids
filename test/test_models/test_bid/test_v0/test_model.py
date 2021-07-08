import datetime

import pytest

from models.bid.v0.model import Bid


class TestInitAndAttributes:
    amount: int = 0
    auction_id: str = "auction_id"
    bidder_id: str = "bidder_id"

    @staticmethod
    def get_bid() -> Bid:
        return Bid(
            amount=TestInitAndAttributes.amount,
            auction_id=TestInitAndAttributes.auction_id,
            bidder_id=TestInitAndAttributes.bidder_id
        )

    def test_init_works(self):
        bid: Bid = self.get_bid()
        assert bid.amount == 0
        assert bid.auction_id == TestInitAndAttributes.auction_id
        assert bid.bidder_id == TestInitAndAttributes.bidder_id
        assert bid.made_at is not None
        assert bid.removed_at is None

    def test_amount_is_immutable(self):
        with pytest.raises(TypeError):
            bid: Bid = self.get_bid()
            bid.amount = 1

    def test_auction_id_is_immutable(self):
        with pytest.raises(TypeError):
            bid: Bid = self.get_bid()
            bid.auction_id = "not_allowed"

    def test_bidder_id_is_immutable(self):
        with pytest.raises(TypeError):
            bid: Bid = self.get_bid()
            bid.bidder_id = "not_allowed"

    def test_made_at_is_immutable(self):
        with pytest.raises(TypeError):
            bid: Bid = self.get_bid()
            bid.made_at = datetime.datetime.now()

    def test_made_at_is_mutable(self):
        bid: Bid = self.get_bid()
        assert bid.removed_at is None
        bid.removed_at = datetime.datetime.now()
        assert bid.removed_at is not None


class TestLessThan:
    @staticmethod
    def get_amount(value: int = 0) -> int:
        return value

    @staticmethod
    def get_auction_id(value: str = "auction_id") -> str:
        return value

    @staticmethod
    def get_bidder_id(value: str = "bidder_id") -> str:
        return value

    def test_active_bids_identical_except_for_amount(self):
        made_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)

        lower_amount: Bid = Bid(
            amount=self.get_amount(value=0),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
        )

        higher_amount: Bid = Bid(
            amount=self.get_amount(value=1),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
        )

        assert lower_amount < higher_amount

    def test_active_bids_identical_except_for_made_at(self):
        earlier_made_at: Bid = Bid(
            amount=self.get_amount(),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
        )

        later_made_at: Bid = Bid(
            amount=self.get_amount(),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)
        )

        assert later_made_at < earlier_made_at

    def test_inactive_bids_identical_except_for_amount(self):
        made_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)
        removed_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)

        lower_amount: Bid = Bid(
            amount=self.get_amount(value=0),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
            removed_at=removed_at,
        )

        higher_amount: Bid = Bid(
            amount=self.get_amount(value=1),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
            removed_at=removed_at,
        )

        assert lower_amount < higher_amount

    def test_inactive_bids_identical_except_for_made_at(self):
        made_at_earlier: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)
        made_at_later: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)
        removed_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=2)

        earlier_made_at: Bid = Bid(
            amount=self.get_amount(),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at_earlier,
            removed_at=removed_at,
        )

        later_made_at: Bid = Bid(
            amount=self.get_amount(),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at_later,
            removed_at=removed_at,
        )

        assert later_made_at < earlier_made_at

    def test_active_always_bid_preferred(self):
        made_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)
        removed_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)

        active_bid_otherwise_identical: Bid = Bid(
            amount=self.get_amount(),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
        )
        inactive_bid_otherwise_identical: Bid = Bid(
            amount=self.get_amount(),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
            removed_at=removed_at,
        )
        assert inactive_bid_otherwise_identical < active_bid_otherwise_identical

        active_bid_lower_amount: Bid = Bid(
            amount=self.get_amount(value=0),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
        )
        inactive_bid_higher_amount: Bid = Bid(
            amount=self.get_amount(value=10),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
            removed_at=removed_at,
        )
        assert inactive_bid_higher_amount < active_bid_lower_amount

        active_bid_later_made_at: Bid = Bid(
            amount=self.get_amount(value=0),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=removed_at,
        )

        inactive_bid_earlier_made_at: Bid = Bid(
            amount=self.get_amount(value=10),
            auction_id=self.get_auction_id(),
            bidder_id=self.get_bidder_id(),
            made_at=made_at,
            removed_at=removed_at,
        )
        assert inactive_bid_earlier_made_at < active_bid_later_made_at
