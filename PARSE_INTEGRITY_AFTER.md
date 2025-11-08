# Parse Integrity Summary

## Overall Statistics

- **Total rows processed:** 249
- **Parsed OK:** 146 (58.6%)
- **Parsed empty object:** 86 (34.5%)
- **Parsed null:** 0 (0.0%)
- **Parse errors present:** 17 (6.8%)

## Violations Overview

**Total violations found: 108**

### Violation Types

- **parsed_empty_object:** 86 occurrences
- **parsed_null:** 17 occurrences
- **parse_error_present: no parser registered for GameActionAck:** 13 occurrences
- **parse_error_present: invalid action_code: invalid digit found in string:** 4 occurrences
- **type_mismatch: value expected str, got int:** 3 occurrences
- **missing_required_field: Value:** 2 occurrences

## Per-Message Statistics

| Message Name | Total | OK | Empty | Null | Error | Failure Rate |
|-------------|-------|----|-----|------|-------|-------------|
| GameActionAck | 13 | 0 | 0 | 0 | 13 | 100.0% |
| GameActionsStart | 10 | 0 | 10 | 0 | 0 | 100.0% |
| GameTurnMiddle | 9 | 0 | 9 | 0 | 0 | 100.0% |
| GameActionsFinish | 9 | 0 | 9 | 0 | 0 | 100.0% |
| BasicsNothing | 9 | 0 | 9 | 0 | 0 | 100.0% |
| GameEffect | 9 | 0 | 9 | 0 | 0 | 100.0% |
| GameTurnStart | 8 | 0 | 8 | 0 | 0 | 100.0% |
| GameTurnReady | 8 | 0 | 8 | 0 | 0 | 100.0% |
| GameTurnFinish | 7 | 0 | 7 | 0 | 0 | 100.0% |
| AksServerMessage | 3 | 3 | 0 | 0 | 0 | 100.0% |
| GamePlayersCoordinates | 3 | 0 | 3 | 0 | 0 | 100.0% |
| BasicsTime | 2 | 2 | 0 | 0 | 0 | 100.0% |
| GameMapLoaded | 2 | 0 | 2 | 0 | 0 | 100.0% |
| ExchangeCraftPublicMode | 2 | 0 | 2 | 0 | 0 | 100.0% |
| GameReady | 2 | 0 | 2 | 0 | 0 | 100.0% |
| GameSetPlayerPosition | 2 | 0 | 2 | 0 | 0 | 100.0% |
| GameStartToPlay | 1 | 0 | 1 | 0 | 0 | 100.0% |
| GameTurnList | 1 | 0 | 1 | 0 | 0 | 100.0% |
| GameFightChallenge | 1 | 0 | 1 | 0 | 0 | 100.0% |
| GameEnd | 1 | 0 | 1 | 0 | 0 | 100.0% |
| HousesLockedProperty | 1 | 0 | 1 | 0 | 0 | 100.0% |
| AksServerWillDisconnect | 1 | 0 | 1 | 0 | 0 | 100.0% |
| GameActions | 92 | 88 | 0 | 0 | 4 | 4.3% |
| GameMovement | 14 | 14 | 0 | 0 | 0 | 0.0% |
| AccountStats | 12 | 12 | 0 | 0 | 0 | 0.0% |
| ItemsWeight | 11 | 11 | 0 | 0 | 0 | 0.0% |
| InfosMessage | 3 | 3 | 0 | 0 | 0 | 0.0% |
| ItemsQuantity | 3 | 3 | 0 | 0 | 0 | 0.0% |
| GameMapData | 2 | 2 | 0 | 0 | 0 | 0.0% |
| FightsCount | 2 | 2 | 0 | 0 | 0 | 0.0% |
| GameMovementRemove | 1 | 1 | 0 | 0 | 0 | 0.0% |
| InfosLifeRestoreTimerFinish | 1 | 1 | 0 | 0 | 0 | 0.0% |
| BasicsDate | 1 | 1 | 0 | 0 | 0 | 0.0% |
| GameCreateSuccess | 1 | 1 | 0 | 0 | 0 | 0.0% |
| InfosLifeRestoreTimerStart | 1 | 1 | 0 | 0 | 0 | 0.0% |
| GameCreate | 1 | 1 | 0 | 0 | 0 | 0.0% |

## Sample Failures

First 10 failed rows with failure reasons:

### 1. Frame 1 - AksServerMessage
- **Status:** fail
- **Reasons:** type_mismatch: value expected str, got int
- **Prefix:** M

### 2. Frame 8 - BasicsTime
- **Status:** fail
- **Reasons:** missing_required_field: Value
- **Prefix:** BT

### 3. Frame 14 - GameMapLoaded
- **Status:** fail
- **Reasons:** parsed_empty_object
- **Prefix:** GDK

### 4. Frame 15 - ExchangeCraftPublicMode
- **Status:** fail
- **Reasons:** parsed_empty_object
- **Prefix:** EW

### 5. Frame 28 - GamePlayersCoordinates
- **Status:** fail
- **Reasons:** parsed_empty_object
- **Prefix:** GIC

### 6. Frame 29 - GamePlayersCoordinates
- **Status:** fail
- **Reasons:** parsed_empty_object
- **Prefix:** GIC

### 7. Frame 30 - GameReady
- **Status:** fail
- **Reasons:** parsed_empty_object
- **Prefix:** GR

### 8. Frame 31 - GamePlayersCoordinates
- **Status:** fail
- **Reasons:** parsed_empty_object
- **Prefix:** GIC

### 9. Frame 32 - GameStartToPlay
- **Status:** fail
- **Reasons:** parsed_empty_object
- **Prefix:** GS

### 10. Frame 33 - GameTurnList
- **Status:** fail
- **Reasons:** parsed_empty_object
- **Prefix:** GTL

