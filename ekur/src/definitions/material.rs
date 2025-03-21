/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright © 2025 Surasia */
use infinite_rs::TagStructure;
use infinite_rs::tag::types::common_types::{
    AnyTag, FieldBlock, FieldCharEnum, FieldLongEnum, FieldReal, FieldRealARGBColor,
    FieldRealQuaternion, FieldRealVector3D, FieldReference, FieldStringId, FieldWordInteger,
};
use num_enum::TryFromPrimitive;

#[derive(TryFromPrimitive, Debug, Default)]
#[repr(u8)]
pub enum MaterialStyleShaderSupportedLayers {
    #[default]
    Supports1Layer,
    Supports4Layers,
    Supports7Layers,
    LayerShaderDisabled,
}

#[derive(TryFromPrimitive, Debug, Default, PartialEq, Eq)]
#[repr(u8)]
pub enum MaterialStyleShaderSupportsDamageEnum {
    #[default]
    No,
    Yes,
}

#[derive(TryFromPrimitive, Debug, Default)]
#[repr(u32)]
pub enum MaterialParameterType {
    #[default]
    Bitmap,
    Real,
    Int,
    Bool,
    Color,
    ScalarGPUProperty,
    ColorGPUProperty,
    String,
    Preset,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x5c))]
pub struct MaterialStyleInfo {
    #[data(offset(0x00))]
    pub material_style: FieldReference,
    #[data(offset(0x1C))]
    pub material_style_tag: FieldReference,
    #[data(offset(0x38))]
    pub region_name: FieldStringId,
    #[data(offset(0x3C))]
    pub base_intention: FieldStringId,
    #[data(offset(0x40))]
    pub mask0_red_channel_intention: FieldStringId,
    #[data(offset(0x44))]
    pub mask0_green_channel_intention: FieldStringId,
    #[data(offset(0x48))]
    pub mask0_blue_channel_intention: FieldStringId,
    #[data(offset(0x4C))]
    pub mask1_red_channel_intention: FieldStringId,
    #[data(offset(0x50))]
    pub mask1_green_channel_intention: FieldStringId,
    #[data(offset(0x54))]
    pub mask1_blue_channel_intention: FieldStringId,
    #[data(offset(0x58))]
    pub supported_layers: FieldCharEnum<MaterialStyleShaderSupportedLayers>,
    #[data(offset(0x59))]
    pub requires_damage: FieldCharEnum<MaterialStyleShaderSupportsDamageEnum>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x5c))]
pub struct MaterialStyleInfoCampaign {
    #[data(offset(0x00))]
    pub material_style: FieldReference,
    #[data(offset(0x1C))]
    pub material_style_tag: FieldReference,
    #[data(offset(0x38))]
    pub region_name: FieldStringId,
    #[data(offset(0x3C))]
    pub base_intention: FieldStringId,
    #[data(offset(0x40))]
    pub mask0_red_channel_intention: FieldStringId,
    #[data(offset(0x44))]
    pub mask0_green_channel_intention: FieldStringId,
    #[data(offset(0x48))]
    pub mask0_blue_channel_intention: FieldStringId,
    #[data(offset(0x4C))]
    pub mask1_red_channel_intention: FieldStringId,
    #[data(offset(0x50))]
    pub mask1_green_channel_intention: FieldStringId,
    #[data(offset(0x54))]
    pub mask1_blue_channel_intention: FieldStringId,
    #[data(offset(0x58))]
    pub supported_layers: FieldCharEnum<MaterialStyleShaderSupportedLayers>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x9c))]
pub struct MaterialParameter {
    #[data(offset(0x00))]
    pub parameter_name: FieldStringId,
    #[data(offset(0x4))]
    pub parameter_type: FieldLongEnum<MaterialParameterType>,
    #[data(offset(0x8))]
    pub bitmap: FieldReference,
    #[data(offset(0x24))]
    pub color: FieldRealARGBColor,
    #[data(offset(0x34))]
    pub real: FieldReal,
    #[data(offset(0x38))]
    pub vector: FieldRealVector3D,
    #[data(offset(0x94))]
    pub register_offset: FieldWordInteger,
    #[data(offset(0x96))]
    pub register_size: FieldWordInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x38))]
pub struct MaterialPostProcessTexture {
    #[data(offset(0x00))]
    pub bitmap_reference: FieldReference,
    #[data(offset(0x2A))]
    pub parameter_index: FieldWordInteger,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x10))]
pub struct MaterialConstant {
    #[data(offset(0x00))]
    pub register: FieldRealQuaternion,
}

#[derive(Debug, Default, TryFromPrimitive)]
#[repr(u8)]
pub enum AlphaMode {
    #[default]
    Opaque,
    Additive,
    Multiply,
    AlphaBlend,
    DoubleMultiply,
    PreMultipliedAlpha,
    Maximum,
    MultiplyAdd,
    AddSrcTimesDstAlpha,
    AddSrcTimesSrcAlpha,
    InvAlphaBlend,
    OverdrawApply,
    Decal,
    Minimum,
    RevSubtract,
    AlphaBlendMax,
    OpaqueAlphaBlend,
    AlphaBlendAdditiveTransparent,
    Unused0,
    DecalAlphaBlend,
    DecalAddSrcTimesSrcAlpha,
    DecalMultiplyAdd,
    WpfNoColorBlendMode,
    DecalOpaque,
    AccumulatePreMultipliedAlpha,
    WpfBlendMode,
    AccumulateMultiplyAdd,
    AccumulateAlphaBlend,
    AccumulateInverseAlphaBlend,
    AccumulateAdditive,
    AccumulateAdditiveTransparent,
    AccumulateAddSrcTimesSrcAlpha,
    AccumulateMultiply,
    AlphaBlendForDisplayPlanes,
    TexturePainterSrcAddDestMult,
    TexturePainterDestMultSubSrc,
    LogicalOr,
    LogicalAnd,
    DecalMultiply,
    DecalDoubleMultiply,
    FourChannelAdditive,
    WpfAdditiveBlendMode,
    CloudApply,
    SubsurfaceScatteringConvolution,
    ReflectionOcclusionMask,
    TaaMaskAdditive,
    TaaMaskRevSubtract,
    TaaMaskMultiply,
    TaaMaskDoubleMultiply,
    TaaMaskPreMultipliedAlpha,
    TaaMaskMultiplyAdd,
    TaaMaskAlphaBlend,
    TaaMaskAddSrcTimesDstAlpha,
    TaaMaskAddSrcTimesSrcAlpha,
    TaaMaskAdditiveTransparent,
    TaaMaskAlphaBlendForDisplayPlane,
    TaaVelocityAdditive,
    TaaVelocityRevSubtract,
    TaaVelocityMultiply,
    TaaVelocityDoubleMultiply,
    TaaVelocityPreMultipliedAlpha,
    TaaVelocityMultiplyAdd,
    TaaVelocityAlphaBlend,
    TaaVelocityAddSrcTimesDstAlpha,
    TaaVelocityAddSrcTimesSrcAlpha,
    TaaVelocityAdditiveTransparent,
    TaaVelocityAlphaBlendForDisplayPlane,
    DeferredDecalsResolve,
    DecalAoOpaque,
    DecalAoAlphaBlend,
    DecalSssBlend,
    HudDamageAlphaBlend,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0xA0))]
pub struct MaterialPostProcessing {
    #[data(offset(0x00))]
    pub textures: FieldBlock<MaterialPostProcessTexture>,
    #[data(offset(0x58))]
    pub material_constants: FieldBlock<MaterialConstant>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x88))]
pub struct MaterialTag {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub material_shader: FieldReference,
    #[data(offset(0x2C))]
    pub material_parameters: FieldBlock<MaterialParameter>,
    #[data(offset(0x40))]
    pub post_process_definition: FieldBlock<MaterialPostProcessing>,
    #[data(offset(0x68))]
    pub alpha_blend_mode: FieldCharEnum<AlphaMode>,
    #[data(offset(0x74))]
    pub style_info: FieldBlock<MaterialStyleInfo>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x88))]
pub struct MaterialTagCampaign {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub material_shader: FieldReference,
    #[data(offset(0x2C))]
    pub material_parameters: FieldBlock<MaterialParameter>,
    #[data(offset(0x40))]
    pub post_process_definition: FieldBlock<MaterialPostProcessing>,
    #[data(offset(0x68))]
    pub alpha_blend_mode: FieldCharEnum<AlphaMode>,
    #[data(offset(0x74))]
    pub style_info: FieldBlock<MaterialStyleInfoCampaign>,
}
