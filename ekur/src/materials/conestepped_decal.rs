/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use anyhow::Result;

use crate::definitions::material::MaterialTag;

use super::{
    common_utils::{f32_from_const, get_post_texture},
    serde_definitions::{ConesteppedDecal, Material, ShaderType, TextureType},
};

pub(super) fn handle_conestepped_decal(mat: &MaterialTag, material: &mut Material) -> Result<()> {
    let post_process = mat.post_process_definition.elements.first();
    let mut conestepped_decal = ConesteppedDecal::default();
    if let Some(post_process) = post_process {
        conestepped_decal.parallax_depth = f32_from_const(material, 0)?;
        conestepped_decal.parallax_height_offset = f32_from_const(material, 4)?;
        get_post_texture(post_process, material, 20, TextureType::MacroConemap)?;
        get_post_texture(post_process, material, 48, TextureType::Control)?;
        get_post_texture(post_process, material, 80, TextureType::Normal)?;
        conestepped_decal.normal_intensity = f32_from_const(material, 112)?;
        material.conestepped_decal = Some(conestepped_decal);
        material.shader_type = ShaderType::ConesteppedDecal;
    }
    Ok(())
}
