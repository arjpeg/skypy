from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from skypy.auction.auction_category import AuctionCategory
from skypy.items import make_correct_item
from skypy.items.item import Item
from skypy.items.rarity import ItemRarity


@dataclass
class AuctionBid:
    auction_id: str
    bidder: str
    profile_id: str
    amount: int
    timestamp: int


@dataclass
class Auction:
    """
    A class for an auction.
    """

    uuid: str
    seller_uuid: str
    profile_id: str
    coop: list[str]

    time_started: int
    time_ended: int

    category: AuctionCategory
    item: Item

    starting_bid: float
    claimed: bool

    is_bin: bool
    bids: list[AuctionBid] = field(default_factory=list)

    @property
    def highest_bid(self) -> float:
        if self.is_bin:
            return self.starting_bid
        else:
            if self.bids:
                return max(self.bids, key=lambda bid: bid.amount).amount
            else:
                return self.starting_bid

    @staticmethod
    def from_json(json: dict[str, Any]) -> Auction:
        """
        Initialize the auction from the json.
        """

        return Auction(
            uuid=json["uuid"],
            seller_uuid=json["auctioneer"],
            profile_id=json["profile_id"],
            coop=json["coop"],
            time_started=json["start"],
            time_ended=json["end"],
            category=AuctionCategory(json["category"].upper()),
            item=make_correct_item(
                Item(
                    uuid=json.get("item_uuid"),
                    name=json["item_name"],
                    rarity=ItemRarity(json["tier"]),
                    lore=json["item_lore"],
                    nbt_data=json["item_bytes"],
                    extra=json["extra"],
                ),
                AuctionCategory(json["category"].upper()),
            ),
            starting_bid=json["starting_bid"],
            claimed=json["claimed"],
            is_bin=json["bin"],
            bids=[AuctionBid(**bid) for bid in json["bids"]],
        )
