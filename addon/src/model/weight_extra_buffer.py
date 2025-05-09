# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import struct

from io import BufferedReader
from typing import cast

from ..exceptions import IncorrectStrideValue

__all__ = ["WeightExtraBuffer"]


class WeightExtraBuffer:
    def __init__(self) -> None:
        self.stride: int = -1
        self.count: int = 0
        self.values: list[float] = []

    def read(self, reader: BufferedReader) -> None:
        self.stride = int.from_bytes(reader.read(1), "little", signed=True)
        if self.stride != 4:
            raise IncorrectStrideValue("Invalid WeightExtra buffer stride")
        self.count = int.from_bytes(reader.read(4), "little")
        for _ in range(self.count):
            value: float = cast(float, struct.unpack("f", reader.read(4))[0])
            self.values.append(value)
