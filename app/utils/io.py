from struct import unpack, pack


def struct_prefix(is_big_endian=False):
    return ">" if is_big_endian else "<"


def read_char(f, is_big_endian=False):
    return unpack(struct_prefix(is_big_endian) + "c", f.read(1))[0]


def read_wide_char(f, is_big_endian=False):
    c = unpack(struct_prefix(is_big_endian) + "H", f.read(2))[0]
    return chr(c)


def read_byte(f, is_big_endian=False):
    return unpack(struct_prefix(is_big_endian) + "b", f.read(1))[0]


def read_short(f, is_big_endian=False):
    return unpack(struct_prefix(is_big_endian) + "h", f.read(2))[0]


def read_int(f, is_big_endian=False):
    return unpack(struct_prefix(is_big_endian) + "i", f.read(4))[0]


def write_char(f, v, is_big_endian=False):
    return f.write(pack(struct_prefix(is_big_endian) + "c", v))


def write_wide_char(f, v, is_big_endian=False):
    c = ord(v)
    return f.write(pack(struct_prefix(is_big_endian) + "H", c))


def write_byte(f, v, is_big_endian=False):
    return f.write(pack(struct_prefix(is_big_endian) + "b", v))


def write_short(f, v, is_big_endian=False):
    return f.write(pack(struct_prefix(is_big_endian) + "h", v))


def write_int(f, v, is_big_endian=False):
    return f.write(pack(struct_prefix(is_big_endian) + "i", v))
