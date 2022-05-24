import colorama
import skypy

# from skypy.items.rarity import ItemRarity

skypy.init("{YOUR_API_KEY}")

# Create a Query object
query_with_enchants = skypy.auction.query.Query(
    item_name="LIVID_DAGGER",
    enchantments_at_min=[
        skypy.item.Enchant(name="ultimate_soul_eater", level=1),
    ],
)

query_without_enchants = skypy.auction.query.Query(
    item_name="LIVID_DAGGER",
)

auction_house = skypy.auction.AuctionHouse()
first_page = auction_house.get_page(0)
auctions = auction_house.get_auctions(first_page)

matches_with_enchants = auction_house.match_query(auctions, query_with_enchants)
matches_without_enchants = auction_house.match_query(auctions, query_without_enchants)

print("Querying the auction house for:", query_with_enchants)

if len(matches_with_enchants) == 0:
    print("No matches found for query")

for auction in matches_with_enchants:
    print(
        auction.item,
        f"{colorama.Fore.MAGENTA}/viewauction {auction.uuid} {colorama.Fore.RESET}",
    )
    print(auction.item.get_enchantments())


print(
    "There are",
    abs(len(matches_with_enchants) - len(matches_without_enchants)),
    "more matches without enchantments",
)

print(matches_with_enchants[0].item.nbt_data)
