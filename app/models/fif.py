from collections import OrderedDict
from os.path import getsize as get_file_size

from app.utils.io import *


class FifEntry:
    def __init__(self, left_padding, right_padding, width):
        self.left_padding = left_padding
        self.right_padding = right_padding
        self.width = width

    @classmethod
    def import_obj(cls, obj):
        return cls(obj["left_padding"], obj["right_padding"], obj["width"])

    def export_obj(self):
        return {
            "left_padding": self.left_padding,
            "right_padding": self.right_padding,
            "width": self.width,
        }


class FifFile:
    def __init__(
        self,
        entries,
        width,
        height,
        character_width,
        character_height,
        is_big_endian=False,
    ):
        self.is_big_endian = is_big_endian
        if character_width + 2 > width:
            raise Exception(
                f"character_width {character_width} is cannot be larger than width {width}"
            )
        if character_height + 2 > height:
            raise Exception(
                f"character_height {character_height} is cannot be larger than height {height}"
            )

        self.width = width
        self.height = height
        self.character_width = character_width
        self.character_height = character_height

        self.last_width = width
        self.last_height = width

        self.column_width = character_width + 2
        self.row_height = character_height + 2
        self.characters_per_row = width // character_width
        self.row_count = height // character_height
        self.characters_per_texture = self.characters_per_row * self.row_count

        self.entry_table_offset = 0
        self.entry_count = 0
        self.texture_count = 0

        if entries:
            self.entries = entries
        else:
            self.entries = OrderedDict()

    @classmethod
    def load(cls, path):
        with open(path, "rb") as f:
            entries = OrderedDict()
            magic_code = f.read(8)
            if magic_code != b"FONTDATF":
                raise IOError(f"Invalid FIF file (magic_code={magic_code})")
            is_big_endian = read_int(f) == 1

            read_byte_f = lambda: read_byte(f, is_big_endian)
            read_short_f = lambda: read_short(f, is_big_endian)
            read_int_f = lambda: read_int(f, is_big_endian)
            read_wide_char_f = lambda: read_wide_char(f, is_big_endian)

            check_1 = read_short_f()
            if check_1 != 101:
                raise IOError(f"Invalid FIF file (check_1 {check_1} != 0x65)")

            entry_table_offset = read_short_f()
            entry_count = read_int_f()

            if get_file_size(path) != entry_table_offset + (entry_count * 16):
                raise IOError(
                    f"Invalid FIF file (file size {get_file_size(path)} is mismatch with "
                    f"entry_table_offset={entry_table_offset}, entry_count={entry_count})"
                )

            characters_per_texture = read_int_f()
            texture_count = read_short_f()
            width = read_short_f()
            height = read_short_f()
            last_width = read_short_f()
            last_height = read_short_f()
            characters_per_row = read_short_f()
            row_count = read_short_f()
            character_width = read_short_f()
            character_height = read_short_f()
            column_width = read_short_f()
            row_height = read_short_f()

            check_2 = read_short_f()
            if check_2 != character_height:
                raise IOError(
                    f"Invalid FIF file (check_2 {check_2} != character_height {character_height})"
                )

            check_3 = read_byte_f()
            if check_3 != 32:
                raise IOError(f"Invalid FIF file (check_3 {check_3} != 32)")

            check_4 = read_byte_f()
            if check_4 != 1:
                raise IOError(f"Invalid FIF file (check_4 {check_4} != 1)")

            f.seek(entry_table_offset)

            for i in range(entry_count):
                left_padding = read_int_f()
                glyph_width = read_int_f()
                right_padding = read_int_f()
                character = read_wide_char_f()
                index = read_short_f()

                if index != i:
                    raise IOError(f"Invalid FIF file (index i {i} != index {index})")

                entries[character] = FifEntry(left_padding, right_padding, glyph_width)

            fif = FifFile(
                entries, width, height, character_width, character_height, is_big_endian
            )
            fif.entry_table_offset = entry_table_offset
            fif.entry_count = entry_count
            fif.texture_count = texture_count
            fif.characters_per_texture = characters_per_texture
            fif.last_width = last_width
            fif.last_height = last_height
            fif.characters_per_row = characters_per_row
            fif.row_count = row_count
            fif.column_width = column_width
            fif.row_height = row_height

            return fif

    def save(self, path):
        with open(path, "wb") as f:
            f.write(b"FONTDATF")
            if self.is_big_endian:
                write_int(f, 1)
            else:
                write_int(f, 0)

            write_byte_f = lambda v: write_byte(f, v, self.is_big_endian)
            write_short_f = lambda v: write_short(f, v, self.is_big_endian)
            write_int_f = lambda v: write_int(f, v, self.is_big_endian)
            write_wide_char_f = lambda v: write_wide_char(f, v, self.is_big_endian)

            write_short_f(101)

            write_short_f(self.entry_table_offset)
            write_int_f(self.entry_count)

            write_int_f(self.characters_per_texture)
            write_short_f(self.texture_count)
            write_short_f(self.width)
            write_short_f(self.height)
            write_short_f(self.last_width)
            write_short_f(self.last_height)
            write_short_f(self.characters_per_row)
            write_short_f(self.row_count)
            write_short_f(self.character_width)
            write_short_f(self.character_height)
            write_short_f(self.column_width)
            write_short_f(self.row_height)

            write_short_f(self.character_height)

            write_byte_f(32)
            write_byte_f(1)

            f.seek(self.entry_table_offset)

            index = 0
            for character in self.entries:
                entry = self.entries[character]
                write_int_f(entry.left_padding)
                write_int_f(entry.width)
                write_int_f(entry.right_padding)
                write_wide_char_f(character)
                write_short_f(index)
                index += 1

    def export_obj(self):
        return {
            "is_big_endian": self.is_big_endian,
            "entry_table_offset": self.entry_table_offset,
            "entry_count": self.entry_count,
            "width": self.width,
            "height": self.height,
            "character_width": self.character_width,
            "character_height": self.character_height,
            "last_width": self.last_width,
            "last_height": self.last_height,
            "column_width": self.column_width,
            "row_height": self.row_height,
            "characters_per_row": self.characters_per_row,
            "row_count": self.row_count,
            "characters_per_texture": self.characters_per_texture,
            "texture_count": self.texture_count,
            "entries": OrderedDict(
                (k, self.entries[k].export_obj()) for k in self.entries
            ),
        }

    @classmethod
    def import_obj(cls, obj):
        entries = OrderedDict()
        for entry_obj_k in obj["entries"]:
            entries[entry_obj_k] = FifEntry.import_obj(obj["entries"][entry_obj_k])

        fif = FifFile(
            entries,
            obj["width"],
            obj["height"],
            obj["character_width"],
            obj["character_height"],
            obj["is_big_endian"],
        )
        fif.entry_table_offset = obj["entry_table_offset"]
        fif.entry_count = obj["entry_count"]
        fif.texture_count = obj["texture_count"]
        fif.characters_per_texture = obj["characters_per_texture"]
        fif.last_width = obj["last_width"]
        fif.last_height = obj["last_height"]
        fif.characters_per_row = obj["characters_per_row"]
        fif.row_count = obj["row_count"]
        fif.column_width = obj["column_width"]
        fif.row_height = obj["row_height"]

        return fif
