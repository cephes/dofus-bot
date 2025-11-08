//! Unit tests for the 10 fixed retroproto parsers
//! These tests verify that the Rust parsers match the Go reference implementations

use dofus_core::retroproto_parsers::generated::*;

#[cfg(test)]
mod parse_tests {
    use super::*;

    #[test]
    fn test_aks_server_message() {
        // Go reference: m.Value = extra (entire payload is message string)
        let payload = "Server is going down for maintenance";
        let result = parse_AksServerMessage(payload).unwrap();
        
        assert_eq!(result.Value, payload);
        assert_eq!(result.value, 0); // lowercase field gets default
    }

    #[test]
    fn test_basics_date() {
        // Go reference: strings.Split(extra, "|"), year, month+1, day
        let payload = "2023|11|25"; // December 25, 2023 (month+1 = 12)
        let result = parse_BasicsDate(payload).unwrap();
        
        assert_eq!(result.Year, 2023);
        assert_eq!(result.Month, 12); // 11 + 1
        assert_eq!(result.Day, 25);
        assert_eq!(result.year, 2023);
        assert_eq!(result.month, 11); // raw month
        assert_eq!(result.day, 25);
    }

    #[test]
    fn test_basics_date_edge_cases() {
        // Test with invalid data
        let result = parse_BasicsDate("invalid|data").unwrap();
        assert_eq!(result.Year, 0);
        assert_eq!(result.Month, 1); // 0 + 1
        assert_eq!(result.Day, 0);
    }

    #[test]
    fn test_basics_time() {
        // Go reference: ParseInt(extra, 10, 64), timestamp handling
        let payload = "1609459200000"; // 2021-01-01 in milliseconds
        let result = parse_BasicsTime(payload).unwrap();
        
        assert_eq!(result.Value, payload);
        assert_eq!(result.value, 1609459200000);
    }

    #[test]
    fn test_game_map_data_pipe_format() {
        // Go reference: supports |id|name|key format
        let payload = "|12345|TestMap|abc123key";
        let result = parse_GameMapData(payload).unwrap();
        
        assert_eq!(result.Id, 12345);
        assert_eq!(result.Name, "TestMap");
        assert_eq!(result.Key, "abc123key");
        assert_eq!(result.id, 12345);
        assert_eq!(result.name, "TestMap");
        assert_eq!(result.key, "abc123key");
    }

    #[test]
    fn test_game_map_data_kv_format() {
        // Go reference: supports id=...,name=...,key=... format
        let payload = "id=54321,name=AnotherMap,key=xyz789";
        let result = parse_GameMapData(payload).unwrap();
        
        assert_eq!(result.Id, 54321);
        assert_eq!(result.Name, "AnotherMap");
        assert_eq!(result.Key, "xyz789");
    }

    #[test]
    fn test_game_movement() {
        // Go reference: preserves full sprites data as string array
        let payload = "+320;0;0;1;1^100*;1;1,2,3;accessories|~321;1;0;2;2^100;2;4,5,6;more";
        let result = parse_GameMovement(payload).unwrap();
        
        assert_eq!(result.Sprites.len(), 2);
        assert!(result.Sprites[0].starts_with('+'));
        assert!(result.Sprites[1].starts_with('~'));
        assert_eq!(result.sprites.len(), 2);
    }

    #[test]
    fn test_game_movement_remove() {
        // Go reference: ParseInt(extra, 10, 32) directly
        let payload = "42";
        let result = parse_GameMovementRemove(payload).unwrap();
        
        assert_eq!(result.Id, 42);
        assert_eq!(result.id, 42);
    }

    #[test]
    fn test_infos_life_restore_timer_start() {
        // Go reference: parse as time.Duration (milliseconds)
        let payload = "5000";
        let result = parse_InfosLifeRestoreTimerStart(payload).unwrap();
        
        assert_eq!(result.Interval, 5000);
        assert_eq!(result.interval, "5000");
    }

    #[test]
    fn test_infos_message() {
        // Go reference: chat ID from first char, rest split by |
        let payload = "1Hello|World|Test";
        let result = parse_InfosMessage(payload).unwrap();
        
        assert_eq!(result.ChatId, 1);
        assert_eq!(result.Messages.len(), 3);
        assert_eq!(result.Messages[0], "Hello");
        assert_eq!(result.Messages[1], "World");
        assert_eq!(result.Messages[2], "Test");
        assert_eq!(result.chat_id, 1);
        assert_eq!(result.messages.len(), 3);
    }

    #[test]
    fn test_infos_message_empty() {
        let result = parse_InfosMessage("").unwrap();
        assert_eq!(result.ChatId, 0);
        assert_eq!(result.Messages.len(), 0);
    }

    #[test]
    fn test_infos_message_single_char() {
        let payload = "3";
        let result = parse_InfosMessage(payload).unwrap();
        
        assert_eq!(result.ChatId, 3);
        assert_eq!(result.Messages.len(), 0);
    }

    #[test]
    fn test_items_quantity() {
        // Go reference: two integers separated by |
        let payload = "192837|100";
        let result = parse_ItemsQuantity(payload).unwrap();
        
        assert_eq!(result.Id, 192837);
        assert_eq!(result.Quantity, 100);
        assert_eq!(result.id, 192837);
        assert_eq!(result.quantity, 100);
    }

    #[test]
    fn test_items_weight() {
        // Go reference: two integers separated by |, handles empty fields
        let payload = "75|100";
        let result = parse_ItemsWeight(payload).unwrap();
        
        assert_eq!(result.Current, 75);
        assert_eq!(result.Max, 100);
        assert_eq!(result.current, 75);
        assert_eq!(result.max, 100);
    }

    #[test]
    fn test_items_weight_empty_fields() {
        let payload = "|100";
        let result = parse_ItemsWeight(payload).unwrap();
        
        assert_eq!(result.Current, 0); // empty field becomes 0
        assert_eq!(result.Max, 100);
    }

    #[test]
    fn test_items_weight_both_empty() {
        let payload = "||";
        let result = parse_ItemsWeight(payload).unwrap();
        
        assert_eq!(result.Current, 0);
        assert_eq!(result.Max, 0);
    }
}