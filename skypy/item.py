from enum import Enum
from typing import Any

import colorama


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
        nbt_data: dict[str, Any],
        uuid: str | None = None,
    ) -> None:
        self.name: str = name
        self.rarity: ItemRarity = rarity
        self.lore: str = lore
        self.nbt_data: dict[str, Any] = nbt_data
        self.uuid: str | None = uuid

        # if name == "Enchanted Book":

    def __str__(self):
        return f"{self.name} (x{self.nbt_data})"
