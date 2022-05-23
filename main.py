import colorama

import skypy
from skypy.items.weapon import Weapon

# from skypy.item import EnchantedBook

skypy.init()

auction_house = skypy.AuctionHouse()

page1 = auction_house.get_page()

# Get the first book in the first page
for auction in auction_house.get_auctions(page1):
    if isinstance(auction.item, Weapon):
        print(
            auction.item,
            f"for {colorama.Fore.YELLOW}{auction.highest_bid:,} coins{colorama.Fore.RESET}",
            "sold by",
            skypy.utils.get_minecraft_username(auction.seller_uuid),
        )
        break
