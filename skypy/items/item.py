from typing import Any

from skypy.items.enchant import Enchant
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
        self.nbt_data: dict[str, Any] = parse_nbt_data(nbt_data)
        self.id: str = self.nbt_data["i"][0]["tag"]["ExtraAttributes"]["id"]
        self.rarity: ItemRarity = rarity
        self.lore: str = remove_color_codes(lore)
        self.uuid: str | None = uuid
        self.extra: str = extra

    def get_enchantments(self) -> list[Enchant]:
        return [
            Enchant(name, level)
            for name, level in self.nbt_data["i"][0]["tag"]["ExtraAttributes"]
            .get("enchantments", {})
            .items()
        ]

    def __repr__(self):
        return f"Item({self.name} ({self.rarity.__repr__()}))"
