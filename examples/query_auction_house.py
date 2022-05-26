"""
A small example to get the data from the Skyblock API using the Skypy library.
"""

import colorama
import skypy

skypy.init("{YOUR_API_KEY}")

ah = skypy.auction.AuctionHouse()

# Get the first page
first_page = ah.get_page()

# Get the first book in the first page
for auction in ah.get_auctions(first_page):
    if isinstance(auction.item, skypy.item.EnchantedBook):
        print(
            auction.item,
            f"for {colorama.Fore.YELLOW}{auction.highest_bid:,} coins{colorama.Fore.RESET}",
            "sold by",
            skypy.utils.get_minecraft_username(auction.seller_uuid),
        )

        break
