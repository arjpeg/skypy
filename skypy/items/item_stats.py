from dataclasses import dataclass

from skypy.items.enchant import Enchant
from skypy.items.rarity import ItemRarity


@dataclass
class ItemStats:
    """
    A class for an item's stats.
    """

    name: str
    rarity: ItemRarity
    modifer: str  # also known as it's reforge
    enchantments: list[Enchant]

    hot_potatoes: int = 0
    dungoun_stars: int = 0
