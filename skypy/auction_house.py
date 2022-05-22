"""
A submodule for the skyblock_api package for the auction house.
"""
from typing import Any

import requests
from skypy.auction import Auction
from skypy.errors import AHPageDoesntExistError


class AuctionHouse:
    """
    A class for the auction house.
    """

    API_URL = "https://api.hypixel.net/skyblock/auctions"
    api_key = ""

    def __init__(self, _api_key: str | None = None) -> None:
        """
        Initialize the auction house for viewing.
        """
        if _api_key:
            self.api_key = _api_key

        elif self.api_key == "":
            raise ValueError(
                "No API key given. This maybe be because you didn't initialize the library. (Run `skypy.init()`)"
            )

        self._cur_max_page: int = self.get_current_max_page()

    def get_page(self, page_number: int = 0) -> dict[str, Any]:
        """
        Get the page with the given number.
        """
        if page_number > self._cur_max_page:
            raise AHPageDoesntExistError(page_number, self._cur_max_page)

        url = (
            f"{self.API_URL}?key={self.api_key}&page={page_number}"
            if page_number > 0
            else self.API_URL
        )
        response = requests.get(url)

        return response.json()

    def get_auctions(
        self, page_data: dict[str, Any], how_many_auctions_to_load: int = -1
    ) -> list[Auction]:
        """
        Get the auctions on the given page.
        """
        if how_many_auctions_to_load == -1:
            how_many_auctions_to_load = len(page_data["auctions"])

        auctions: list[Auction] = []

        for i in range(how_many_auctions_to_load):
            auctions.append(Auction.from_json(page_data["auctions"][i]))

        return auctions

    def get_auction(self, page_data: dict[str, Any], auction_no: int) -> Auction:
        """
        Get the auction with the given number.
        """
        if auction_no > len(page_data["auctions"]):
            raise AHPageDoesntExistError(auction_no, len(page_data["auctions"]))

        return Auction.from_json(page_data["auctions"][auction_no])

    def get_current_max_page(self) -> int:
        """
        Get the current max page.
        """

        page_data: dict[str, Any] = requests.get(self.API_URL).json()
        return page_data["totalPages"]
