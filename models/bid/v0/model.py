from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Bid(BaseModel):
    """
    A bid on a property
    """

    class Config:
        validate_assignment = True

    amount: int = Field(
        ...,
        description="Bid amount expressed in the unit denomination of the currency e.g. cents for EUR or USD"
    )

    auction_id: str = Field(
        ...,
        description="A unique identifier for an auction",
        allow_mutation=False,
    )

    bidder_id: str = Field(
        ...,
        description="A unique identifier for a bidder",
        allow_mutation=False,
    )

    made_at: datetime = Field(
        default=datetime.now(tz=timezone.utc),
        description="UTC timestamp of when the bid was made",
        allow_mutation=False,
    )

    removed_at: Optional[datetime] = Field(
        default=None,
        description="UTC timestamp of when the bid was removed",
        allow_mutation=True,
    )

    def __lt__(self, other: Bid) -> bool:
        both_bids_active: bool = self.is_active() and other.is_active()
        neither_bid_active: bool = not (self.is_active() or other.is_active())
        is_lower_amount: bool = self.amount < other.amount
        is_equal_amount: bool = self.amount == other.amount
        is_later_bid: bool = self.made_at < other.made_at

        if both_bids_active or neither_bid_active:
            return is_lower_amount or (is_equal_amount and is_later_bid)
        else:
            return not self.is_active()

    def __eq__(self, other: Bid) -> bool:
        both_bids_active: bool = self.is_active() and other.is_active()
        neither_bid_active: bool = not (self.is_active() or other.is_active())
        is_equal_amount: bool = self.amount == other.amount
        is_simultaneous: bool = self.made_at == other.made_at

        if both_bids_active or neither_bid_active:
            return is_equal_amount and is_simultaneous
        else:
            return False

    def __gt__(self, other: Bid) -> bool:
        return not self < other and not self == other

    def is_active(self) -> bool:
        return self.removed_at is None

    def remove(self) -> None:
        self.removed_at = datetime.now(tz=timezone.utc)
