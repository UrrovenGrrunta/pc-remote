# UG-PEP: FAILED IMPLEMENTATION ARCHIVE
#
# This file contains previous experimental implementations.
# It is intentionally preserved as development history.
#
# Do not "fix" failed code in this file.
# Failures are documentation.

import os
import struct
import snappy

from pathlib import Path


SST_PATH = (
    Path(os.getenv("APPDATA"))
    / "hydralauncher"
    / "hydra-db-backup-2026-08-18"
    / "000232.ldb"
)


def read_varint(data, offset):
    value = 0
    shift = 0

    while True:
        byte = data[offset]
        offset += 1

        value |= (byte & 0x7F) << shift

        if not byte & 0x80:
            return value, offset

        shift += 7


with open(SST_PATH, "rb") as file:
    file.seek(-48, 2)
    footer = file.read(48)

offset = 0
meta_offset, offset = read_varint(footer, offset)
meta_size, offset = read_varint(footer, offset)

index_offset, offset = read_varint(footer, offset)
index_size, offset = read_varint(footer, offset)

with open(SST_PATH, "rb") as file:
    file.seek(meta_offset)
    meta_block = file.read(meta_size)
    meta_trailer = file.read(5)

with open(SST_PATH, "rb") as file:
    file.seek(index_offset)
    index_block = file.read(index_size)
    index_trailer = file.read(5)

if index_trailer[0] == 1:
    index_block = snappy.decompress(index_block)

restart_count = struct.unpack("<I", index_block[-4:])[0]
restart_array_offset = len(index_block) - (restart_count * 4) - 4
entries_data = index_block[:restart_array_offset]

offset = 0

shared, offset = read_varint(entries_data, offset)
non_shared, offset = read_varint(entries_data, offset)
value_length, offset = read_varint(entries_data, offset)

key_bytes = entries_data[offset:offset + non_shared]

value_start = offset + non_shared
value_end = value_start + value_length
value_bytes = entries_data[value_start:value_end]

data = value_bytes
offset = 0

block_offset, offset = read_varint(data, offset)
block_size, offset = read_varint(data, offset)

with open(SST_PATH, "rb") as file:
    file.seek(block_offset)
    data_block = file.read(block_size)
    data_trail = file.read(5)

if data_trail[0] == 1:
    data_block = snappy.decompress(data_block)

restart_count = struct.unpack("<I", data_block[-4:])[0]
restart_array_offset = (
    len(data_block)
    - (restart_count * 4)
    - 4
)
entries_data = data_block[:restart_array_offset]

offset = 0
previous_key = b''

while offset < len(entries_data):
    shared, offset = read_varint(entries_data, offset)
    non_shared, offset = read_varint(entries_data, offset)
    value_length, offset = read_varint(entries_data, offset)

    key_delta = entries_data[offset:offset + non_shared]

    value_start = offset + non_shared
    value_end = value_start + value_length
    value_bytes = entries_data[value_start:value_end]

    full_key = previous_key[:shared] + key_delta
    previous_key = full_key

    value_offset = 0

    block_offset, value_offset = read_varint(
        value_bytes,
        value_offset,
    )
    block_size, value_offset = read_varint(
        value_bytes,
        value_offset,
    )

    print(
        f"index key: {full_key}\n"
        f"block offset: {block_offset}\n"
        f"block size: {block_size}\n"
    )

    offset = value_end
