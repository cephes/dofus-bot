use clap::Parser;
use serde::Serialize;
use std::fs::File;
use std::io::Write;
use dofus_core::dofus_proto;

#[derive(Parser)]
#[command(name = "dofus-core")]
#[command(about = "Dofus bot core engine")]
struct Args {
    /// Path to the input file (pcap or raw data)
    #[arg(short, long)]
    input: String,

    /// Output JSON file
    #[arg(short, long, default_value = "output.json")]
    output: String,

    /// Mode: pcap or dofus
    #[arg(short, long, default_value = "pcap")]
    mode: String,

    /// Reassemble TCP stream before splitting (recommended).
    #[arg(long="reassemble", default_value_t = true)]
    pub reassemble: bool,
    /// Disable stream reassembly.
    #[arg(long="no-reassemble", action=clap::ArgAction::SetFalse, overrides_with="reassemble")]
    pub no_reassemble: bool,
}

#[derive(Serialize)]
#[allow(dead_code)]
struct PacketHeader {
    index: usize,
    payload: Vec<u8>,
    timestamp: String,
    length: usize,
    // Placeholder for parsed headers
    src_ip: Option<String>,
    dst_ip: Option<String>,
    protocol: Option<String>,
}

mod parser {
    use super::PacketHeader;

    #[allow(dead_code)]
    pub fn parse_packet(index: usize, data: &[u8]) -> PacketHeader {
        // Stubbed parsing: just return basic info
        PacketHeader {
            index,
            payload: data.to_vec(),
            timestamp: "stub".to_string(),
            length: data.len(),
            src_ip: Some("192.168.1.1".to_string()),
            dst_ip: Some("192.168.1.2".to_string()),
            protocol: Some("TCP".to_string()),
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let stream = std::fs::read(&args.input)?;
    let packets = dofus_proto::classify_stream(&stream);

    let mut json_frames: Vec<serde_json::Value> = Vec::new();

    for (index, packet) in packets.into_iter().enumerate() {
        let json_packet = serde_json::json!({
            "frame_index": index,
            "packet_kind": match &packet.kind {
                dofus_proto::PacketKind::Client(s) => format!("client:{}", s),
                dofus_proto::PacketKind::Server(s) => format!("server:{}", s),
                dofus_proto::PacketKind::Unknown(s) => format!("unknown:{}", s),
            },
            "length": packet.payload.len(),
            "payload_hex": hex::encode(&packet.payload),
            "header_meta": packet.header_meta.map(|m| serde_json::json!({
                "length_field_bytes": m.length_field_bytes,
                "raw_header": hex::encode(&m.raw_header),
                "parsed_length": m.parsed_length,
                "notes": m.notes
            }))
        });
        json_frames.push(json_packet);
    }

    let json = serde_json::to_string_pretty(&json_frames)?;
    let mut file = File::create(&args.output)?;
    file.write_all(json.as_bytes())?;

    println!("Parsed {} packets to {}", json_frames.len(), args.output);
    Ok(())
}