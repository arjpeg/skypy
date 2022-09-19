import asyncio
import time
from typing import Any

import httpx
import requests


async def get_data(client: httpx.AsyncClient, url: str) -> dict[str, Any]:
    resp = await client.get(url)  # type: ignore
    json_data = resp.json()

    return json_data


async def get_all_auctions_in_range(
    client: httpx.AsyncClient, _range: tuple[int, int]
) -> tuple[dict[str, Any]]:
    tasks: list[asyncio.Task[dict[str, Any]]] = [
        asyncio.create_task(
            get_data(client, f"https://api.hypixel.net/skyblock/auctions?page={i}")
        )
        for i in range(*_range)
    ]

    auction_data: tuple[dict[str, Any]] = await asyncio.gather(*tasks)  # type: ignore

    return auction_data


def sync_get_all_auctions_in_range(_range: tuple[int, int]) -> tuple[dict[str, Any]]:
    auction_data: list[requests.Response] = [
        requests.get(f"https://api.hypixel.net/skyblock/auctions?page={i}")
        for i in range(*_range)
    ]

    return [response.json() for response in auction_data]  # type: ignore


if __name__ == "__main__":
    async_client = httpx.AsyncClient()
    event_loop = asyncio.new_event_loop()

    start_time = time.perf_counter()
    event_loop.run_until_complete(get_all_auctions_in_range(async_client, (0, 60)))

    print("Async:")
    print("--- Took %s seconds ---" % (time.perf_counter() - start_time))
    event_loop.run_until_complete(async_client.aclose())

    # Close the event loop.
    event_loop.close()

    # Now run the same thing synchronously.
    start_time = time.perf_counter()
    sync_get_all_auctions_in_range((0, 60))
    print("Sync:")
    print("--- Took %s seconds ---" % (time.perf_counter() - start_time))
