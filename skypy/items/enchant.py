from dataclasses import dataclass

import colorama
from skypy.utils import convert_to_greek_numeral


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
