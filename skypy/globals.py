api_key: str = ""


def set_api_key(_api_key: str) -> None:
    """
    Set the API key.
    """
    globals()["api_key"] = _api_key
