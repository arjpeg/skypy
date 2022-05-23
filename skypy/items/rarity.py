from enum import Enum

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
