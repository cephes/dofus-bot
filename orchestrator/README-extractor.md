# Flow Extractor

Extracts network flows from PCAP files and writes concatenated payloads to binary files.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r orchestrator/requirements-extract.txt
```

## Usage

```powershell
python orchestrator/cli.py extract .\examples\pcap\sample.pcap --out-dir .\examples\pcap\flows --proto TCP --min-bytes 16
```

Output files are named `flow_{n:03d}_{proto}_{srcip}_{sport}_{dstip}_{dport}.bin`.

Feed `.bin` files to the core parser:

```powershell
cargo run -- --mode dofus --input .\examples\pcap\flows\flow_000_TCP_192.168.1.1_12345_192.168.1.2_80.bin --output decoded.json