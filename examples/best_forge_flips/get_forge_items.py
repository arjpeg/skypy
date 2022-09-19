"""
Heya there!

This file is just to parse the forge items in the best_forge_flips.txt file.
While I could have hardcoded them, 
    a) I'm lazy (there are too many items)
    b) The products are constantly changing

If I haven't updated the forge_products.txt file, then go to
    https://hypixel-skyblock.fandom.com/wiki/The_Forge
    and copy the items into the forge_products.txt file.
    (note that you have to seperately copy the Refine Ores section, and Item Casting section)
    (also note that you shouldn't copy the heading for each section)
    so the start of the file should look like this:
    
    Refined Diamond	Epic	
    Enchanted Diamond Block 2x Enchanted Diamond Block
    8 hours	2
    ...
"""


from dataclasses import dataclass


@dataclass
class ForgeItem:
    name: str
    duration: float  # in terms of hours
    items_required: list[tuple[str, int]]


def idfy(x: str) -> str:
    return x.upper().replace(" ", "_")


try:
    with open("forge_products.txt", "r") as f:
        lines = [line.replace("\t", " ").strip("\n") for line in f.readlines()]
except FileNotFoundError:
    print(
        "Please copy the forge_products.txt file into the examples/best_forge_flips folder."
    )
    exit(1)

forge_items: list[ForgeItem] = []


for (idx, line) in enumerate(lines):
    # check there if there is a digit anywhere in the line
    if any(char.isdigit() for char in line):
        continue

    cur_item = ForgeItem(" ".join(line.split()[:-1]), 0, [])

    for _line in lines[idx + 1 :]:
        time_words: list[str] = [
            "second",
            "seconds",
            "minute",
            "minutes",
            "hour",
            "hours",
            "day",
            "days",
        ]

        # If the line is the last line
        if any(x in _line.lower() for x in time_words):
            _line_without_tier = _line[:-2].split(" ")
            time_in_hours: float = 0

            for duration in zip(_line_without_tier[::2], _line_without_tier[1::2]):
                duration = duration[0], duration[1].lower()

                if duration[1] not in time_words:
                    break

                if duration[1] == "second" or duration[1] == "seconds":
                    time_in_hours += float(duration[0]) / 3600
                if duration[1] == "minute" or duration[1] == "minutes":
                    time_in_hours += float(duration[0]) / 60
                elif duration[1] == "hour" or duration[1] == "hours":
                    time_in_hours += float(duration[0])
                elif duration[1] == "days" or duration[1] == "day":
                    time_in_hours += float(duration[0]) * 24

            cur_item.duration = time_in_hours
            forge_items.append(cur_item)
            break
        else:
            _line_split = _line.split(" ")

            if "coins" in _line:
                _line_split = [
                    "".join(char for char in x if ord(char) < 128) for x in _line_split
                ]

                cur_item.items_required.append(
                    ("coins", int(_line_split[2][13:].replace(",", "")))
                )
                continue

            ingredient_name = " ".join(_line_split[: len(_line_split) // 2])
            ingredient_amount = int(_line_split[len(_line_split) // 2][:-1])

            cur_item.items_required.append((ingredient_name, ingredient_amount))
