# Parser Coverage Report

- Generated: 2025-11-07T02:05:02.207594Z
- NDJSON: `..\examples\pcap\decoded\dummy_parsed_all.ndjson`

## Totals
- Rows: 249
- Structured rows: 146
- Empty-object rows: 86
- Null rows: 17
- Rows with parse_error set: 17

## Registry / Rust Sources
- Rust message files found: 511 (generated + handwritten)
- Registry names detected: 509

## Top Missing (seen in NDJSON but no Rust parse fn or not registered)
- **GameActions** — seen 92×, parse_fn=False, registered=True (file=core\src\retroproto_parsers\handwritten\GameActions.rs)
- **GameActionAck** — seen 13×, parse_fn=True, registered=False (file=core\src\retroproto_parsers\generated\GameActionAck.rs)
- **GameEffect** — seen 9×, parse_fn=False, registered=True (file=core\src\retroproto_parsers\handwritten\GameEffect.rs)

## Messages With Null Output Only
- GameActionAck

## Sample of Structured Messages (fields)
- **AccountStats** — fields: alignment, alignment_enabled, alignment_level, bonus_points, bonus_points_spell, characteristics, discernment, disgrace, energy, energy_max
- **AksServerMessage** — fields: value
- **BasicsDate** — fields: day, month, year
- **BasicsTime** — fields: value
- **FightsCount** — fields: value
- **GameActions** — fields: action_code, payload
- **GameCreate** — fields: rr_type
- **GameCreateSuccess** — fields: rr_type
- **GameMapData** — fields: id, key, name
- **GameMovement** — fields: sprites
- **GameMovementRemove** — fields: id
- **InfosLifeRestoreTimerFinish** — fields: restored
- **InfosLifeRestoreTimerStart** — fields: interval
- **InfosMessage** — fields: chat_id, messages
- **ItemsQuantity** — fields: id, quantity
- **ItemsWeight** — fields: current, max

## By Prefix Outcome Counts
- **As** — structured:12
- **BD** — structured:1
- **BN** — empty:9
- **BT** — structured:2
- **EW** — empty:2
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
- **GKK** — null:13
- **GM** — structured:14
- **GM|-** — structured:1
- **GR** — empty:2
- **GS** — empty:1
- **GTF** — empty:7
- **GTL** — empty:1
- **GTM** — empty:9
- **GTR** — empty:8
- **GTS** — empty:8
- **Gd** — empty:1
- **Gp** — empty:2
- **ILF** — structured:1
- **ILS** — structured:1
- **Im** — structured:3
- **M** — structured:3
- **OQ** — structured:3
- **Ow** — structured:11
- **fC** — structured:2
- **hX** — empty:1
- **k** — empty:1
