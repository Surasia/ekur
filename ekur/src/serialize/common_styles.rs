use crate::definitions::runtime_styles::RuntimeCoatingStyles;
use anyhow::Result;
use indexmap::IndexMap;
use serde::Serialize;
use std::{collections::HashMap, fs::File, io::BufWriter, path::PathBuf};

#[derive(Debug, Default, Serialize)]
pub struct CommonStyleListEntry {
    pub reference: String,
    pub name: String,
}

#[derive(Debug, Default, Serialize)]
pub struct CommonStyleList {
    pub default_index: i32,
    pub styles: IndexMap<i32, CommonStyleListEntry>,
}

pub fn process_styles(
    styles: &HashMap<i32, RuntimeCoatingStyles>,
    save_path: &str,
    strings: &HashMap<i32, String>,
) -> Result<()> {
    let mut list = CommonStyleList::default();
    for (id, style) in styles {
        for reference in &style.styles.elements {
            let entry = CommonStyleListEntry {
                reference: reference.style_ref.global_id.to_string(),
                name: strings
                    .get(&reference.name.0)
                    .cloned()
                    .unwrap_or(reference.name.0.to_string()),
            };
            list.styles.insert(reference.name.0, entry);
        }
        list.default_index = style.default_style_index.0;
        let mut path = PathBuf::from(format!("{save_path}/stylelists/"));
        path.push(id.to_string());
        path.set_extension("json");
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer_pretty(writer, &list)?;
    }
    Ok(())
}
