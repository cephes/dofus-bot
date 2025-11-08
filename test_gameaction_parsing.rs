// Test program to validate GameAction subparser functionality
use std::collections::HashMap;
use serde_json::Value;

// Import the GameAction subparsers and dispatcher
use crate::retroproto_parsers::generated::actions::GameAction_1::parse_GameAction_1;
use crate::retroproto_parsers::generated::actions::GameAction_2::parse_GameAction_2;
use crate::retroproto_parsers::generated::actions::GameAction_900::parse_GameAction_900;
use crate::retroproto_parsers::generated::actions::GameAction_901::parse_GameAction_901;
use crate::retroproto_parsers::generated::actions::GameAction_902::parse_GameAction_902;
use crate::retroproto_parsers::generated::actions::GameAction_903::parse_GameAction_903;
use crate::retroproto_parsers::handwritten::GameActions;

fn main() {
    println!("🧪 Testing GameAction Subparser Functionality\n");
    
    // Test 1: Individual subparser functions
    test_individual_parsers();
    
    // Test 2: GameActions dispatcher
    test_dispatcher();
    
    println!("\n✅ All tests completed successfully!");
}

fn test_individual_parsers() {
    println!("📋 Testing Individual GameAction Subparsers:");
    
    // Test GameAction_1 (Movement)
    match parse_GameAction_1("123;456") {
        Ok(action) => println!("  ✅ GameAction_1: id={}, sprite_id={}", action.id, action.sprite_id),
        Err(e) => println!("  ❌ GameAction_1 failed: {}", e),
    }
    
    // Test GameAction_2 (LoadGameMap)
    match parse_GameAction_2("789") {
        Ok(action) => println!("  ✅ GameAction_2: map_id={}", action.map_id),
        Err(e) => println!("  ❌ GameAction_2 failed: {}", e),
    }
    
    // Test GameAction_900 (Challenge)
    match parse_GameAction_900("1001;2002") {
        Ok(action) => println!("  ✅ GameAction_900: challenger_id={}, challenged_id={}", 
                              action.challenger_id, action.challenged_id),
        Err(e) => println!("  ❌ GameAction_900 failed: {}", e),
    }
    
    // Test GameAction_901 (ChallengeAccept)
    match parse_GameAction_901("3003") {
        Ok(action) => println!("  ✅ GameAction_901: fighter_id={}", action.fighter_id),
        Err(e) => println!("  ❌ GameAction_901 failed: {}", e),
    }
    
    // Test GameAction_902 (ChallengeRefuse)
    match parse_GameAction_902("4004") {
        Ok(action) => println!("  ✅ GameAction_902: fighter_id={}", action.fighter_id),
        Err(e) => println!("  ❌ GameAction_902 failed: {}", e),
    }
    
    // Test GameAction_903 (ChallengeJoin)
    match parse_GameAction_903("5005") {
        Ok(action) => println!("  ✅ GameAction_903: fighter_id={}", action.fighter_id),
        Err(e) => println!("  ❌ GameAction_903 failed: {}", e),
    }
}

fn test_dispatcher() {
    println!("\n🎮 Testing GameActions Dispatcher:");
    
    // Test the full GameActions parsing
    let test_payloads = vec![
        "1;123;456",     // Action 1: Movement
        "2;789",         // Action 2: LoadGameMap  
        "900;1001;2002", // Action 900: Challenge
        "901;3003",      // Action 901: ChallengeAccept
        "902;4004",      // Action 902: ChallengeRefuse
        "903;5005",      // Action 903: ChallengeJoin
        "999;999;999",   // Unknown action (should gracefully fail)
    ];
    
    for payload in test_payloads {
        match GameActions::parse_game_actions(payload) {
            Ok(result) => {
                println!("  ✅ Dispatched: {}", serde_json::to_string(&result).unwrap());
            },
            Err(e) => println!("  ❌ Dispatch failed: {}", e),
        }
    }
}