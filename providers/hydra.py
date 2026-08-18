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

print(f"meta_offset: {meta_offset}")
print(f"meta_size: {meta_size}")

index_offset, offset = read_varint(footer, offset)
index_size, offset = read_varint(footer, offset)

print(f"index_offset: {index_offset}")
print(f"index_size: {index_size}")

with open(SST_PATH, "rb") as file:
    file.seek(meta_offset)
    meta_block = file.read(meta_size)
    meta_trailer = file.read(5)
    
print(f"meta_block hex: {meta_block.hex(" ")}")
print(f"meta_trailer hex: {meta_trailer.hex(" ")}")

with open(SST_PATH, "rb") as file:
    file.seek(index_offset)
    index_block = file.read(index_size)
    index_trailer = file.read(5)

print(f"index trailer hex: {index_trailer.hex(' ')}")

if index_trailer[0] == 1:
    index_block = snappy.decompress(index_block)
    

print(f"index_block: {index_block}")

restart_count = struct.unpack("<I", index_block[-4:])[0]

print(f"restart_count: {restart_count}")

restart_array_offset = len(index_block) - (restart_count * 4) - 4

print(f"restart_array_offset: {restart_array_offset}")

entries_data = index_block[:restart_array_offset]

print(f"entries size: {len(entries_data)}")