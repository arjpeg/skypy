from __future__ import annotations

from typing import Any

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

    @staticmethod
    def is_book(item: Item) -> bool:
        if item.name == "Enchanted Book":
            return True

        return False

    @staticmethod
    def make_book(item: Item) -> EnchantedBook:
        if not EnchantedBook.is_book(item):
            raise ValueError("Item can't be made into an enchanted book.")
        # get the level from the extra information
        nbt_enchants: dict[str, int] = item.nbt_data["i"][0]["tag"]["ExtraAttributes"][
            "enchantments"
        ]
        enchants: list[Enchant] = [
            Enchant(name, level) for name, level in nbt_enchants.items()
        ]

        return EnchantedBook(
            enchants=enchants,
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
