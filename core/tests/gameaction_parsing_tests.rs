// GameAction subparser validation tests
use dofus_core::retroproto_parsers::generated::actions::{
    GameAction_1::parse_GameAction_1,
    GameAction_2::parse_GameAction_2,
    GameAction_900::parse_GameAction_900,
    GameAction_901::parse_GameAction_901,
    GameAction_902::parse_GameAction_902,
    GameAction_903::parse_GameAction_903,
};
use dofus_core::retroproto_parsers::handwritten::GameActions;

#[test]
fn test_gameaction_1_parsing() {
    let result = parse_GameAction_1("123;456");
    assert!(result.is_ok());
    let action = result.unwrap();
    assert_eq!(action.id, 123);
    assert_eq!(action.sprite_id, 456);
}

#[test]
fn test_gameaction_2_parsing() {
    let result = parse_GameAction_2("123;456");
    assert!(result.is_ok());
    let action = result.unwrap();
    assert_eq!(action.sprite_id, 123);
    assert_eq!(action.cinematic, 456);
}

#[test]
fn test_gameaction_900_parsing() {
    let result = parse_GameAction_900("1001;2002");
    assert!(result.is_ok());
    let action = result.unwrap();
    assert_eq!(action.challenger_id, 1001);
    assert_eq!(action.challenged_id, 2002);
}

#[test]
fn test_gameaction_901_parsing() {
    let result = parse_GameAction_901("3003;4004");
    assert!(result.is_ok());
    let action = result.unwrap();
    assert_eq!(action.challenger_id, 3003);
    assert_eq!(action.challenged_id, 4004);
}

#[test]
fn test_gameaction_902_parsing() {
    let result = parse_GameAction_902("5005;6006");
    assert!(result.is_ok());
    let action = result.unwrap();
    assert_eq!(action.challenger_id, 5005);
    assert_eq!(action.challenged_id, 6006);
}

#[test]
fn test_gameaction_903_parsing() {
    let result = parse_GameAction_903("7007;E");
    assert!(result.is_ok());
    let action = result.unwrap();
    assert_eq!(action.challenger_id, 7007);
    assert_eq!(action.error_reason, 'E');
}

#[test]
fn test_gameactions_dispatcher_action_1() {
    let result = GameActions::parse_game_actions("1;123;456");
    assert!(result.is_ok());
    let parsed = result.unwrap();
    assert_eq!(parsed.action_code, 1);
    // Verify payload is parsed correctly
    let payload_str = serde_json::to_string(&parsed.payload).unwrap();
    assert!(payload_str.contains("\"id\":123"));
    assert!(payload_str.contains("\"sprite_id\":456"));
}

#[test]
fn test_gameactions_dispatcher_action_2() {
    let result = GameActions::parse_game_actions("2;123;456");
    assert!(result.is_ok());
    let parsed = result.unwrap();
    assert_eq!(parsed.action_code, 2);
    // Verify payload is parsed correctly
    let payload_str = serde_json::to_string(&parsed.payload).unwrap();
    assert!(payload_str.contains("\"sprite_id\":123"));
    assert!(payload_str.contains("\"cinematic\":456"));
}

#[test]
fn test_gameactions_dispatcher_action_900() {
    let result = GameActions::parse_game_actions("900;1001;2002");
    assert!(result.is_ok());
    let parsed = result.unwrap();
    assert_eq!(parsed.action_code, 900);
    let payload_str = serde_json::to_string(&parsed.payload).unwrap();
    assert!(payload_str.contains("\"challenger_id\":1001"));
    assert!(payload_str.contains("\"challenged_id\":2002"));
}

#[test]
fn test_gameactions_dispatcher_unknown_action() {
    let result = GameActions::parse_game_actions("999;test;data");
    assert!(result.is_ok());
    let parsed = result.unwrap();
    assert_eq!(parsed.action_code, 999);
    // Unknown actions should return JSON with metadata
    let payload_str = serde_json::to_string(&parsed.payload).unwrap();
    assert!(payload_str.contains("\"action_code\":999"));
    assert!(payload_str.contains("\"unparsed_rest\":\"test;data\""));
    assert!(payload_str.contains("\"note\":\"Action-specific parser not available\""));
}