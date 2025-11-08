"""
Flow Extractor for PCAP Files

This module provides functionality to extract and reassemble network flows from PCAP files.
It groups packets by 5-tuple, reassembles payloads, and writes each flow to a binary file.

Assumptions and Limitations:
- TCP reassembly uses sequence numbers for ordering but does not handle retransmissions or gaps beyond basic ordering.
- UDP flows are assembled in capture order.
- Only packets with Raw payload are processed.
- Memory usage scales with number of flows; for very large pcaps, consider external filtering.
"""

import os
import logging
from typing import List, Tuple, Optional, Dict
from collections import defaultdict
from scapy.all import rdpcap, Packet, IP, TCP, UDP, Raw

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def reassemble_tcp_segments(segments: List[Tuple[int, bytes]]) -> bytes:
    """
    Reassemble TCP segments by sequence number.

    Args:
        segments: List of (seq_num, payload) tuples.

    Returns:
        Concatenated payload in sequence order.
    """
    # Sort by sequence number
    segments.sort(key=lambda x: x[0])
    # Simple concatenation; does not handle overlaps or gaps
    return b''.join(payload for _, payload in segments)

def extract_flows(
    pcap_path: str,
    out_dir: str = "examples/pcap/flows",
    proto_filter: Optional[str] = None,
    src_ip: Optional[str] = None,
    dst_ip: Optional[str] = None,
    min_bytes: int = 1
) -> List[str]:
    """
    Extract flows from a PCAP file and write to binary files.

    Args:
        pcap_path: Path to the PCAP file.
        out_dir: Output directory for flow files.
        proto_filter: Filter by protocol ('TCP' or 'UDP').
        src_ip: Filter by source IP.
        dst_ip: Filter by destination IP.
        min_bytes: Minimum flow size in bytes.

    Returns:
        List of written file paths.
    """
    os.makedirs(out_dir, exist_ok=True)
    packets = rdpcap(pcap_path)
    flows: Dict[Tuple[str, str, int, str, int], List[Tuple[int, bytes]]] = defaultdict(list)

    for pkt in packets:
        if not pkt.haslayer(Raw):
            continue  # Skip packets without payload

        ip_layer = pkt.getlayer(IP)
        if not ip_layer:
            continue

        proto = None
        src_port = dst_port = 0
        seq = 0

        if pkt.haslayer(TCP):
            proto = 'TCP'
            tcp_layer = pkt[TCP]
            src_port = tcp_layer.sport
            dst_port = tcp_layer.dport
            seq = tcp_layer.seq
        elif pkt.haslayer(UDP):
            proto = 'UDP'
            udp_layer = pkt[UDP]
            src_port = udp_layer.sport
            dst_port = udp_layer.dport
        else:
            continue  # Skip non-TCP/UDP

        if proto_filter and proto != proto_filter.upper():
            continue

        src = ip_layer.src
        dst = ip_layer.dst

        if src_ip and src != src_ip:
            continue
        if dst_ip and dst != dst_ip:
            continue

        # Normalize flow key: sort IPs and ports to make bidirectional flows the same
        if (src, src_port) > (dst, dst_port):
            flow_key = (proto, dst, dst_port, src, src_port)
        else:
            flow_key = (proto, src, src_port, dst, dst_port)

        payload = bytes(pkt[Raw])
        flows[flow_key].append((seq, payload))

    written_files = []
    for i, (flow_key, segments) in enumerate(flows.items()):
        proto, src_ip, src_port, dst_ip, dst_port = flow_key

        if proto == 'TCP':
            payload = reassemble_tcp_segments(segments)
        else:  # UDP
            # For UDP, just concatenate in order
            payload = b''.join(payload for _, payload in segments)

        if len(payload) < min_bytes:
            continue

        filename = f"flow_{i:03d}_{proto}_{src_ip}_{src_port}_{dst_ip}_{dst_port}.bin"
        filepath = os.path.join(out_dir, filename)

        # Atomic write
        tmp_path = filepath + '.tmp'
        with open(tmp_path, 'wb') as f:
            f.write(payload)
        os.replace(tmp_path, filepath)

        written_files.append(filepath)
        logging.info(f"Written {len(payload)} bytes to {filepath}")

    return written_files