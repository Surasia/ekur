# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
import json
import logging
from pathlib import Path
from typing import cast

import bpy
from bpy.types import (
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeOutputMaterial,
    ShaderNodeTexImage,
    ShaderNodeTree,
)

from ..json_definitions import (
    CoatingGlobalEntries,
    CommonCoating,
    CommonLayer,
    CommonMaterial,
    CommonRegion,
    CommonStyleList,
    get_intentions,
)
from ..nodes.hims import HIMS
from ..nodes.layer import Layer
from ..utils import assign_value, create_node, read_json_file, read_texture

MP_VISOR: int = 1420626520
ANY_REGION: int = 192819851

__all__ = ["LayeredShader"]


class LayeredShader:
    def __init__(
        self,
        material_tree: ShaderNodeTree,
        material: CommonMaterial,
        styles: CommonStyleList,
        data_folder: str,
    ) -> None:
        self.node_tree: ShaderNodeTree = material_tree
        self.styles: CommonStyleList = styles
        self.material: CommonMaterial = material
        self.index: int = 0
        self.data_folder: str = data_folder
        self.shader: ShaderNodeGroup
        self.create_nodes()

    def create_nodes(self):
        self.shader = create_node(self.node_tree.nodes, 700, 600, ShaderNodeGroup)
        self.shader.node_tree = cast(ShaderNodeTree, HIMS().node_tree)
        self.shader.width = 400
        material_output = create_node(self.node_tree.nodes, 2000, 150, ShaderNodeOutputMaterial)
        _ = self.node_tree.links.new(self.shader.outputs[0], material_output.inputs[0])

    def create_image(self, shader: NodeTree, name: int, y: int) -> ShaderNodeTexImage:
        texture = cast(ShaderNodeTexImage, shader.nodes.new("ShaderNodeTexImage"))
        texture.hide = True
        texture.location = (0, y)
        texture.image = read_texture(str(name))
        return texture

    def create_textures(self) -> None:
        textures = self.material["textures"]
        if textures.get("Asg"):
            tex = self.create_image(self.node_tree, textures["Asg"], 120)
            tex.interpolation = "Cubic"
            if tex.image and tex.image.get("use_alpha"):  # pyright: ignore[reportUnknownMemberType]
                transparencies = [21, 36, 51, 67, 83, 99, 115]
                for i in transparencies:
                    _ = self.node_tree.links.new(tex.outputs[1], self.shader.inputs[i])

            _ = self.node_tree.links.new(tex.outputs[0], self.shader.inputs[0])
        else:
            assign_value(self.shader, 0, (1.0, 1.0, 1.0, 1.0))
        if textures.get("Mask0"):
            tex = self.create_image(self.node_tree, textures["Mask0"], 80)
            _ = self.node_tree.links.new(tex.outputs[0], self.shader.inputs[1])
        if textures.get("Mask1"):
            tex = self.create_image(self.node_tree, textures["Mask1"], 40)
            _ = self.node_tree.links.new(tex.outputs[0], self.shader.inputs[2])
        if textures.get("Normal") and textures["Normal"] != -1:
            tex = self.create_image(self.node_tree, textures["Normal"], 0)
            _ = self.node_tree.links.new(tex.outputs[0], self.shader.inputs[3])
        else:
            assign_value(self.shader, 3, (0.5, 0.5, 1.0, 1.0))

    def process_styles(self) -> None:
        style = self.styles["default_style"]["reference"]
        import_props = bpy.context.scene.import_properties  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportUnknownVariableType]
        custom_style: str = cast(str, import_props.coat_id)
        items_func = cast(int, import_props.coatings)
        use_default: str = import_props.use_default  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

        if custom_style != "" and not use_default and self.styles["styles"].get(custom_style):
            style = self.styles["styles"][custom_style]["reference"]
        if custom_style == "" and not use_default and self.styles["styles"].get(str(items_func)):
            style = self.styles["styles"][str(items_func)]["reference"]

        style_path = Path(f"{self.data_folder}/styles/{style}.json")
        if not style_path.exists():
            logging.warning(f"Style path does not exist!: {style_path}")
            return
        style_json = read_json_file(style_path, CommonCoating)

        globals_path = Path(f"{self.data_folder}/globals.json")
        if not globals_path.exists():
            logging.warning(f"Style path does not exist!: {globals_path}")
            return
        globals_json = read_json_file(globals_path, CoatingGlobalEntries)
        self.create_style(style_json, globals_json)

    def create_style(self, style: CommonCoating, globals: CoatingGlobalEntries):
        style_info = self.material["style_info"]
        if style_info:
            all = style["regions"].get(str(ANY_REGION))
            reg: CommonRegion | None = None
            if style["regions"].get(str(style_info["region_name"])):
                reg = style["regions"][str(style_info["region_name"])]

            intentions = get_intentions(style_info)
            self.index = 0
            diff = 15

            for i, intention in enumerate(intentions[: style_info["supported_layers"]]):
                intention = str(intention)
                if i == 2:
                    diff = 16
                self.find_intention(intention, reg, all, globals, diff, i)

            assign_value(self.shader, 7, style["grime_amount"])
            if style["grime_swatch"]["disabled"]:
                assign_value(self.shader, 7, 0.0)
            assign_value(self.shader, 16, style["scratch_amount"])
            assign_value(self.shader, 12, 1.0)
            assign_value(self.shader, 135, style_info["texel_density"][0])
            assign_value(self.shader, 136, style_info["texel_density"][1])

            self.index = 109
            top = style["grime_swatch"]["top_color"]
            swatch = cast(ShaderNodeTree, Layer(style["grime_swatch"], f"g_{top}").node_tree)
            emissive_amount = style["grime_swatch"]["emissive_amount"]
            self.create_swatch(swatch, top, 7, emissive_amount, is_grime=True)
            toggle_damage = cast(bool, bpy.context.scene.import_properties.toggle_damage)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
            if toggle_damage and style_info["supported_layers"] == 7:
                assign_value(self.shader, 106, 0.0)
            if toggle_damage and style_info["supported_layers"] == 4:
                assign_value(self.shader, 58, 0.0)
            self.index = 0

    def create_swatch(
        self,
        shader_group: ShaderNodeTree,
        color: tuple[float, float, float],
        location: float,
        emissive: float,
        is_grime: bool = False,
        disabled: bool = False,
    ):
        redo2 = False
        if location == 1 and not self.shader.inputs[23].is_linked:
            location = 0
            self.index -= 15
            redo2 = True

        swatch = cast(ShaderNodeGroup, self.node_tree.nodes.new("ShaderNodeGroup"))
        swatch.hide = True
        swatch.use_custom_color = True
        swatch.color = color
        swatch.node_tree = shader_group
        swatch.location = (500, -232 + location * -350)
        if self.material["style_info"]:
            assign_value(swatch, 0, self.material["style_info"]["texel_density"][0])
            assign_value(swatch, 1, self.material["style_info"]["texel_density"][1])
            assign_value(swatch, 6, self.material["style_info"]["material_offset"][0])
            assign_value(swatch, 7, self.material["style_info"]["material_offset"][1])

        _ = self.node_tree.links.new(swatch.outputs[0], self.shader.inputs[13 + self.index])
        _ = self.node_tree.links.new(swatch.outputs[1], self.shader.inputs[14 + self.index])
        _ = self.node_tree.links.new(swatch.outputs[2], self.shader.inputs[15 + self.index])
        if is_grime:
            _ = self.node_tree.links.new(swatch.outputs[5], self.shader.inputs[16 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[6], self.shader.inputs[20 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[7], self.shader.inputs[21 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[8], self.shader.inputs[22 + self.index])
        else:
            if self.index != 0 and not disabled:
                assign_value(self.shader, 12 + self.index, 1.0)
            assign_value(self.shader, 22 + self.index, emissive)
            _ = self.node_tree.links.new(swatch.outputs[3], self.shader.inputs[17 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[4], self.shader.inputs[18 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[5], self.shader.inputs[19 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[6], self.shader.inputs[23 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[7], self.shader.inputs[24 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[8], self.shader.inputs[25 + self.index])
            _ = self.node_tree.links.new(swatch.outputs[9], self.shader.inputs[26 + self.index])
        if redo2:
            self.index += 15
            self.create_swatch(shader_group, color, 2, emissive)

    def get_intention(
        self,
        intention: str,
        reg: CommonRegion | None,
        all: CommonRegion | None,
        globals: CoatingGlobalEntries,
    ) -> CommonLayer | None:
        if reg and reg["layers"].get(intention):
            return reg["layers"][intention]
        elif all and all["layers"].get(str(intention)):
            return all["layers"][intention]
        elif globals["entries"].get(intention):
            if globals["entries"][intention]["fallback"] != 0:
                fallback = str(globals["entries"][intention]["fallback"])
                return self.get_intention(fallback, reg, all, globals)
            return globals["entries"][intention]["layer"]
        else:
            logging.warning(f"Intention not found at all, skipping!: {intention}")

    def find_intention(
        self,
        intention: str,
        mat_reg: CommonRegion | None,
        any_reg: CommonRegion | None,
        globals: CoatingGlobalEntries,
        difference: int,
        i: int,
    ):
        """Finds the intention provided in the "common", "local" and "global" regions.

        Args:
            intention: Name of intention to search for.
            mat_reg: Region of the material containing intentions that should be prioritized.
            any_reg: "common" (index 0) region on a coating.
            globals: Intentions found in the "CoatingGlobals" tag
            difference: Difference between the indices of the inputs between the zones on the shader.
            i: Index of the intention.
        """
        layer = self.get_intention(intention, mat_reg, any_reg, globals)
        toggle_visors = cast(bool, bpy.context.scene.import_properties.toggle_visors)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
        visor = cast(str, bpy.context.scene.import_properties.visors)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
        if (
            i == 0
            and self.material["style_info"]
            and self.material["style_info"]["region_name"] == MP_VISOR
            and toggle_visors
        ):
            visors_path = Path(f"{self.data_folder}/all_visors.json")
            if not visors_path.exists():
                return
            visors = read_json_file(visors_path, dict[str, CommonLayer])
            layer = visors[visor]
        if layer:
            swatch = cast(
                ShaderNodeTree, Layer(layer, f"{intention}_{hash(json.dumps(layer))}").node_tree
            )
            emissive = layer["emissive_amount"]
            self.create_swatch(swatch, layer["mid_color"], i, emissive, layer["disabled"])
        self.index += difference
