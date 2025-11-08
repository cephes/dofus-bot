use crate::dofus_mapping::detect_prefix_from_text;
use crate::parser::splitter::split_dofus_messages;
use crate::parser::reassembly::{build_prefix_regex, split_stream_by_prefixes};
use crate::dofus_mapping::all_known_prefixes;

#[derive(Debug, Clone)]
pub enum PacketKind {
    Client(String),
    Server(String),
    Unknown(String),
}

#[derive(Debug, Clone)]
pub struct Packet {
    pub kind: PacketKind,
    pub payload: Vec<u8>,
    pub header_meta: Option<crate::dofus_framing::HeaderMeta>,
}

pub fn classify_packet(payload: &[u8]) -> Vec<Packet> {
    // NOTE: previously we tried to reassemble here, but this function is per-frame.
    // Keep it frame-based for callers that want that behavior.
    let messages = split_dofus_messages(payload);
    let mut packets = Vec::new();
    for message in messages {
        let payload_str = String::from_utf8_lossy(&message);
        let meta = crate::dofus_mapping::detect_prefix_from_text(&payload_str);
        let kind = if let Some(meta) = &meta {
            match meta.category.as_str() {
                "client" => PacketKind::Client(meta.prefix.clone()),
                "server" => PacketKind::Server(meta.prefix.clone()),
                _ => PacketKind::Unknown(meta.prefix.clone()),
            }
        } else {
            PacketKind::Unknown("unknown".to_string())
        };
        let mut header_meta = None;
        if let Some(meta) = meta {
            header_meta = Some(crate::dofus_framing::HeaderMeta {
                length_field_bytes: 0,
                raw_header: vec![],
                parsed_length: None,
                notes: format!(
                    "Detected via mapping: category={}, source={:?}:{:?}, notes={:?}",
                    meta.category, meta.source_file, meta.source_line, meta.notes
                ),
            });
        }
        packets.push(Packet { kind, payload: message.to_vec(), header_meta });
    }
    packets
}

/// Stream-aware classification: split a full TCP flow using whitelisted prefixes.
pub fn classify_stream(stream: &[u8]) -> Vec<Packet> {
    let prefixes = all_known_prefixes();
    let rx = build_prefix_regex(&prefixes);
    let segments = split_stream_by_prefixes(stream, &rx);
    let mut packets = Vec::new();
    for message in segments {
        let payload_str = String::from_utf8_lossy(&message);
        let meta = crate::dofus_mapping::detect_prefix_from_text(&payload_str);
        let kind = if let Some(meta) = &meta {
            match meta.category.as_str() {
                "client" => PacketKind::Client(meta.prefix.clone()),
                "server" => PacketKind::Server(meta.prefix.clone()),
                _ => PacketKind::Unknown(meta.prefix.clone()),
            }
        } else {
            PacketKind::Unknown("unknown".to_string())
        };
        let header_meta = meta.map(|m| crate::dofus_framing::HeaderMeta {
            length_field_bytes: 0,
            raw_header: vec![],
            parsed_length: None,
            notes: format!(
                "Detected via mapping: category={:?}, source={:?}:{:?}, notes={:?}",
                m.category, m.source_file, m.source_line, m.notes
            ),
        });
        packets.push(Packet { kind, payload: message.to_vec(), header_meta });
    }
    packets
}

pub fn classify_packet_with_reassembly(payload: &[u8]) -> Vec<Packet> {
    let messages = crate::parser::reassembly::split_stream_by_prefixes(payload, &crate::parser::reassembly::build_prefix_regex(&crate::dofus_mapping::all_known_prefixes()));

    let mut packets = Vec::new();

    for message in messages {
        let payload_str = String::from_utf8_lossy(&message);

        let meta = detect_prefix_from_text(&payload_str);

        let kind = if let Some(meta) = &meta {
            match meta.category.as_str() {
                "client" => PacketKind::Client(meta.prefix.clone()),
                "server" => PacketKind::Server(meta.prefix.clone()),
                _ => PacketKind::Unknown(meta.prefix.clone()),
            }
        } else {
            PacketKind::Unknown("unknown".to_string())
        };

        let mut header_meta = None;
        if let Some(meta) = meta {
            header_meta = Some(crate::dofus_framing::HeaderMeta {
                length_field_bytes: 0,
                raw_header: vec![],
                parsed_length: None,
                notes: format!(
                    "Detected via mapping: category={}, source={:?}:{:?}, notes={:?}",
                    meta.category,
                    meta.source_file,
                    meta.source_line,
                    meta.notes
                ),
            });
        }

        packets.push(Packet {
            kind,
            payload: message.to_vec(),
            header_meta,
        });
    }

    packets
}