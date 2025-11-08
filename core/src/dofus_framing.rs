use byteorder::{BigEndian, ReadBytesExt};
use std::io::{self, Read};

#[derive(Debug, Clone)]
pub struct HeaderMeta {
    pub length_field_bytes: usize,
    pub raw_header: Vec<u8>,
    pub parsed_length: Option<usize>,
    pub notes: String,
}

#[derive(Debug, Clone)]
pub struct PacketFrame {
    pub index: usize,
    pub payload: Vec<u8>,
    pub header_meta: Option<HeaderMeta>,
}

const MAX_FRAME_SIZE: usize = 10 * 1024 * 1024; // 10 MB

/// Attempts to detect and parse a header from the buffer.
/// Returns (HeaderMeta, total_frame_length) if detected, None otherwise.
pub fn detect_and_parse_header(buf: &[u8]) -> Option<(HeaderMeta, usize)> {
    // TODO: Attempt to parse retroproto spec from third_party/retroproto to determine exact framing.
    // For now, implement heuristics as per requirements.

    // Heuristic 1: Try u16 BE length prefix
    if buf.len() >= 2 {
        let mut reader = &buf[..2];
        if let Ok(length_u16) = reader.read_u16::<BigEndian>() {
            let length = length_u16 as usize;
            if length > 0 && length <= MAX_FRAME_SIZE {
                let header_bytes = 2;
                let required = header_bytes + length;
                let actual_total = if required > buf.len() { buf.len() } else { required };
                let notes = if required > buf.len() {
                    "partial u16 BE length prefix heuristic".to_string()
                } else {
                    "u16 BE length prefix heuristic".to_string()
                };
                return Some((
                    HeaderMeta {
                        length_field_bytes: header_bytes,
                        raw_header: buf[..header_bytes].to_vec(),
                        parsed_length: Some(length),
                        notes,
                    },
                    actual_total,
                ));
            }
        }
    }

    // Heuristic 2: Try u32 BE length prefix
    if buf.len() >= 4 {
        let mut reader = &buf[..4];
        if let Ok(length_u32) = reader.read_u32::<BigEndian>() {
            let length = length_u32 as usize;
            if length > 0 && length <= MAX_FRAME_SIZE {
                let header_bytes = 4;
                let required = header_bytes + length;
                let actual_total = if required > buf.len() { buf.len() } else { required };
                let notes = if required > buf.len() {
                    "partial u32 BE length prefix heuristic".to_string()
                } else {
                    "u32 BE length prefix heuristic".to_string()
                };
                return Some((
                    HeaderMeta {
                        length_field_bytes: header_bytes,
                        raw_header: buf[..header_bytes].to_vec(),
                        parsed_length: Some(length),
                        notes,
                    },
                    actual_total,
                ));
            }
        }
    }

    // Heuristic 3: Dofus-style variable-length header (simplified)
    if !buf.is_empty() {
        let header_byte = buf[0];
        let length_bytes = ((header_byte >> 6) & 0x03) + 1; // 1-4 bytes
        if buf.len() >= length_bytes as usize {
            let length = match length_bytes {
                1 => buf[0] as usize & 0x3F,
                2 => ((buf[0] as usize & 0x3F) << 8) | buf[1] as usize,
                3 => ((buf[0] as usize & 0x3F) << 16) | ((buf[1] as usize) << 8) | buf[2] as usize,
                4 => ((buf[0] as usize & 0x3F) << 24) | ((buf[1] as usize) << 16) | ((buf[2] as usize) << 8) | buf[3] as usize,
                _ => return None,
            };
            if length > 0 && length <= MAX_FRAME_SIZE {
                let header_bytes = length_bytes as usize;
                let required = header_bytes + length;
                let actual_total = if required > buf.len() { buf.len() } else { required };
                let notes = if required > buf.len() {
                    format!("partial Dofus variable-length header heuristic ({} bytes)", length_bytes)
                } else {
                    format!("Dofus variable-length header heuristic ({} bytes)", length_bytes)
                };
                return Some((
                    HeaderMeta {
                        length_field_bytes: header_bytes,
                        raw_header: buf[..header_bytes].to_vec(),
                        parsed_length: Some(length),
                        notes,
                    },
                    actual_total,
                ));
            }
        }
    }

    None
}

/// Reads Dofus frames from a reader.
/// Attempts heuristics in order; falls back to StreamToEnd if none work.
pub fn read_dofus_frames<R: Read>(mut r: R) -> Result<Vec<PacketFrame>, io::Error> {
    let mut buffer = Vec::new();
    r.read_to_end(&mut buffer)?;

    let mut frames = Vec::new();
    let mut index = 0;
    let mut offset = 0;

    while offset < buffer.len() {
        if let Some((meta, total_len)) = detect_and_parse_header(&buffer[offset..]) {
            let payload_start = offset + meta.length_field_bytes;
            let payload_end = offset + total_len;
            let payload = buffer[payload_start..payload_end].to_vec();
            frames.push(PacketFrame {
                index,
                payload,
                header_meta: Some(meta),
            });
            offset = payload_end;
            index += 1;
        } else {
            // Fallback: StreamToEnd - single frame with remaining data
            let payload = buffer[offset..].to_vec();
            frames.push(PacketFrame {
                index,
                payload,
                header_meta: Some(HeaderMeta {
                    length_field_bytes: 0,
                    raw_header: Vec::new(),
                    parsed_length: None,
                    notes: "StreamToEnd fallback - no valid header detected".to_string(),
                }),
            });
            break;
        }
    }

    Ok(frames)
}