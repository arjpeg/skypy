"""
Hello!

This file is meant to demonstrate how to use the skypy library, to get the best forge flips.
"""
import time
from typing import Any

import colorama
import skypy
from skypy.bazaar import BazaarProduct

from get_forge_items import forge_items

print(
    f"{colorama.Fore.MAGENTA}Found {colorama.Fore.YELLOW}{len(forge_items)}{colorama.Fore.MAGENTA} items from the {colorama.Fore.CYAN}get_forge_items{colorama.Fore.MAGENTA} file!{colorama.Fore.RESET}"
)


def idfy(name: str) -> str:
    """
    Used to convert a string to a valid identifier.
    """
    return name.upper().replace(" ", "_")


def deidfy(name: str) -> str:
    """
    Used to convert a string from a valid identifier to a more human readable string.
    """
    return " ".join(
        map(lambda x: x.capitalize(), name.lower().replace("_", " ").split())
    )


skypy.init("{YOUR_API_KEY_HERE}")

bazaar = skypy.bazaar.Bazaar()
auction_house = skypy.auction.AuctionHouse()

gemstone_names = [
    "RUBY",
    "AMBER",
    "SAPPHIRE",
    "JADE",
    "AMETHYST",
    "TOPAZ",
    "JASPER",
    "OPAL",
]


def to_bazaar_product(product: dict[str, Any]) -> BazaarProduct:
    """
    Converts a dictionary from the get_forge_items file to a BazaarProduct object.
    """
    return BazaarProduct(
        item_name=product["product_id"],
        sell_summary=product["sell_summary"],
        buy_summary=product["buy_summary"],
        sell_price=product["quick_status"]["sellPrice"],
        sell_volume=product["quick_status"]["sellVolume"],
        sell_movingWeek=product["quick_status"]["sellMovingWeek"],
        sell_orders=product["quick_status"]["sellOrders"],
        buy_price=product["quick_status"]["buyPrice"],
        buy_volume=product["quick_status"]["buyVolume"],
        buy_movingWeek=product["quick_status"]["buyMovingWeek"],
        buy_orders=product["quick_status"]["buyOrders"],
    )


bazaar_items: list[BazaarProduct] = [
    to_bazaar_product(product) for product in bazaar.get_all_products().values()
]
bazaar_item_names: list[str] = [product.item_name for product in bazaar_items]

print(f"{colorama.Fore.GREEN}Successfully queried the Bazaar!{colorama.Fore.RESET}")

auction_house_auctions: list[skypy.auction.Auction] = []

ah_pages_to_query = int(
    input(
        f"{colorama.Fore.CYAN}How many Auction House pages do you want to query {colorama.Fore.YELLOW}(more pages = more accurate, but takes longer) {colorama.Fore.LIGHTBLACK_EX}(Current max AH Page is {auction_house.get_current_max_page()})?{colorama.Fore.RESET} "
    )
)

for page in auction_house.get_auction_pages(0, ah_pages_to_query):
    auction_house_auctions.extend(auction_house.get_auctions(page))

print(
    f"{colorama.Fore.GREEN}Successfully queried the Auction House!{colorama.Fore.RESET}"
)

ingredients: list[str] = []

for item in forge_items:
    ingredients.extend([ingredient[0] for ingredient in item.items_required])

item_names = [item.name for item in forge_items]
item_names.extend(ingredients)

item_names_idfyd: list[str] = [idfy(name) for name in item_names]


########################################################################
############           THE INGREDIENT COSTS           ##################
########################################################################

# To accurately caclulate the profits of each item, we need to go through
# each item, and go through each of its ingredients.

item_prices: dict[str, float] = {}

for bazaar_product in bazaar_items:
    item_price: float = round(
        bazaar_items[
            bazaar_item_names.index(idfy(bazaar_product.item_name))
        ].sell_price,
        2,
    )

    print(
        f"{colorama.Fore.CYAN}{bazaar_product.item_name} {any(gemstone_name in bazaar_product.item_name for gemstone_name in gemstone_names)}"
    )

    if any(
        gemstone_name in bazaar_product.item_name for gemstone_name in gemstone_names
    ):
        item_prices[
            deidfy(bazaar_product.item_name).replace("Gem", "Gemstone")
        ] = item_price
        continue

    if bazaar_product.item_name in item_names_idfyd:
        item_prices[deidfy(bazaar_product.item_name)] = item_price

for auction in auction_house_auctions:
    if not auction.is_bin:
        continue

    if "[Lvl" in auction.item.name:
        # This signifies that the item is a pet, so we change its name to
        # {PETNAME} Pet
        pet_name = ""
        in_pet_lvl: bool = True

        for idx, char in enumerate(auction.item.name):
            if char == "]":
                in_pet_lvl = False
                continue

            if not in_pet_lvl:
                pet_name = auction.item.name[idx + 1 :] + " Pet"
                break

        if pet_name in item_names:
            item_prices[pet_name] = min(
                item_prices.get(pet_name, float("inf")), auction.highest_bid
            )

    elif auction.item.name in item_names:
        item_prices[auction.item.name] = min(
            item_prices.get(auction.item.name, float("inf")), auction.highest_bid
        )


print(item_prices)

final_profits: dict[str, float] = {}

for item in forge_items:
    # get the number of hours the item takes
    try:
        # Calculate the profit of the item based on its sell price, and how long it takes
        item_profit: float = round((24 / item.duration) * item_prices[item.name], 2)

        try:
            # Now calculate the ingredient costs of the item
            item_ingredient_costs: float = sum(
                item_prices[ingredient[0]] * ingredient[1]
                for ingredient in item.items_required
            )
        except KeyError:
            print(
                f"{colorama.Fore.RED}Could not find ingredient '{item.name}' for item '{item.name}'"
            )
            continue

        print(
            f"{colorama.Fore.LIGHTBLUE_EX}{item.name}: takes {colorama.Fore.YELLOW}{item.duration} hours{colorama.Fore.WHITE} and sells for {colorama.Fore.LIGHTYELLOW_EX}{item_prices[item.name]:,} coins but costs {colorama.Fore.LIGHTRED_EX}{item_ingredient_costs:,.2f} coins to make,{colorama.Fore.WHITE} meaning you would earn around {colorama.Fore.LIGHTYELLOW_EX}{item_profit-item_ingredient_costs:,.2f} coins / hour.{colorama.Fore.RESET}"
        )

        final_profits[item.name] = item_profit - item_ingredient_costs
    except KeyError as err:
        print(
            f"{colorama.Fore.RED}Couldn't find '{item.name}' in the Bazaar/AH{colorama.Fore.RESET}",
            item_prices.get(item.name, ""),
            err,
        )


print(f"{colorama.Fore.LIGHTMAGENTA_EX}So, the best item to forge is...")
time.sleep(3.5)

best_item: str = ""

for name, profit in final_profits.items():
    if profit > final_profits.get(best_item, 0):
        best_item = name


print(
    f"{colorama.Fore.LIGHTMAGENTA_EX}{best_item}! With profits around {colorama.Fore.LIGHTYELLOW_EX}{final_profits[best_item]:,.2f} coins / hour{colorama.Fore.RESET}"
)
