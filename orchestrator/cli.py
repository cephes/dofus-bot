#!/usr/bin/env python3
"""
CLI wrapper for flow extraction tools.
"""

import argparse
import os
import sys
from tools.extract_flows import extract_flows

def main():
    parser = argparse.ArgumentParser(description="Flow Extractor CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    extract_parser = subparsers.add_parser('extract', help='Extract flows from PCAP')
    extract_parser.add_argument('pcap_path', help='Path to PCAP file')
    extract_parser.add_argument('--out-dir', default='examples/pcap/flows', help='Output directory')
    extract_parser.add_argument('--proto', choices=['TCP', 'UDP'], help='Filter by protocol')
    extract_parser.add_argument('--min-bytes', type=int, default=1, help='Minimum flow size')
    extract_parser.add_argument('--filter-src', help='Filter by source IP')
    extract_parser.add_argument('--filter-dst', help='Filter by destination IP')

    args = parser.parse_args()

    if args.command == 'extract':
        try:
            files = extract_flows(
                pcap_path=args.pcap_path,
                out_dir=args.out_dir,
                proto_filter=args.proto,
                src_ip=args.filter_src,
                dst_ip=args.filter_dst,
                min_bytes=args.min_bytes
            )
            print(f"Extracted {len(files)} flows:")
            for f in files:
                size = os.path.getsize(f)
                print(f"  {f}: {size} bytes")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()