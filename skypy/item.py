from __future__ import annotations

from enum import Enum
from typing import Any

import colorama

from skypy.utils import parse_nbt_data, remove_color_codes


class ItemRarity(Enum):
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    EPIC = "EPIC"
    LEGENDARY = "LEGENDARY"
    MYTHIC = "MYTHIC"
    DIVINE = "DIVINE"
    SPECIAL = "SPECIAL"
    VERY_SPECIAL = "VERY_SPECIAL"

    def __repr__(self) -> str:
        colors: dict[str, str] = {
            "COMMON": colorama.Fore.WHITE,
            "UNCOMMON": colorama.Fore.LIGHTGREEN_EX,
            "RARE": colorama.Fore.BLUE,
            "EPIC": colorama.Fore.MAGENTA,
            "LEGENDARY": colorama.Fore.YELLOW,
            "MYTHIC": colorama.Fore.LIGHTMAGENTA_EX,
            "DIVINE": colorama.Fore.LIGHTCYAN_EX,
        }

        return f"{colors.get(self.value, colorama.Fore.WHITE)}{self.value}{colorama.Fore.RESET}"


class Item:
    def __init__(
        self,
        name: str,
        rarity: ItemRarity,
        lore: str,
        extra: str,
        nbt_data: str,
        uuid: str | None = None,
    ) -> None:
        self.name: str = name
        self.rarity: ItemRarity = rarity
        self.lore: str = remove_color_codes(lore)
        self.nbt_data: dict[str, Any] = parse_nbt_data(nbt_data)
        self.uuid: str | None = uuid
        self.extra: str = extra

    @staticmethod
    def make_correct_item(item: Item) -> Item:
        if EnchantedBook.is_book(item):
            return EnchantedBook.make_book(item)

        return item

    def __repr__(self):
        return f"Item({self.name} ({self.rarity.__repr__()}) {remove_color_codes(self.extra)})"


class EnchantedBook(Item):
    """Class to represent an enchanted book due to the way hypixel categorizes items."""

    def __init__(
        self,
        book_name: str,
        lore: str,
        extra: str,
        nbt_data: dict[str, Any],
        uuid: str | None = None,
        book_level: int = 1,
        rarity: ItemRarity = ItemRarity.COMMON,
    ) -> None:
        self.name = book_name
        self.lore = remove_color_codes(lore)
        self.extra = remove_color_codes(extra)
        self.rarity = rarity
        self.nbt_data = nbt_data
        self.uuid = uuid
        self.level = book_level

    @staticmethod
    def is_book(item: Item) -> bool:
        if item.name == "Enchanted Book":
            return True

        return False

    @staticmethod
    def make_book(item: Item) -> EnchantedBook:
        if not EnchantedBook.is_book(item):
            raise ValueError("Item can't be made into an enchanted book.")

        # get the name from the extra information
        # which looks like "Enchanted Book Enchanted Book Ultimate Wise",
        book_name: str = remove_color_codes(" ".join(item.extra.split(" ")[4:]))
        if len(book_name.split(" ")) > 3:
            print(book_name)
            print(item.extra)
            print(item.nbt_data)

        # get the level from the extra information
        enchants: dict[str, int] = item.nbt_data["i"][0]["tag"]["ExtraAttributes"][
            "enchantments"
        ]

        enchant_level: int = enchants[list(enchants.keys())[0]]

        return EnchantedBook(
            book_name=book_name,
            lore=item.lore,
            extra=item.extra,
            nbt_data=item.nbt_data,
            uuid=item.uuid,
            book_level=enchant_level,
            rarity=item.rarity,
        )

    def __repr__(self):
        return f"EnchantedBook({colorama.Fore.LIGHTCYAN_EX}{self.name} {self.level}{colorama.Fore.RESET})"
