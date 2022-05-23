from typing import Any

from skypy.items.rarity import ItemRarity
from skypy.utils import parse_nbt_data, remove_color_codes


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

    def __repr__(self):
        return f"Item({self.name} ({self.rarity.__repr__()}) {remove_color_codes(self.extra)})"
