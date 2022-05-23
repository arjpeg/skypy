from dataclasses import dataclass, field

from skypy.auction.auction import Auction
from skypy.auction.auction_category import AuctionCategory
from skypy.items.enchant import Enchant
from skypy.items.rarity import ItemRarity
from skypy.items.weapon import Weapon


@dataclass
class Query:
    """
    An object used to more easily query the hypixel auction house api.
    """

    max_price: int | None = None
    item_name: str | None = None

    enchantments_at_min: list[Enchant] | None = field(default_factory=list)
    hot_potatoes_at_min: int | None = None
    dungoun_stars_at_min: int | None = None

    rarity: ItemRarity | None = None
    reforge: str | None = None

    def validate(self, auction: Auction) -> bool:
        """
        Check if the given auction matches the validation passed in the Query object.
        """
        item = auction.item

        if self.item_name is not None and self.item_name != item.id:
            return False

        if self.rarity is not None and self.rarity != item.rarity:
            return False

        if self.max_price is not None and self.max_price <= auction.highest_bid:
            return False

        if self.enchantments_at_min is not None:
            for enchantment in self.enchantments_at_min:
                if enchantment not in item.get_enchantments():
                    return False

        if (
            self.hot_potatoes_at_min is not None
            or self.dungoun_stars_at_min is not None
        ):
            # The item is a weapon or armor
            if auction.category != AuctionCategory.WEAPON:
                return False

            weapon = Weapon.make_weapon(item)

            if (
                self.hot_potatoes_at_min is not None
                and self.hot_potatoes_at_min > weapon.hot_potatoes
            ):
                return False

            if (
                self.dungoun_stars_at_min is not None
                and self.dungoun_stars_at_min > weapon.dungoun_stars
            ):
                return False

        return True
