import json
import re
import argparse
from math import ceil
from collections import OrderedDict
from os.path import join as path_join
from PIL import Image, ImageFont, ImageDraw, ImageChops

from app.models.fif import FifFile, FifEntry

NONE_CHARACTER_REGEX = r"(\{color:(\d+)\})|(\{\/color\})|(\{clear\})|(\{arrow\})|(\{speed:(\d+)\})|(\{wait:(\d+)\})|(\n)|(\\u[a-fA-F0-9]{4})"


def px_to_pt(pt):
    return round(pt / 1.25)


def get_characters(path, entry_wrapper_index=0):
    with open(path, "r", encoding="utf-8") as json_f:
        obj = json.load(json_f)
        character_set = set()
        for (
            c
        ) in "1234567890-:;,.&()!/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            character_set.add(c)
        for entry in obj["Entries"][entry_wrapper_index]:
            entry = re.sub(NONE_CHARACTER_REGEX, "", entry, re.M)
            for character in entry:
                character_set.add(character)
        characters = sorted(list(character_set))
        return characters


def update_fif(fif, characters):
    fif.entry_count = len(characters)

    fif.characters_per_row = fif.width // fif.column_width
    fif.row_count = fif.height // fif.row_height

    fif.characters_per_texture = fif.characters_per_row * fif.row_count
    fif.texture_count = ceil(fif.entry_count / fif.characters_per_texture)


def generate_entries(fif, characters, font, font_size, color, font_top_margin, output):
    character_index = 0
    new_entries = OrderedDict()

    for texture_index in range(fif.texture_count):
        texture_character_count = 0
        pos_width = 0
        pos_height = 0

        image = Image.new("RGB", (fif.width, fif.height), (0, 0, 0))
        alpha = Image.new("L", image.size, "black")
        imtext = Image.new("L", image.size, 0)
        drtext = ImageDraw.Draw(imtext)

        while (
            texture_character_count < fif.characters_per_texture
            and character_index < len(characters)
        ):
            character = characters[character_index]
            glyph_size = font.getsize(character)
            pos = (
                pos_width + 1,
                round(pos_height - font_size * 0.1 + 1) + font_top_margin,
            )
            drtext.text(pos, character, font=font, fill="white")

            if character.isspace():
                new_entries[character] = FifEntry(0, 10, 1)
            if character.isalpha():
                new_entries[character] = FifEntry(0, 0, glyph_size[0])
            else:
                new_entries[character] = FifEntry(0, 2, glyph_size[0])

            character_index += 1
            texture_character_count += 1
            if texture_character_count % fif.characters_per_row == 0:
                pos_width = 0
                pos_height += fif.row_height
            else:
                pos_width += fif.column_width

        alpha = ImageChops.lighter(alpha, imtext)
        solidcolor = Image.new("RGBA", image.size, color)
        immask = Image.eval(imtext, lambda p: 255 * (int(p != 0)))
        image = Image.composite(solidcolor, image, immask)
        image.putalpha(alpha)
        image.save(output + f"_{texture_index:02}.dds.png", "PNG")

    return new_entries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate font json file from text json"
    )
    parser.add_argument("text_json", help="File path of text json")
    parser.add_argument("output_dir", help="Directory path to save generated data")
    parser.add_argument("name", help="File Name without extension of generated data")
    parser.add_argument(
        "-f",
        "--fif_json",
        help="File path of fif json to copy properties",
        required=True,
    )
    parser.add_argument(
        "-g", "--font", help="Font file path to generate font image", required=True
    )
    parser.add_argument(
        "-i",
        "--index",
        help="Index of entry in text json (default 0)",
        default=0,
        type=int,
    )
    parser.add_argument("-c", "--color", help="Color of font image", default="#ffffff")
    parser.add_argument(
        "--font_top_margin", help="Top margin for font", default=0, type=int
    )
    parser.add_argument(
        "--font_rel_size", help="Font relative size factor", default=0, type=int
    )
    args = parser.parse_args()

    output = path_join(args.output_dir, args.name)
    with open(args.fif_json, "r", encoding="utf-8") as json_f:
        obj = json.load(json_f, object_pairs_hook=OrderedDict)
        fif = FifFile.import_obj(obj)
    font_size = px_to_pt(fif.character_height) - 2 + args.font_rel_size
    font = ImageFont.truetype(args.font, size=font_size)
    characters = get_characters(args.text_json, args.index)

    update_fif(fif, characters)
    new_entries = generate_entries(
        fif, characters, font, font_size, args.color, args.font_top_margin, output
    )
    fif.entries = new_entries
    fif.save(output + ".fif")
