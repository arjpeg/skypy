"""
A small library to get the data from the Skyblock API.
"""
import os

from dotenv import load_dotenv  # type: ignore

import skypy.globals as _globals
from skypy.auction_house import AuctionHouse


def init(api_key: str | None = None) -> None:
    """
    Initialize the library.
    """

    load_dotenv()

    if api_key:
        _globals.set_api_key(api_key)
    elif os.getenv("API_KEY"):
        _globals.set_api_key(os.getenv("API_KEY"))  # type: ignore
    else:
        raise ValueError("No API key given or found in the .env file.")

    AuctionHouse.api_key = _globals.api_key
