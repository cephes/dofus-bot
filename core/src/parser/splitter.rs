/// Splits a byte slice containing concatenated Dofus messages into a Vec<Vec<u8>>
/// Splitting rules (conservative):
/// 1. Split on NUL (0x00) boundaries.
/// 2. If NUL is not present, split at positions immediately preceding known prefixes:
///    GM|, GA;, BN|, HC, HC|, GN|, GT|, PV? (include typical tokens used by Dofus Retro)
/// 3. Trim leading/trailing whitespace bytes and ignore empty fragments.
/// Returns Vec of byte vectors (each logical message).
pub fn split_dofus_messages(payload: &[u8]) -> Vec<Vec<u8>> {
    let mut messages = Vec::new();

    // First, split on NUL (0x00)
    let nul_splits: Vec<&[u8]> = payload.split(|&b| b == 0x00).collect();

    for part in nul_splits {
        if part.is_empty() {
            continue;
        }

        // Trim whitespace
        let trimmed = trim_whitespace(part);
        if trimmed.len() < 3 {
            continue; // Ignore very small fragments
        }

        // Check for known prefixes and split further if needed
        let sub_messages = split_on_prefixes(trimmed);
        messages.extend(sub_messages);
    }

    messages
}

fn trim_whitespace(data: &[u8]) -> &[u8] {
    let start = data.iter().position(|&b| !is_whitespace(b)).unwrap_or(data.len());
    let end = data.iter().rposition(|&b| !is_whitespace(b)).map(|i| i + 1).unwrap_or(0);
    if start < end {
        &data[start..end]
    } else {
        &[]
    }
}

fn is_whitespace(b: u8) -> bool {
    b == b' ' || b == b'\t' || b == b'\n' || b == b'\r'
}

fn split_on_prefixes(data: &[u8]) -> Vec<Vec<u8>> {
    let prefixes: &[&[u8]] = &[
        b"GM|", b"GA;", b"BN|", b"HC", b"HC|", b"GN|", b"GT|", b"PV?",
    ];

    let mut positions = Vec::new();
    for &prefix in prefixes {
        let mut i = 0;
        while let Some(pos) = find_prefix(data, i, prefix) {
            positions.push(pos);
            i = pos + 1;
        }
    }

    let mut messages = Vec::new();
    if positions.is_empty() {
        messages.push(data.to_vec());
    } else {
        positions.sort();
        positions.dedup();
        let mut prev = 0;
        for &pos in &positions {
            if pos > prev {
                messages.push(data[prev..pos].to_vec());
            }
            prev = pos;
        }
        if prev < data.len() {
            messages.push(data[prev..].to_vec());
        }
    }

    messages
}

fn find_prefix(data: &[u8], start: usize, prefix: &[u8]) -> Option<usize> {
    for i in start..=(data.len().saturating_sub(prefix.len())) {
        if data[i..i + prefix.len()] == *prefix {
            return Some(i);
        }
    }
    None
}