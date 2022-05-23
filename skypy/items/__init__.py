"""
All item categories that are used in the Hypixel API.
"""
from __future__ import annotations
from skypy.items.enchanted_book import EnchantedBook

from skypy.items.item import Item


def make_correct_item(item: Item) -> Item:
    if EnchantedBook.is_book(item):
        return EnchantedBook.make_book(item)

    return item
