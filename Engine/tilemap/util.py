import json


def load_sprite_fusion_map(file_path: str) -> json:
    """
    Load a Sprite Fusion map from a JSON file.
    :param file_path: The path to the JSON file.
    :return: The loaded map as a JSON object.
    """
    with open(file_path, "r") as file:
        fusion_map = json.load(file)
    return fusion_map


def fusion_to_rich_tilemap(fusion_map: json, tilemap):
    """
    Convert a Sprite Fusion (https://www.spritefusion.com/editor) map to a rich tilemap.
    :param fusion_map: The fusion map to convert.
    :param tilemap: The tilemap to convert to.
    :return: The converted rich tilemap.
    """
    rich_tilemap = []
    for row in fusion_map:
        rich_row = []
        for cell in row:
            if cell == 0:
                rich_row.append(tilemap[0])
            else:
                rich_row.append(tilemap[cell])
        rich_tilemap.append(rich_row)
    return rich_tilemap
