"""
A submodule for the skyblock_api package for the auction house.
"""
import asyncio
import sys
from typing import Any

import httpx
import requests
from skypy.auction.auction import Auction
from skypy.auction.query.query_object import Query
from skypy.errors import AHPageDoesntExistError
from skypy.utils.network import get_all_auctions_in_range, get_data


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

        if (
            sys.version_info[0] == 3
            and sys.version_info[1] >= 8
            and sys.platform.startswith("win")
        ):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        self._network_client: httpx.AsyncClient = httpx.AsyncClient()
        self._event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.cur_max_page: int = self.get_current_max_page()

    def get_page(self, page_number: int = 0) -> dict[str, Any]:
        """
        Get the page with the given number.
        """
        if page_number > self.cur_max_page:
            raise AHPageDoesntExistError(page_number, self.cur_max_page)

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
        Get the auctions on the given page. This is slightly faster than getting all the auctions due to the fact that we don't need to create as many Auction.from_json() calls.
        """
        if how_many_auctions_to_load == -1:
            how_many_auctions_to_load = len(page_data["auctions"])

        auctions: list[Auction] = []

        for i in range(how_many_auctions_to_load):
            auctions.append(Auction.from_json(page_data["auctions"][i]))

        return auctions

    def get_current_max_page(self) -> int:
        """
        Get the current max page.
        """

        return self._event_loop.run_until_complete(
            get_data(self._network_client, self.API_URL)
        )["totalPages"]

        # page_data: dict[str, Any] = requests.get(self.API_URL).json()
        # return page_data["totalPages"]

    def get_auction_pages(
        self, page_start: int, page_to_end: int
    ) -> list[dict[str, Any]]:
        """
        Get the auction pages with the given numbers.
        """

        return self._event_loop.run_until_complete(get_all_auctions_in_range(self._network_client, (page_start, page_to_end)))  # type: ignore

    def match_query(self, auctions: list[Auction], query: Query) -> list[Auction]:
        """
        Match the query to the auctions.
        """
        matched_auctions: list[Auction] = []

        for auction in auctions:
            if query.validate(auction):
                matched_auctions.append(auction)

        return matched_auctions
