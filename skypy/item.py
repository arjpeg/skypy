from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import colorama

from skypy.utils import convert_to_greek_numeral, parse_nbt_data, remove_color_codes


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


@dataclass
class Enchant:
    name: str
    level: int

    def __repr__(self) -> str:
        if self.name.lower().startswith("ultimate"):
            color = colorama.Fore.MAGENTA
        else:
            color = colorama.Fore.LIGHTCYAN_EX

        return f"{color}{self.name} {convert_to_greek_numeral(self.level)}{colorama.Fore.RESET}"


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
