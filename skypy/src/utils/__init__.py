"""
Utilities for the SkyPy package such as cleaning text, etc.
"""


def remove_color_codes(text: str) -> str:
    """
    Remove color codes from the given text.
    """
    res: str = ""
    skip_next: bool = False

    for char in text:
        if char == "\u00A7":
            skip_next = True
            continue

        if not skip_next:
            res += char

        skip_next = False

    return res
