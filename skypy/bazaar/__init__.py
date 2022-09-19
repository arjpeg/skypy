from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class BazaarProduct:
    """
    Used as a representation of a single bazaar item (has a name, and all of its orders)
    """

    item_name: str

    sell_summary: list[dict[str, float]]
    buy_summary: list[dict[str, float]]

    sell_price: float
    sell_volume: float
    sell_movingWeek: float
    sell_orders: float

    buy_price: float
    buy_volume: float
    buy_movingWeek: float
    buy_orders: int


class Bazaar:
    """
    A wrapper around Hypixel's Bazaar API.
    """

    API_URL: str = "https://api.hypixel.net/skyblock/bazaar"

    def __init__(self):
        self._network_client = httpx.Client()

    def get_all_products(self) -> dict[str, Any]:
        """
        Gets all the bazaar items from the API.
        """

        response = self._network_client.get(self.API_URL)  # type: ignore
        json = response.json()

        if json["success"] is False:
            raise ValueError(json["cause"])

        return json["products"]

    def get_item_by_id(self, item_id: str) -> BazaarProduct:
        """
        Gets a single bazaar item by its ID.
        """

        products = self.get_all_products()

        if item_id not in products:
            raise ValueError(f"Item ID {item_id} not found.")

        product = products[item_id]

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
