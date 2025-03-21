/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use std::collections::HashMap;

use serde::Serialize;

#[derive(Default, Debug, Serialize)]
pub(crate) enum ShaderType {
    #[default]
    Unknown,
    Layered,
    Diffuse,
    Decal,
    SelfIllum,
    ConesteppedLevel,
    ColorDecal,
    ConesteppedDecal,
    Meter,
    SkinShader,
    EyeShader,
    Hair,
}

#[derive(Default, Debug, Serialize, PartialEq, Eq, Hash)]
pub enum TextureType {
    #[default]
    Normal,
    Asg,
    Mask0,
    Mask1,
    Color,
    Control,
    AlphaMap,
    MacroMaskMap,
    MacroCohmap,
    MacroConemap,
    MacroNormal,
    NoiseTexture,
    SharedControl,
    BurntGradient,
    Emissive,
    Meter,
    AORoughnessTransmission,
    SpecScatterPore,
    PoreNormal,
    DetailNormal,
    Sclera,
    ScleraNormal,
    Iris,
    IrisNormal,
    AO,
    EyeGazeMap,
    Cubemap,
}

#[derive(Default, Debug, Serialize, Clone)]
pub(crate) struct StyleInfo {
    pub(crate) texel_density: (f32, f32),
    pub(crate) material_offset: (f32, f32),
    pub(crate) stylelist: i32,
    pub(crate) region_name: i32,
    pub(crate) base_intention: i32,
    pub(crate) mask0_red_intention: i32,
    pub(crate) mask0_green_intention: i32,
    pub(crate) mask0_blue_intention: i32,
    pub(crate) mask1_red_intention: i32,
    pub(crate) mask1_green_intention: i32,
    pub(crate) mask1_blue_intention: i32,
    pub(crate) supported_layers: u8,
    pub(crate) enable_damage: bool,
}

#[derive(Default, Debug, Serialize)]
pub struct DiffuseInfo {
    pub metallic_white: f32,
    pub metallic_black: f32,
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub si_color_tint: (f32, f32, f32),
    pub si_intensity: f32,
    pub si_amount: f32,
    pub color_tint: (f32, f32, f32),
}

#[derive(Default, Debug, Serialize)]
pub struct DecalSlot {
    pub top_color: (f32, f32, f32),
    pub mid_color: (f32, f32, f32),
    pub bot_color: (f32, f32, f32),
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub metallic: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct SelfIllum {
    pub color: (f32, f32, f32),
    pub intensity: f32,
    pub opacity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct ConemappedLevel {
    pub macro_mask_transform: [f32; 2],
    pub macro_normal_transform: [f32; 2],
    pub macro_normal_intensity: f32,
    pub macro_cohmap_transform: [f32; 2],
    pub macro_height_scale: f32,
    pub macro_conemap_transform: [f32; 2],
    pub macro_cone_depth: f32,
    pub macro_cone_offset: f32,
    pub macro_cone_quality: f32,
    pub macro_noise_transform: [f32; 2],
    pub macro_noise_color: [f32; 3],
    pub macro_noise_roughness: f32,
    pub macro_noise_remap_white: f32,
    pub macro_noise_remap_black: f32,
    pub macro_noise_detail_remap_white: f32,
    pub macro_noise_detail_remap_black: f32,
    pub macro_noise_opacity: f32,
    pub base_normal_intensity: f32,
    pub base_normal_transform: [f32; 2],
    pub base_control_transform: [f32; 2],
    pub base_height_scale: f32,
    pub base_top_color: [f32; 3],
    pub base_mid_color: [f32; 3],
    pub base_bottom_color: [f32; 3],
    pub base_roughness_white: f32,
    pub base_roughness_black: f32,
    pub base_metallic: f32,
    pub base_curvature_height_influence: f32,
    pub base_edge_wear_offset: f32,
    pub base_edge_wear_contrast: f32,
    pub base_edge_wear_opacity: f32,
    pub base_edge_wear_color: [f32; 3],
    pub base_edge_wear_roughness: f32,
    pub shared_control_transform: [f32; 2],
    pub burnt_gradient_transform: [f32; 2],
    pub layer2_height_scale: f32,
    pub char_height_scale: f32,
    pub char_height_offset: f32,
    pub char_opacity: f32,
    pub char_top_color: [f32; 3],
    pub char_mid_color: [f32; 3],
    pub char_bot_color: [f32; 3],
    pub char_roughness_white: f32,
    pub char_roughness_black: f32,
    pub rust_height_scale: f32,
    pub rust_height_offset: f32,
    pub rust_staining_offset: f32,
    pub rust_falloff_color: [f32; 3],
    pub rust_heavy_rust_offset: f32,
    pub rust_heavy_rust_falloff_paint_opacity: f32,
    pub rust_secondary_top_color: [f32; 3],
    pub rust_secondary_mid_color: [f32; 3],
    pub rust_secondary_bottom_color: [f32; 3],
    pub rust_secondary_color_start: f32,
    pub rust_secondary_color_end: f32,
    pub rust_top_color: [f32; 3],
    pub rust_mid_color: [f32; 3],
    pub rust_bottom_color: [f32; 3],
    pub rust_normal_intensity_new: f32,
    pub rust_heavy_rust_edge_start: f32,
    pub rust_heavy_rust_edge_end: f32,
    pub rust_roughness_white: f32,
    pub rust_roughness_black: f32,
    pub rust_metallic: f32,
    pub burnt_height_offset: f32,
    pub burnt_opacity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct ColorDecal {
    pub opacity: f32,
    pub metallic: f32,
    pub roughness: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct ConesteppedDecal {
    pub parallax_depth: f32,
    pub parallax_height_offset: f32,
    pub normal_intensity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct Meter {
    pub meter_off_color: (f32, f32, f32),
    pub meter_on_color: (f32, f32, f32),
    pub meter_value: f32,
    pub meter_intensity: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct SkinShader {
    pub sss_strength: f32,
    pub specular_intensity: f32,
    pub specular_white: f32,
    pub specular_black: f32,
    pub pore_normal_intensity: f32,
    pub micro_normal_intensity: f32,
    pub micro_normal_scale: [f32; 2],
}

#[derive(Default, Debug, Serialize)]
pub struct EyeShader {
    pub sclera_brightness: f32,
    pub sclera_normal_intensity: f32,
    pub sclera_roughness: f32,
    pub sclera_ior: f32,
    pub iris_radius: f32,
    pub iris_brightness: f32,
    pub iris_normal_intensity: f32,
    pub cornea_roughness: f32,
    pub cornea_ior: f32,
    pub pupil_scale: f32,
    pub limbus_width: f32,
    pub limbus_darkening_scale: f32,
    pub limbus_power: f32,
    pub eye_ior: f32,
    pub cornea_height_scale: f32,
    pub overall_scale: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct Hair {
    pub tint_color: (f32, f32, f32),
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub ior: f32,
}

#[derive(Default, Debug, Serialize)]
pub struct LevelLayer {
    pub height_scale: f32,
    pub roughness_white: f32,
    pub roughness_black: f32,
    pub opacity: f32,
    pub ior: f32,
    pub uses_single_metallic: bool,
    pub uses_color_gradient: bool,
    pub uses_packed: bool,
    pub metallic: f32,
    pub metallic_white: f32,
    pub metallic_black: f32,
    pub normal_intensity: f32,
    pub top_color: (f32, f32, f32),
    pub mid_color: (f32, f32, f32),
    pub bot_color: (f32, f32, f32),
    pub color_tint: (f32, f32, f32),
}

#[derive(Default, Debug, Serialize)]
pub struct RegularLevelShader {
    pub macro_normal_intensity: f32,
    pub macro_color_intensity: f32,
    pub macro_roughness_intensity: f32,
    pub macro_occlusion_intensity: f32,
    pub macro_metallic_intensity: f32,
    pub macro_cavity_intensity: f32,
    pub macro_cavity_exponent: f32,
    pub layers: Vec<LevelLayer>,
}

#[derive(Default, Debug, Serialize)]
pub struct Material {
    pub shader: i32,
    pub textures: HashMap<TextureType, i32>,
    pub shader_type: ShaderType,
    pub alpha_blend_mode: String,
    pub style_info: Option<StyleInfo>,
    pub diffuse_info: Option<DiffuseInfo>,
    pub illum_info: Option<SelfIllum>,
    pub decal_slots: Option<DecalSlot>,
    pub conemapped_level: Option<ConemappedLevel>,
    pub color_decal: Option<ColorDecal>,
    pub conestepped_decal: Option<ConesteppedDecal>,
    pub meter: Option<Meter>,
    pub skin: Option<SkinShader>,
    pub eye: Option<EyeShader>,
    pub hair: Option<Hair>,
    pub level: Option<RegularLevelShader>,
    #[serde(skip)]
    pub material_constants: Vec<u8>,
}
