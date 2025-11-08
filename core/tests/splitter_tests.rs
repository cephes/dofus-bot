use dofus_core::parser::splitter::split_dofus_messages;

#[test]
fn test_split_on_nul() {
    let payload = b"GM|test\x00GM|other";
    let messages = split_dofus_messages(payload);
    assert_eq!(messages.len(), 2);
    assert_eq!(messages[0], b"GM|test");
    assert_eq!(messages[1], b"GM|other");
}

#[test]
fn test_split_on_prefix_no_nul() {
    let payload = b"GM|firstGM|second";
    let messages = split_dofus_messages(payload);
    assert_eq!(messages.len(), 2);
    assert_eq!(messages[0], b"GM|first");
    assert_eq!(messages[1], b"GM|second");
}

#[test]
fn test_ignore_small_fragments() {
    let payload = b"GM|test\x00\x00\x00GM|other";
    let messages = split_dofus_messages(payload);
    assert_eq!(messages.len(), 2);
    assert_eq!(messages[0], b"GM|test");
    assert_eq!(messages[1], b"GM|other");
}

#[test]
fn test_trim_whitespace() {
    let payload = b"  GM|test  \x00GM|other  ";
    let messages = split_dofus_messages(payload);
    assert_eq!(messages.len(), 2);
    assert_eq!(messages[0], b"GM|test");
    assert_eq!(messages[1], b"GM|other");
}