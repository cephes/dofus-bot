# AUTOHEAL Report

**Generated:** 2025-11-07 00:25:55
**Status:** FAILED

## Summary

- **Go Structs Scanned:** 565
- **Rust Structs Found:** 462
- **Files Changed:** 120
- **Fields Added:** 229
- **Type Changes:** 0
- **Parser Functions Created:** 0

## Changes Made

- Added fields to AccountAddCharacter: Name, Color1, Class, Color2, Color3, Sex
- Added fields to AccountBoost: CharacteristicId, Amount
- Added fields to AccountConfiguredPort: Port
- Added fields to AccountCredential: Hash, Username, CryptoMethod
- Added fields to AccountDeleteCharacter: SecretAnswer, Id
- Added fields to AccountGetGifts: Lang
- Added fields to AccountSearchForFriend: Pseudo
- Added fields to AccountSendIdentity: Id
- Added fields to AccountSendTicket: Ticket
- Added fields to AccountSetCharacter: Id
- Added fields to AccountSetServer: Id
- Added fields to AccountUseKey: Id
- Added fields to AccountVersion: Streaming, Beta, Major, Patch, Electron, Minor
- Added fields to ChatRequestSubscribeChannelAdd: Channels
- Added fields to ChatRequestSubscribeChannelRemove: Channels
- Added fields to ChatSend: Message, PrivateReceiver, ChatChannel
- Added fields to DialogBeginning: NPCId
- Added fields to DialogCreate: NPCId
- Added fields to DialogResponse: Answer, Question
- Added fields to EmotesSetDirection: Dir
- Added fields to ExchangeBigStoreBuy: Price, QuantityIndex, ItemId
- Added fields to ExchangeBigStoreItemList: ItemTemplateId
- Added fields to ExchangeBigStoreSearch: TemplateId, ItemType
- Added fields to ExchangeBigStoreType: ItemType
- Added fields to ExchangeGetItemMiddlePriceInBigStore: TemplateId
- Added fields to ExchangePutInCertificateFromShed: MountId
- Added fields to ExchangePutInInventoryFromShed: MountId
- Added fields to ExchangePutInMountParkFromShed: MountId
- Added fields to ExchangePutInShedFromCertificate: CertificateId
- Added fields to ExchangePutInShedFromInventory: MountId
- Added fields to ExchangePutInShedFromMountPark: MountId
- Added fields to ExchangeRequest: Cell, Id, Type
- Added fields to GameActionAck: Id
- Added fields to GameActionCancel: Params, Id
- Added fields to GameActionsSendActions: ActionType, ActionChallengeRefuse, ActionChallenge, ActionMovement, ActionChallengeAccept
- Added fields to GameActionsSendActionsActionMovement: DirAndCells
- Added fields to GameActionsSendActionsActionChallenge: ChallengedId
- Added fields to GameActionsSendActionsActionChallengeAccept: ChallengerId
- Added fields to GameActionsSendActionsActionChallengeRefuse: ChallengerId
- Added fields to GameCreate: Type
- Added fields to InfosSendScreenInfo: DisplayState, Width, Height
- Added fields to ItemsDestroy: Quantity, Id
- Added fields to ItemsDrop: Quantity, Id
- Added fields to ItemsRequestMovement: Quantity, Position, Id
- Added fields to ItemsUseConfirm: SpriteId, Cell, Id
- Added fields to ItemsUseNoConfirm: SpriteId, Cell, Id
- Added fields to MountRename: Name
- Added fields to MountRequestData: Validity, Id
- Added fields to SpellsBoost: Id
- Added fields to SpellsForget: Id
- Added fields to SpellsMoveToUsed: Position, Id
- Added fields to AccountCharacterAddError: Reason
- Added fields to AccountCharacterNameGeneratedError: Reason
- Added fields to AccountCharacterNameGeneratedSuccess: Name
- Added fields to AccountCharacterSelectedSuccess: Items, Name, Color1, Color2, Id, GFXId, Color3, Level, Sex
- Added fields to AccountCharactersListSuccess: CharactersCount, Characters, Subscription
- Added fields to AccountCommunity: Id
- Added fields to AccountHosts: Value
- Added fields to AccountLoginError: Extra, Reason
- Added fields to AccountLoginSuccess: Authorized
- Added fields to AccountNewLevel: Level
- Added fields to AccountPseudo: Value
- Added fields to AccountQueue: Position
- Added fields to AccountSecretQuestion: Value
- Added fields to AccountSelectServerError: Extra, Reason
- Added fields to AccountSelectServerPlainSuccess: Port, Host, Ticket
- Added fields to AccountSelectServerSuccess: Port, Host, Ticket
- Added fields to AccountServersListSuccess: ServersCharacters, Subscription
- Added fields to AccountStats: XP, Alignment, Initiative, FakeAlignment, AlignmentLevel, XPLow, Disgrace, BonusPointsSpell, BonusPoints, Discernment, Grade, AlignmentEnabled, EnergyMax, Honour, LPMax, XPHigh, Kama, Energy, Characteristics, LP
- Added fields to AccountTicketResponseSuccess: KeyId
- Added fields to AksHelloConnect: Salt
- Added fields to AksRPing: Value
- Added fields to AksServerMessage: Value
- Added fields to BasicsDate: Day, Year, Month
- Added fields to BasicsSubscriberRestrictionAdd: DialogId
- Added fields to BasicsTime: Value
- Added fields to ChatMessageError: Reason
- Added fields to ChatMessageSuccess: Name, PrivateTo, Id, ChatChannel, Message
- Added fields to ChatServerMessage: Message
- Added fields to DialogCreateSuccess: NPCId
- Added fields to DialogQuestion: Answers, QuestionParams, Question
- Added fields to EmotesList: Emotes
- Added fields to ExchangeBigStoreTypeItemsList: ItemTemplateIds, ItemType
- Added fields to ExchangeCreateSuccess: Paddock, NPCBuy, Type
- Added fields to ExchangeLeaveSuccess: TypePlayerExchange
- Added fields to ExchangeMountStorageAdd: NewBorn, Data
- Added fields to ExchangeMountStorageRemove: MountId
- Added fields to ExchangeRequestError: Reason
- Added fields to FightsCount: Value
- Added fields to GameActions: ActionLoadGameMap, ActionChallengeJoin, ActionType, ActionChallengeRefuse, ActionChallenge, ActionMovement, ActionChallengeAccept
- Added fields to GameActionsActionMovement: SpriteId, DirAndCells, Id
- Added fields to GameActionsActionLoadGameMap: SpriteId, Cinematic
- Added fields to GameActionsActionChallenge: ChallengedId, ChallengerId
- Added fields to GameActionsActionChallengeAccept: ChallengedId, ChallengerId
- Added fields to GameActionsActionChallengeRefuse: ChallengedId, ChallengerId
- Added fields to GameActionsActionChallengeJoin: ErrorReason, ChallengerId
- Added fields to GameCreateSuccess: Type
- Added fields to GameMapData: Name, Key, Id
- Added fields to GameMovement: Sprites
- Added fields to GameMovementRemove: Id
- Added fields to InfosLifeRestoreTimerFinish: Restored
- Added fields to InfosLifeRestoreTimerStart: Interval
- Added fields to InfosMessage: Messages, ChatId
- Added fields to ItemsAccessories: Accessories, Id
- Added fields to ItemsAddError: Reason
- Added fields to ItemsAddSuccess: Items
- Added fields to ItemsItemSetAdd: Effects, Id, ItemsTemplatesIds
- Added fields to ItemsItemSetRemove: Id
- Added fields to ItemsQuantity: Quantity, Id
- Added fields to ItemsRemove: Id
- Added fields to ItemsTool: JobId
- Added fields to ItemsWeight: Max, Current
- Added fields to MountEquipError: Reason
- Added fields to MountEquipSuccess: Data
- Added fields to SpecializationChange: Value
- Added fields to SpecializationSet: Value
- Added fields to SpellsChangeOption: CanUseSeeAllSpell
- Added fields to SpellsList: Spells
- Added fields to SpellsUpgradeSpellSuccess: Level, Id
- Added fields to TutorialShowTip: Id

## Top 20 Most Changed Files

| File | Changes |
|------|---------|
| AccountAddCharacter | 1 changes |
| AccountBoost | 1 changes |
| AccountConfiguredPort | 1 changes |
| AccountCredential | 1 changes |
| AccountDeleteCharacter | 1 changes |
| AccountGetGifts | 1 changes |
| AccountSearchForFriend | 1 changes |
| AccountSendIdentity | 1 changes |
| AccountSendTicket | 1 changes |
| AccountSetCharacter | 1 changes |
| AccountSetServer | 1 changes |
| AccountUseKey | 1 changes |
| AccountVersion | 1 changes |
| ChatRequestSubscribeChannelAdd | 1 changes |
| ChatRequestSubscribeChannelRemove | 1 changes |
| ChatSend | 1 changes |
| DialogBeginning | 1 changes |
| DialogCreate | 1 changes |
| DialogResponse | 1 changes |
| EmotesSetDirection | 1 changes |

## Build Results

**Status:** FAILED
**Command:** `cargo build --release -p dofus-core`

**Build Errors (first 50 lines):**
```
   Compiling dofus-core v0.1.0 (D:\WorkDir\dofus-bot\core)
error: expected one of `,`, `.`, `?`, `}`, or an operator, found `id`
  --> src\retroproto_parsers\generated\actions\GameActionAck.rs:20:1
   |
14 |     Ok(GameActionAck {
   |        ------------- while parsing this struct
...
18 |         idid: Default::default()
   |                                 -
   |                                 |
   |                                 expected one of `,`, `.`, `?`, `}`, or an operator
   |                                 help: try adding a comma: `,`
19 |
20 | id: Default::default()
   | ^^ unexpected token

error: expected `;`, found keyword `pub`
  --> src\retroproto_parsers\generated\actions\GameActionAck.rs:23:3
   |
23 | })
   |   ^ help: add `;` here
24 |
25 |   pub id: i64,
   |   --- unexpected token

error: visibility `pub` is not followed by an item
  --> src\retroproto_parsers\generated\actions\GameActionAck.rs:25:3
   |
25 |   pub id: i64,
   |   ^^^ the visibility
   |
   = help: you likely meant to define an item, e.g., `pub fn foo() {}`

error: expected identifier, found `:`
  --> src\retroproto_parsers\generated\actions\GameActionAck.rs:25:9
   |
25 |   pub id: i64,
   |         ^ expected identifier

error: expected one of `,`, `.`, `?`, `}`, or an operator, found `id`
  --> src\retroproto_parsers\generated\actions\GameActionCancel.rs:25:1
   |
16 |     Ok(GameActionCancel {
   |        ---------------- while parsing this struct
...
23 | id: Default::default(), params: Default::default()
   |                                                   -
   |                                                   |
   |                                                   expected one of `,`, `.`, `?`, `}`, or an operator
   |                                                   help: try adding a comma: `,`
24 |
25 | id: Default::default(), params: Default::default()
   | ^^ unexpected token

error: expected one of `,`, `.`, `?`, `}`, or an operator, found `params`
  -
```

## Idempotency Note

This script is idempotent - running it again will not duplicate changes or cause regressions.
All modified files were backed up to `.archive/AUTOHEAL_20251107_002453/` before changes.

## Next Steps

❌ Some build errors remain. Please review the build output above and iterate as needed.

---
*Generated by tools/align_rust_to_go.py*
