from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .item import Item, ItemRarity


@dataclass
class AuctionBid:
    auction_id: str
    bidder: str
    profile_id: str
    amount: int
    timestamp: int


class AuctionCategory(Enum):
    WEAPON = "WEAPON"
    ARMOR = "ARMOR"
    ACCESSORIES = "ACCESSORIES"
    CONSUMABLES = "CONSUMABLES"
    BLOCKS = "BLOCKS"
    MISC = "MISC"


@dataclass
class Auction:
    """
    A class for an auction. Coming from the hypixel api, it looks like this:
    {"uuid":"{UUID}","auctioneer":"{PERSON_WHO_AUCTIONED}","profile_id":"{WHICH_PROFILE}}","coop":["ANY_COOP_MEMBERS"],"start":{TIME_WHEN_AUCTIONED},"end":{WHEN_AUCTION_END},"item_name":"{ITEM_NAME}","item_lore":"{ITEM_LORE}","extra":"{EXTRA_INFO}","category":"{ITEM_TYPE}","tier":"{ITEM_TIER}","starting_bid":{STARTING_BID},"item_bytes":"{ITEM_DATA_IN_BASE_64}","claimed":{true/false},"claimed_bidders":[],"highest_bid_amount":{HIGHEST_BID_AMOUNT_IF_AUCTION},"last_updated":{...},"bin":{BIN_OR_AUCTION},"bids":[],"item_uuid":"{ITEM_UUID}"},
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
            item=Item.make_correct_item(
                Item(
                    uuid=json.get("item_uuid"),
                    name=json["item_name"],
                    rarity=ItemRarity(json["tier"]),
                    lore=json["item_lore"],
                    nbt_data=json["item_bytes"],
                    extra=json["extra"],
                )
            ),
            starting_bid=json["starting_bid"],
            claimed=json["claimed"],
            is_bin=json["bin"],
            bids=[AuctionBid(**bid) for bid in json["bids"]],
        )
