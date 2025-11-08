import pytest
import os
import tempfile
from scapy.all import IP, TCP, UDP, Raw, wrpcap
from tools.extract_flows import extract_flows, reassemble_tcp_segments

def test_reassemble_tcp_ordering():
    segments = [
        (200, b"second"),
        (100, b"first"),
    ]
    result = reassemble_tcp_segments(segments)
    assert result == b"firstsecond"

def test_extract_single_tcp_flow(tmp_path):
    # Create synthetic PCAP with TCP flow
    pkt1 = IP(src="192.168.1.1", dst="192.168.1.2") / TCP(sport=12345, dport=80, seq=100) / Raw(b"hello")
    pkt2 = IP(src="192.168.1.2", dst="192.168.1.1") / TCP(sport=80, dport=12345, seq=200) / Raw(b"world")

    pcap_path = tmp_path / "test.pcap"
    wrpcap(str(pcap_path), [pkt1, pkt2])

    out_dir = tmp_path / "flows"
    files = extract_flows(str(pcap_path), str(out_dir))

    assert len(files) == 1
    with open(files[0], 'rb') as f:
        data = f.read()
    assert data == b"helloworld"  # Reassembled in order

def test_extract_udp_and_filters(tmp_path):
    # Create PCAP with TCP and UDP flows
    tcp_pkt = IP(src="192.168.1.1", dst="192.168.1.2") / TCP(sport=12345, dport=80) / Raw(b"tcp")
    udp_pkt = IP(src="192.168.1.1", dst="192.168.1.2") / UDP(sport=12345, dport=53) / Raw(b"udp")

    pcap_path = tmp_path / "test.pcap"
    wrpcap(str(pcap_path), [tcp_pkt, udp_pkt])

    out_dir = tmp_path / "flows"

    # Filter UDP only
    files = extract_flows(str(pcap_path), str(out_dir), proto_filter="UDP")
    assert len(files) == 1
    with open(files[0], 'rb') as f:
        data = f.read()
    assert data == b"udp"