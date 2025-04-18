# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from functools import reduce
import logging
import operator
from typing import cast
import bpy
from bpy.types import EditBone, Object
from mathutils import Matrix

from ...utils import get_import_properties

from ..bone import Bone
from ..metadata import Model

__all__ = ["import_bones", "get_bone_transforms"]


def create_transform(rot_matrix: Matrix, trans_matrix: Matrix) -> Matrix:
    """
    Create a transformation matrix from the given rotation and translation matrices.

    Args:
    - rot_matrix: The rotation matrix.
    - trans_matrix: The translation matrix.

    Returns:
    - The transformation matrix.
    """
    transform = rot_matrix @ trans_matrix

    m = transform.transposed()
    translation, rotation, _ = m.decompose()
    return Matrix.Translation(translation * 1) @ rotation.to_matrix().to_4x4()


def get_bone_lineage(model: Model, bone: Bone) -> list[Bone]:
    """
    Get the lineage (list of bones up to it) of the given bone.

    - model: The model containing the rig to get the lineage from.
    - bone: The bone to get the lineage of.

    Returns:
    - The lineage of the bone.
    """
    lineage = [bone]
    current_bone = bone
    while current_bone.parent_index >= 0:
        if current_bone.parent_index <= len(model.bones):
            current_bone = model.bones[current_bone.parent_index]
            lineage.append(current_bone)
    lineage.reverse()
    return lineage


def get_bone_transforms(model: Model) -> list[Matrix]:
    """
    Get the global transformation matrices of all bones in the model created through getting the bone lineage.

    Args:
    - model: The model containing the rig to get the bone transforms from.

    Returns:
    - The transformation matrices of all bones in the model.
    """
    result: list[Matrix] = []
    for bone in model.bones:
        lineage = get_bone_lineage(model, bone)
        transforms = [
            create_transform(x.rotation_matrix.matrix, x.transformation_matrix.matrix)
            for x in lineage
        ]
        res = cast(Matrix, reduce(operator.matmul, transforms))
        result.append(res)
    return result


def import_bones(model: Model) -> Object:
    """
    Import the bones from the given model.

    Args:
    - model: The model to import the bones from.

    Returns:
    - The armature object containing the bones.
    """
    props = get_import_properties()
    armature_data = bpy.data.armatures.new(f"{model.header.tag_id}_Armature")
    armature_obj = bpy.data.objects.new(f"{model.header.tag_id}_Armature", armature_data)

    if bpy.context.scene is not None:
        bpy.context.scene.collection.objects.link(armature_obj)  # pyright: ignore[reportUnknownMemberType]
    else:
        logging.warning("No scene found to link the armature to!")

    bpy.ops.object.select_all(action="DESELECT")  # pyright: ignore[reportUnknownMemberType]
    armature_obj.select_set(True)  # pyright: ignore[reportUnknownMemberType]
    if bpy.context.view_layer is not None:
        bpy.context.view_layer.objects.active = armature_obj
    else:
        logging.warning("No view layer found to set the armature object to!")
    bpy.ops.object.mode_set(mode="EDIT")  # pyright: ignore[reportUnknownMemberType]

    bone_transforms = get_bone_transforms(model)

    editbones: list[EditBone] = []
    for bone in model.bones:
        editbone = armature_data.edit_bones.new(str(bone.name))
        editbones.append(editbone)

    for i, bone in enumerate(model.bones):
        editbone = editbones[i]  # directly accessing the list is fine here
        editbone.length = 0.03 * props.scale_factor
        editbone.matrix = bone_transforms[i]
        if bone.parent_index >= 0:
            editbone.parent = editbones[bone.parent_index]

    bpy.ops.object.mode_set(mode="OBJECT")  # pyright: ignore[reportUnknownMemberType]
    return armature_obj
