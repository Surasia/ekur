# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from io import BufferedReader
from .vectors import Bounds


class BoundingBox:
    def __init__(self) -> None:
        self.x_bounds: Bounds = Bounds()
        self.y_bounds: Bounds = Bounds()
        self.z_bounds: Bounds = Bounds()
        self.u_bounds: Bounds = Bounds()
        self.v_bounds: Bounds = Bounds()

    def read(self, reader: BufferedReader) -> None:
        self.x_bounds.read(reader)
        self.y_bounds.read(reader)
        self.z_bounds.read(reader)
        self.u_bounds.read(reader)
        self.v_bounds.read(reader)

    def get_model_scale(self) -> list[tuple[float, float, float]]:
        return [
            (self.x_bounds.min, self.x_bounds.max, self.x_bounds.max - self.x_bounds.min),
            (self.y_bounds.min, self.y_bounds.max, self.y_bounds.max - self.y_bounds.min),
            (self.z_bounds.min, self.z_bounds.max, self.z_bounds.max - self.z_bounds.min),
        ]

    def get_uv_scale(self) -> list[tuple[float, float, float]]:
        return [
            (self.u_bounds.min, self.u_bounds.max, self.u_bounds.max - self.u_bounds.min),
            (self.v_bounds.min, self.v_bounds.max, self.v_bounds.max - self.v_bounds.min),
        ]
