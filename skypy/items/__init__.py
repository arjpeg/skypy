"""
All item categories that are used in the Hypixel API.
"""
from __future__ import annotations

import skypy.items.rarity as rarity  # type: ignore
from skypy.auction.auction_category import AuctionCategory
from skypy.items.enchant import Enchant  # type: ignore
from skypy.items.enchanted_book import EnchantedBook
from skypy.items.item import Item
from skypy.items.weapon import Weapon


def make_correct_item(item: Item, category: AuctionCategory) -> Item:
    if EnchantedBook.is_book(item, category):
        return EnchantedBook.make_book(item)
    if Weapon.is_weapon(item, category):
        return Weapon.make_weapon(item)

    return item
