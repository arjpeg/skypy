import skypy

skypy.init("{YOUR_API_KEY}")

# Create a Query object
query = skypy.auction.query.Query(
    max_price=100_000_100,  # 100M
    item_name="LIVID_DAGGER",
    # enchantments_at_min=[skypy.item.Enchant("ultimate_one_for_all", 1)],
    dungoun_stars_at_min=1,
)

auction_house = skypy.auction.AuctionHouse()
first_page = auction_house.get_page(0)
auctions = auction_house.get_auctions(first_page)

for auction in auction_house.match_query(auctions, query):
    print(auction.item)
    print(auction.item.get_enchantments())
