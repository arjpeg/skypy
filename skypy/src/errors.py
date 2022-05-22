"""Some common errors for the SkyPy package."""


class SkyPyError(Exception):
    """
    A base class for all SkyPy errors.
    """

    pass


class AHPageDoesntExistError(SkyPyError):
    """
    An error that occurs when the page does not exist.
    """

    def __init__(self, page_no: int, max_page_no: int | None) -> None:
        super().__init__(
            f"Page {page_no} does not exist"
            + (f" (current max page: {max_page_no})" if max_page_no else "")
        )
