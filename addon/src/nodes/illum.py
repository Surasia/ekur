# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import bpy
from bpy.types import (
    NodeGroupInput,
    NodeGroupOutput,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketShader,
    ShaderNodeBsdfPrincipled,
    ShaderNodeMath,
    ShaderNodeMix,
)

from ..utils import create_node, create_socket


class SelfIllum:
    def __init__(self) -> None:
        self.node_tree = bpy.data.node_groups.get("Self-Illumination Shader")
        if self.node_tree:
            return
        else:
            self.node_tree = bpy.data.node_groups.new(
                type="ShaderNodeTree",  # pyright: ignore[reportArgumentType]
                name="Self-Illumination Shader",
            )
        self.create_sockets()
        self.create_nodes()

    def create_sockets(self) -> None:
        interface = self.node_tree.interface
        _ = create_socket(interface, "BSDF", NodeSocketShader, False)
        _ = create_socket(interface, "Color Texture", NodeSocketColor)
        _ = create_socket(interface, "Alpha Texture", NodeSocketColor)
        _ = create_socket(interface, "Color", NodeSocketColor)
        _ = create_socket(interface, "Opacity", NodeSocketFloat)
        _ = create_socket(interface, "Intensity", NodeSocketFloat)

    def create_nodes(self) -> None:
        nodes = self.node_tree.nodes
        input = create_node(nodes, 0, 0, NodeGroupInput)
        output = create_node(nodes, 0, 0, NodeGroupOutput)
        bsdf = create_node(nodes, 0, 0, ShaderNodeBsdfPrincipled)
        mult = create_node(nodes, 0, 0, ShaderNodeMath)
        mult.operation = "MULTIPLY"

        mult_2 = create_node(nodes, 0, 0, ShaderNodeMix)
        mult_2.data_type = "RGBA"
        mult_2.blend_type = "MULTIPLY"
        _: NodeSocketFloat = mult_2.inputs[0]
        _.default_value = 1.0

        links = self.node_tree.links
        _ = links.new(input.outputs[0], mult_2.inputs[6])
        _ = links.new(input.outputs[2], mult_2.inputs[7])
        _ = links.new(mult_2.outputs[2], bsdf.inputs[0])
        _ = links.new(mult_2.outputs[2], bsdf.inputs[27])
        _ = links.new(input.outputs[1], mult.inputs[0])
        _ = links.new(input.outputs[3], mult.inputs[1])
        _ = links.new(input.outputs[4], bsdf.inputs[28])
        _ = links.new(mult.outputs[0], bsdf.inputs[4])
        _ = links.new(bsdf.outputs[0], output.inputs[0])
