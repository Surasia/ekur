# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader
import logging


class ModelHeader:
    def __init__(self) -> None:
        self.magic: str = ""
        self.tag_id: int = -1
        self.region_count: int = 0
        self.node_count: int = 0
        self.marker_count: int = 0
        self.material_count: int = 0
        self.section_count: int = 0
        self.bounding_box_count: int = 0

    def read(self, reader: BufferedReader) -> None:
        self.magic = reader.read(4).decode("utf-8")
        if self.magic != "SURA":
            logging.critical(f"Invalid magic: {self.magic}")
            return
        self.tag_id = int.from_bytes(reader.read(4), "little", signed=True)
        self.region_count = int.from_bytes(reader.read(4), "little")
        self.node_count = int.from_bytes(reader.read(4), "little")
        self.marker_count = int.from_bytes(reader.read(4), "little")
        self.material_count = int.from_bytes(reader.read(4), "little")
        self.section_count = int.from_bytes(reader.read(4), "little")
        self.bounding_box_count = int.from_bytes(reader.read(4), "little")
