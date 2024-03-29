"""
A small library to get the data from the Skyblock API.
"""
import os

from dotenv import load_dotenv  # type: ignore

import skypy.auction as auction  # type: ignore
import skypy.bazaar as bazaar  # type: ignore
import skypy.globals as _globals
import skypy.items as item  # type: ignore
import skypy.utils as utils  # type: ignore


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

    auction.AuctionHouse.api_key = _globals.api_key
