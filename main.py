import skypy.src as skypy

skypy.init()

auction_house = skypy.AuctionHouse()

page1 = auction_house.get_page(0)

print("The first auction in page 1 is:")
print(auction_house.get_auction(page1, 0))
