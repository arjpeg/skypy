from __future__ import annotations

from typing import Any

from skypy.auction.auction_category import AuctionCategory
from skypy.items.enchant import Enchant
from skypy.items.item import Item
from skypy.items.rarity import ItemRarity
from skypy.utils import remove_color_codes


class EnchantedBook(Item):
    """Class to represent an enchanted book due to the way hypixel categorizes items."""

    def __init__(
        self,
        lore: str,
        extra: str,
        enchants: list[Enchant],
        nbt_data: dict[str, Any],
        uuid: str | None = None,
        rarity: ItemRarity = ItemRarity.COMMON,
    ) -> None:
        self.enchants: list[Enchant] = enchants
        self.lore = remove_color_codes(lore)
        self.extra = remove_color_codes(extra)
        self.rarity = rarity
        self.nbt_data = nbt_data
        self.uuid = uuid

        self.id = self.nbt_data["i"][0]["tag"]["ExtraAttributes"]["id"]

    @staticmethod
    def is_book(item: Item, category: AuctionCategory) -> bool:
        if item.name == "Enchanted Book" and category == AuctionCategory.CONSUMABLES:
            return True

        return False

    @staticmethod
    def make_book(item: Item) -> EnchantedBook:
        # Assumes that the item can be made into an enchanted book

        return EnchantedBook(
            enchants=Item.get_enchantments(item),
            lore=item.lore,
            extra=item.extra,
            nbt_data=item.nbt_data,
            uuid=item.uuid,
            rarity=item.rarity,
        )

    def __repr__(self):
        string = ""

        for enchant in self.enchants:
            string += f"{enchant.__repr__()}, "

        return f"EnchantedBook({string[:-2]})"
