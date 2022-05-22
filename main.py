import skypy
from skypy.item import EnchantedBook

skypy.init()

auction_house = skypy.AuctionHouse()

page1 = auction_house.get_page(0)

# Get the first book in the first page
for auction in auction_house.get_auctions(page1):
    if isinstance(auction.item, EnchantedBook):
        print(auction.item, "for at minimum", f"{auction.highest_bid:,} coins")

# print(auction_house.get_auction(page1, 2))
# print(auction_house.get_auction(page1, 2).item.nbt_data)
