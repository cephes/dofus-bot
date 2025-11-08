use std::cmp::Ordering;

/// Return start offsets of messages in `s`, using a whitelist of `prefixes`.
/// Boundary rules:
///  - Left boundary: start-of-text or previous char NOT [A-Za-z0-9]
///  - Token: one of the known prefixes (longest-first match)
///  - Right boundary: next char is a digit OR one of ';', '|', '+', '-', '?' OR end-of-text
pub fn find_prefix_starts(s: &str, prefixes: &[String]) -> Vec<usize> {
    // Sort once (caller can cache); we re-sort to be safe.
    let mut ps: Vec<&str> = prefixes.iter().map(|p| p.as_str()).collect();
    ps.sort_by(|a, b| match b.len().cmp(&a.len()) {
        Ordering::Equal => a.cmp(b),
        other => other,
    });

    let bytes = s.as_bytes();
    let mut starts = Vec::new();
    let mut i = 0;
    while i < bytes.len() {
        // Left boundary
        let left_ok = if i == 0 {
            true
        } else {
            !is_ascii_alnum(bytes[i - 1])
        };

        if left_ok {
            // Try longest-first prefix match
            if let Some((plen, right_ok)) = match_prefix_right(bytes, i, &ps) {
                if right_ok {
                    starts.push(i);
                    // Move to end of this token to avoid finding nested starts right away
                    i = i.saturating_add(plen);
                    continue;
                }
            }
        }
        i += 1;
    }
    starts
}

fn is_ascii_alnum(b: u8) -> bool {
    (b'A'..=b'Z').contains(&b) || (b'a'..=b'z').contains(&b) || (b'0'..=b'9').contains(&b)
}

fn right_boundary_ok(next: Option<u8>) -> bool {
    match next {
        None => true,
        // Treat NUL (0x00) as a valid delimiter as well.
        Some(c) => c == 0 || c.is_ascii_digit() || matches!(c, b';' | b'|' | b'+' | b'-' | b'?'),
    }
}

fn match_prefix_right(bytes: &[u8], i: usize, ps: &[&str]) -> Option<(usize, bool)> {
    for p in ps {
        let plen = p.len();
        if i + plen > bytes.len() {
            continue;
        }
        if &bytes[i..i + plen] == p.as_bytes() {
            let right = if i + plen >= bytes.len() {
                None
            } else {
                Some(bytes[i + plen])
            };
            return Some((plen, right_boundary_ok(right)));
        }
    }
    None
}