import os
import json
import snappy
import struct

from pathlib import Path


HYDRA_PATH = Path(os.getenv("APPDATA")) / "hydralauncher"


def read_varint(
    data: bytes,
    offset: int,
) -> tuple[int, int]:
    value = 0
    shift = 0

    while True:
        byte = data[offset]
        offset += 1

        value |= (byte & 0x7F) << shift

        if not byte & 0x80:
            return value, offset

        shift += 7


def read_block(
    file_path: Path,
    block_offset: int,
    block_size: int,
) -> bytes:
    with open(file_path, "rb") as file:
        file.seek(block_offset)
        block = file.read(block_size)
        trailer = file.read(5)

        if trailer[0] == 1:
            block = snappy.decompress(block)

    return block


def read_footer(file_path: Path) -> tuple[int, int]:
    offset = 0

    with open(file_path, "rb") as file:
        file.seek(-48, 2)
        footer = file.read(48)

    _, offset = read_varint(footer, offset)
    _, offset = read_varint(footer, offset)

    index_offset, offset = read_varint(footer, offset)
    index_size, offset = read_varint(footer, offset)

    return index_offset, index_size


def parse_block_entries(
    block: bytes,
) -> list[tuple[bytes, bytes]]:
    restart_count = struct.unpack("<I", block[-4:])[0]
    restart_array_offset = (
        len(block)
        - (restart_count * 4)
        - 4
    )

    entries_data = block[:restart_array_offset]
    offset = 0
    entries: list[tuple[bytes, bytes]] = []

    previous_key = b""

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

        offset = value_end

        entries.append((full_key, value_bytes))

    return entries


def read_data_blocks(file_path: Path) -> list[bytes]:
    index_offset, index_size = read_footer(file_path)

    index_block = read_block(
        file_path,
        index_offset,
        index_size,
    )
    index_entries = parse_block_entries(index_block)

    data_blocks: list[bytes] = []

    for _, value_bytes in index_entries:
        value_offset = 0

        block_offset, value_offset = read_varint(
            value_bytes,
            value_offset,
        )
        block_size, _ = read_varint(
            value_bytes,
            value_offset,
        )

        block = read_block(
            file_path,
            block_offset,
            block_size,
        )
        data_blocks.append(block)

    return data_blocks


def parse_internal_key(
    full_key: bytes,
) -> tuple[bytes, int, int]:
    user_key = full_key[:-8]
    internal_suffix = full_key[-8:]

    packed = int.from_bytes(
        internal_suffix,
        byteorder="little",
    )

    sequence_number = packed >> 8
    value_type = packed & 0xFF

    return user_key, sequence_number, value_type


def find_latest_records(
    data_blocks: list[bytes],
) -> dict[bytes, tuple[int, int, bytes]]:
    latest_records: dict[bytes, tuple[int, int, bytes]] = {}

    for block in data_blocks:
        entries = parse_block_entries(block)

        for full_key, value_bytes in entries:
            user_key, sequence_number, value_type = parse_internal_key(
                full_key
            )

            if (
                user_key not in latest_records
                or sequence_number > latest_records[user_key][0]
            ):
                latest_records[user_key] = (
                    sequence_number,
                    value_type,
                    value_bytes,
                )

    return latest_records


def find_database_files(
    hydra_path: Path,
) -> list[Path]:
    database_path = hydra_path / "hydra-db"

    database_files_ldb = list(database_path.glob("*.ldb"))
    database_files_sst = list(database_path.glob("*.sst"))

    database_files = database_files_ldb + database_files_sst

    return database_files


def get_hydra_games(
    hydra_path: Path = HYDRA_PATH,
) -> list[dict]:
    database_files = find_database_files(hydra_path)
    all_records: dict[bytes, tuple[int, int, bytes]] = {}

    for database_file in database_files:
        data_blocks = read_data_blocks(database_file)
        latest_records = find_latest_records(data_blocks)

        for user_key, record in latest_records.items():
            sequence_number, _, _ = record

            if (
                user_key not in all_records
                or sequence_number > all_records[user_key][0]
            ):
                all_records[user_key] = record

    games: list[dict] = []

    for user_key, record in all_records.items():
        if user_key.startswith(b"!games!"):
            _, value_type, value_bytes = record

            if value_type == 0:
                continue

            game = json.loads(value_bytes)

            if game.get("executablePath"):
                games.append(game)

    return games