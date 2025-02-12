# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright © 2025 Surasia
from functools import reduce
import operator
import bpy
from bpy.types import EditBone, Object
from mathutils import Matrix

from ..bone import Bone
from ..metadata import Model


def create_transform(transform: Matrix, bone_mode: bool = False) -> Matrix:
    if not bone_mode:
        return Matrix.Scale(1, 4) @ transform.transposed()

    m = transform.transposed()
    translation, rotation, _ = m.decompose()
    return Matrix.Translation(translation * 1) @ rotation.to_matrix().to_4x4()


def get_bone_lineage(model: Model, bone: Bone) -> list[Bone]:
    lineage = [bone]
    current_bone = bone
    while current_bone.parent_index >= 0:
        current_bone = model.bones[current_bone.parent_index]
        lineage.append(current_bone)
    lineage.reverse()
    return lineage


def get_bone_transforms(model: Model) -> list[Matrix]:
    result = []
    for bone in model.bones:
        lineage = get_bone_lineage(model, bone)
        transforms = [create_transform(x.local_transform.to_matrix(), True) for x in lineage]
        result.append(reduce(operator.matmul, transforms))
    return result


def import_bones(model: Model) -> Object:
    armature_data = bpy.data.armatures.new(f"{model.header.tag_id}_Armature")
    armature_obj = bpy.data.objects.new(f"{model.header.tag_id}_Armature", armature_data)

    bpy.context.scene.collection.objects.link(armature_obj)

    bpy.ops.object.select_all(action="DESELECT")
    armature_obj.select_set(True)
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode="EDIT")

    bone_transforms = get_bone_transforms(model)

    editbones: list[EditBone] = []
    for bone in model.bones:
        editbone = armature_data.edit_bones.new(str(bone.name))
        editbones.append(editbone)

    for i, bone in enumerate(model.bones):
        editbone = editbones[i]
        editbone.length = 0.03
        editbone.matrix = bone_transforms[i]
        if bone.parent_index >= 0:
            editbone.parent = editbones[bone.parent_index]

    bpy.ops.object.mode_set(mode="OBJECT")
    return armature_obj
