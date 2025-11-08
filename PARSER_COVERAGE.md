# Parser Coverage Report

- Generated: 2025-11-06T20:09:18.285401Z
- NDJSON: `examples\pcap\decoded\dummy_parsed_new.ndjson`

## Totals
- Rows: 249
- Structured rows: 155
- Empty-object rows: 85
- Null rows: 9
- Rows with parse_error set: 9

## Registry / Rust Sources
- Rust message files found: 452 (generated + handwritten)
- Registry names detected: 467

## Top Missing (seen in NDJSON but no Rust parse fn or not registered)
- **GameActions** — seen 92×, parse_fn=False, registered=True (file=core\src\retroproto_parsers\handwritten\GameActions.rs)
- **GameEffect** — seen 9×, parse_fn=False, registered=True (file=core\src\retroproto_parsers\handwritten\GameEffect.rs)
- **ExchangeCraftPublicMode** — seen 2×, parse_fn=False, registered=False (file=None)
- **GameReady** — seen 2×, parse_fn=False, registered=False (file=None)
- **BasicsDate** — seen 1×, parse_fn=False, registered=False (file=None)

## Messages With Null Output Only
- BasicsDate
- ExchangeCraftPublicMode
- GameReady

## Sample of Structured Messages (fields)
- **AccountStats** — fields: alignment, alignmentEnabled, alignmentLevel, bonusPoints, bonusPointsSpell, discernment, disgrace, energy, energyMax, fakeAlignment
- **AksServerMessage** — fields: value
- **FightsCount** — fields: value
- **GameActionAck** — fields: id
- **GameActions** — fields: action_code, rest
- **GameCreate** — fields: type
- **GameCreateSuccess** — fields: type
- **GameMapData** — fields: id, key, name
- **GameMovement** — fields: sprites
- **GameMovementRemove** — fields: id
- **InfosLifeRestoreTimerFinish** — fields: restored
- **InfosMessage** — fields: chatId
- **ItemsQuantity** — fields: id, quantity
- **ItemsWeight** — fields: current, max

## By Prefix Outcome Counts
- **As** — structured:12
- **BD** — null:1
- **BN** — empty:9
- **BT** — empty:2
- **EW** — null:2
- **GA** — null:4, structured:88
- **GAF** — empty:9
- **GAS** — empty:10
- **GC** — structured:1
- **GCK** — structured:1
- **GDK** — empty:2
- **GDM** — structured:2
- **GE** — empty:1
- **GIC** — empty:3
- **GIE** — empty:9
- **GKK** — structured:13
- **GM** — structured:14
- **GM|-** — structured:1
- **GR** — null:2
- **GS** — empty:1
- **GTF** — empty:7
- **GTL** — empty:1
- **GTM** — empty:9
- **GTR** — empty:8
- **GTS** — empty:8
- **Gd** — empty:1
- **Gp** — empty:2
- **ILF** — structured:1
- **ILS** — empty:1
- **Im** — structured:3
- **M** — structured:3
- **OQ** — structured:3
- **Ow** — structured:11
- **fC** — structured:2
- **hX** — empty:1
- **k** — empty:1
