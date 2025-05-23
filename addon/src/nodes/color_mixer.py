# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy

from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeTree,
    ShaderNodeMath,
    ShaderNodeMix,
)

from ..utils import assign_value, create_node, create_socket

__all__ = ["ColorMixer"]


class ColorMixer:
    def __init__(self) -> None:
        self.node_tree: NodeTree | None = bpy.data.node_groups.get("Color Mixer")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="Color Mixer")
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        if self.node_tree is None:
            return
        interface = self.node_tree.interface
        _ = create_socket(interface, "Color", NodeSocketColor, False)
        _ = create_socket(interface, "Gradient Out", NodeSocketFloat)
        _ = create_socket(interface, "Top", NodeSocketColor)
        _ = create_socket(interface, "Mid", NodeSocketColor)
        _ = create_socket(interface, "Bot", NodeSocketColor)

    def create_nodes(self) -> None:
        if self.node_tree is None:
            return
        input = create_node(self.node_tree.nodes, -474, 0, NodeGroupInput)
        output = create_node(self.node_tree.nodes, 530, 4, NodeGroupOutput)

        madd = create_node(self.node_tree.nodes, -239, 316, ShaderNodeMath)
        madd.operation = "MULTIPLY_ADD"
        assign_value(madd, 1, 2.0)
        assign_value(madd, 2, -1.0)
        madd.location = (-239, 316)

        madd2 = create_node(self.node_tree.nodes, -240, 125, ShaderNodeMath)
        madd2.operation = "MULTIPLY_ADD"
        assign_value(madd2, 1, -2.0)
        assign_value(madd2, 2, 1.0)

        mix = create_node(self.node_tree.nodes, 300, 80, ShaderNodeMix)
        mix.clamp_factor = True
        mix.clamp_result = True
        mix.data_type = "RGBA"

        mix1 = create_node(self.node_tree.nodes, 79, 135, ShaderNodeMix)
        mix1.clamp_factor = True
        mix1.clamp_result = True
        mix1.data_type = "RGBA"

        links = self.node_tree.links
        _ = links.new(input.outputs[2], mix1.inputs[6])
        _ = links.new(mix1.outputs[2], mix.inputs[6])
        _ = links.new(input.outputs[3], mix.inputs[7])
        _ = links.new(mix.outputs[2], output.inputs[0])
        _ = links.new(input.outputs[1], mix1.inputs[7])
        _ = links.new(input.outputs[0], madd.inputs[0])
        _ = links.new(input.outputs[0], madd2.inputs[0])
        _ = links.new(madd.outputs[0], mix1.inputs[0])
        _ = links.new(madd2.outputs[0], mix.inputs[0])
