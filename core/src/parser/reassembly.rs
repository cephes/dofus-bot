use regex::Regex;

/// Build a length-desc, escaped alternation from known prefixes.
pub fn build_prefix_regex(prefixes: &[String]) -> Regex {
    // Sort by length desc so that longer tokens (e.g., "GM|-" before "GM|") win.
    let mut ps: Vec<String> = prefixes.iter().cloned().collect();
    ps.sort_by(|a, b| b.len().cmp(&a.len()));
    let parts: Vec<String> = ps.into_iter().map(|s| regex::escape(&s)).collect();

    // Boundary rules enforced in code since regex crate doesn't support lookbehind/lookahead:
    //  - Left boundary: previous char is NOT alphanumeric (or start-of-string).
    //  - Token: one of the known prefixes (alternation).
    //  - Right boundary: next char is a digit or Dofus delimiter ; | + - ?  OR end-of-string.
    // This avoids false hits like "Blacklist-" or base64-ish blobs.
    let pat = format!(r"(?m){}", parts.join("|"));

    // Be defensive: if building the giant alternation somehow fails, keep a minimal safe regex.
    Regex::new(&pat)
        .unwrap_or_else(|_| Regex::new(r"(?m)GM\|\-|GM\|").unwrap())
}

/// Split the whole text stream at valid, whitelisted prefixes.
pub fn split_stream_by_prefixes(stream: &[u8], rx: &Regex) -> Vec<Vec<u8>> {
    if stream.is_empty() { return Vec::new(); }
    let s = String::from_utf8_lossy(stream);

    // Find all candidate starts, enforcing boundaries in code.
    let mut starts: Vec<usize> = rx.find_iter(&s)
        .filter_map(|m| {
            let start = m.start();
            // Left boundary: previous char is NOT alphanumeric (or start-of-string).
            let left_ok = start == 0 || !s.as_bytes()[start - 1].is_ascii_alphanumeric();
            // Right boundary: next char is a digit or Dofus delimiter ; | + - ? OR NUL (0x00) OR end-of-string.
            let end = m.end();
            let right_ok = end == s.len() || matches!(s.as_bytes()[end], b'0'..=b'9' | b';' | b'|' | b'+' | b'-' | b'?' | 0);
            if left_ok && right_ok { Some(start) } else { None }
        })
        .collect();
    if starts.is_empty() { return Vec::new(); }
    starts.sort_unstable();

    // Build UTF-8 slices; protocol is text so re-encoding is fine.
    let mut chunks: Vec<Vec<u8>> = Vec::new();
    for (i, a) in starts.iter().enumerate() {
        let b = if i + 1 < starts.len() { starts[i + 1] } else { s.len() };
        if a < &b {
            chunks.push(s[*a..b].as_bytes().to_vec());
        }
    }
    chunks
}