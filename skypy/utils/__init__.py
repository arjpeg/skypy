"""
Utilities for the SkyPy package such as cleaning text, etc.
"""

import base64
import io
from typing import Any

import requests  # type: ignore
from nbt import nbt  # type: ignore
from nbt.nbt import TAG_Compound, TAG_List  # type: ignore


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


def unpack_nbt(tag: Any) -> dict[str, Any]:
    """
    Unpack the given NBT data into a string.
    """

    if isinstance(tag, TAG_List):
        return [unpack_nbt(i) for i in tag.tags]  # type: ignore
    elif isinstance(tag, TAG_Compound):
        return dict((i.name, unpack_nbt(i)) for i in tag.tags)  # type: ignore
    else:
        return tag.value


def parse_nbt_data(data: str) -> dict[str, Any]:
    """
    Parse the given NBT data into a dictionary.
    """

    nbt_file = nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(data)))

    return unpack_nbt(nbt_file)


def convert_to_greek_numeral(num: int) -> str:
    """
    Convert the given number to a greek numeral upto 10.
    """

    if num == 1:
        return "I"
    elif num == 2:
        return "II"
    elif num == 3:
        return "III"
    elif num == 4:
        return "IV"
    elif num == 5:
        return "V"
    elif num == 6:
        return "VI"
    elif num == 7:
        return "VII"
    elif num == 8:
        return "VIII"
    elif num == 9:
        return "IX"
    elif num == 10:
        return "X"

    return f"(UNKNOWN NUMBER {num})"


def get_minecraft_username(uuid: str) -> str:
    """
    Get the Minecraft username for the given UUID.
    """
    req = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names")

    return req.json()[0]["name"]
