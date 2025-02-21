use infinite_rs::{
    tag::types::common_types::{
        AnyTag, FieldBlock, FieldQwordInteger, FieldReference, FieldStringId,
    },
    TagStructure,
};

#[derive(Default, Debug, TagStructure)]
#[data(size(0x18))]
pub struct ForgeObjectCategoryEntry {
    #[data(offset(0x08))]
    pub title: FieldStringId,
    #[data(offset(0x0C))]
    pub description: FieldStringId,
    #[data(offset(0x10))]
    pub category_id: FieldStringId,
    #[data(offset(0x14))]
    pub parent_category_id: FieldStringId,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x60))]
pub struct ForgeObjectManifestEntry {
    #[data(offset(0x00))]
    pub element_id: FieldQwordInteger,
    #[data(offset(0x08))]
    pub forge_object: FieldReference,
    #[data(offset(0x24))]
    pub name: FieldStringId,
    #[data(offset(0x28))]
    pub description: FieldStringId,
    #[data(offset(0x48))]
    pub object_metadata: FieldBlock<ForgeObjectCategoryEntry>,
}

#[derive(Default, Debug, TagStructure)]
#[data(size(0x48))]
pub struct ForgeObjectManifest {
    #[data(offset(0x00))]
    pub any_tag: AnyTag,
    #[data(offset(0x10))]
    pub entries: FieldBlock<ForgeObjectManifestEntry>,
}
