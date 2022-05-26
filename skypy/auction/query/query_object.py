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

        # Get all the enchant names from the item
        enchant_names = [enchantment.name for enchantment in item.get_enchantments()]

        if self.enchantments_at_min is not None:
            for enchantment in self.enchantments_at_min:
                if enchantment.name not in enchant_names:
                    return False

                for item_enchant in item.get_enchantments():
                    if enchantment.name == item_enchant.name:
                        if item_enchant.level < enchantment.level:
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

    def __repr__(self) -> str:
        string: str = "Query("

        # make the item_name property easier to read
        # ex. LIVID_DAGGER -> Livid Dagger
        human_readable_name = (
            self.item_name.replace("_", " ").title() if self.item_name else ""
        )

        if self.rarity is not None:
            string += self.rarity.__repr__() + " "

        if self.reforge is not None:
            string += self.reforge + " "

        string += human_readable_name + " "

        if self.dungoun_stars_at_min is not None:
            string += ("✪" * self.dungoun_stars_at_min) + " "

        if self.hot_potatoes_at_min is not None:
            string += ("🥔" * self.hot_potatoes_at_min) + " "

        if self.max_price is not None:
            string += f"max_price={self.max_price}, "

        if self.enchantments_at_min is not None:
            _enchant_string = ""
            for enchantment in self.enchantments_at_min:
                _enchant_string += f"{enchantment}, "

            _enchant_string = _enchant_string[:-2]

            string += f"enchantments_at_min=[{_enchant_string}], "

        # Remove the last comma and space
        string = string[:-2]

        string += ")"

        return string
