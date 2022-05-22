import colorama
import skypy
from skypy.auction import AuctionCategory

# from skypy.item import EnchantedBook

skypy.init()

auction_house = skypy.AuctionHouse()

page1 = auction_house.get_page(2)

# Get the first book in the first page
for auction in auction_house.get_auctions(page1):
    if auction.category == AuctionCategory.WEAPON:
        print(
            auction.item,
            f"@{colorama.Fore.YELLOW}{auction.highest_bid:,} coins{colorama.Fore.RESET}",
        )

# print(auction_house.get_auction(page1, 2))
# print(auction_house.get_auction(page1, 2).item.nbt_data)
