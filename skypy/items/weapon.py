from __future__ import annotations

from typing import Any

from skypy.auction.auction_category import AuctionCategory
from skypy.items.item import Item
from skypy.items.item_stats import ItemStats
from skypy.utils import remove_color_codes


class Weapon(Item):
    """Class to represent a weapon."""

    def __init__(
        self,
        lore: str,
        extra: str,
        nbt_data: dict[str, Any],
        item_stats: ItemStats,
        uuid: str | None = None,
    ) -> None:
        self.name = item_stats.name

        self.rarity = item_stats.rarity
        self.reforge = item_stats.modifer

        self.enchants = item_stats.enchantments
        self.hot_potatoes = item_stats.hot_potatoes

        self.dungoun_stars = item_stats.dungoun_stars

        self.lore = remove_color_codes(lore)
        self.extra = remove_color_codes(extra)
        self.nbt_data = nbt_data
        self.uuid = uuid

        self.id = self.nbt_data["i"][0]["tag"]["ExtraAttributes"]["id"]

    @staticmethod
    def is_weapon(item: Item, category: AuctionCategory) -> bool:
        if category == AuctionCategory.WEAPON:
            return True

        return False

    @staticmethod
    def make_weapon(item: Item) -> Weapon:
        # Assumes that the item can be made into a weapon

        reforge: str = item.nbt_data["i"][0]["tag"]["ExtraAttributes"].get(
            "modifier", ""
        )

        hot_potatoes: int = item.nbt_data["i"][0]["tag"]["ExtraAttributes"].get(
            "hot_potato_count", 0
        )

        dungoun_stars: int = item.nbt_data["i"][0]["tag"]["ExtraAttributes"].get(
            "upgrade_level", 0
        )

        return Weapon(
            lore=item.lore,
            extra=item.extra,
            nbt_data=item.nbt_data,
            item_stats=ItemStats(
                name=item.name,
                rarity=item.rarity,
                modifer=reforge,
                enchantments=Item.get_enchantments(item),
                hot_potatoes=hot_potatoes,
                dungoun_stars=dungoun_stars,
            ),
        )

    def __repr__(self):
        return f"Weapon({self.rarity.__repr__()} {self.name})".replace("  ", " ")
