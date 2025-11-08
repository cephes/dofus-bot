import argparse
import json
import os
import subprocess
import sys
import pathlib
from typing import Tuple, Optional

def run_with_output_streaming(cmd, cwd=None, step_name="Step") -> Tuple[bool, str]:
    """
    Run a command with real-time stdout/stderr streaming and capture full output.
    Returns (success, full_output)
    """
    # Echo the command
    print(f"\n{'='*80}")
    print(f"STEP: {step_name}")
    print(f"COMMAND: {' '.join(map(str, cmd))}")
    if cwd:
        print(f"WORKDIR: {cwd}")
    print(f"{'='*80}")
    
    full_output = []
    
    try:
        # Use subprocess.Popen for real-time streaming
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream output in real-time
        if process.stdout:
            for line in process.stdout:
                print(line.rstrip())
                full_output.append(line.rstrip())
        
        # Wait for completion
        return_code = process.wait()
        
        if return_code != 0:
            print(f"\n{'!'*80}")
            print(f"STEP FAILED: {step_name}")
            print(f"COMMAND: {' '.join(map(str, cmd))}")
            print(f"EXIT CODE: {return_code}")
            
            # Show last ~60 lines of output
            if full_output:
                print(f"\nLAST ~60 LINES OF OUTPUT:")
                print(f"{'='*40}")
                recent_output = full_output[-60:]
                for line in recent_output:
                    print(line)
                print(f"{'='*40}")
            
            print(f"{'!'*80}\n")
            return False, '\n'.join(full_output)
        else:
            print(f"\n✓ STEP COMPLETED: {step_name}")
            return True, '\n'.join(full_output)
            
    except Exception as e:
        error_msg = f"Exception running command: {e}"
        print(f"\n{'!'*80}")
        print(f"STEP FAILED: {step_name}")
        print(f"COMMAND: {' '.join(map(str, cmd))}")
        print(f"ERROR: {error_msg}")
        print(f"{'!'*80}\n")
        return False, error_msg

def main():
    parser = argparse.ArgumentParser(
        description="Run the dummy parsing pipeline with configurable options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Run full pipeline
  %(prog)s --core-only --skip-registry       # Build only dofus-core, skip registry
  %(prog)s --no-stop                         # Continue even if steps fail
  %(prog)s --core-only                       # Build only dofus-core package
        """
    )
    
    parser.add_argument(
        "--skip-registry",
        action="store_true",
        help="Do not run tools/gen_parser_registry.py"
    )
    
    parser.add_argument(
        "--core-only",
        action="store_true", 
        help="Build only dofus-core package instead of full workspace"
    )
    
    parser.add_argument(
        "--no-stop",
        action="store_true",
        help="Continue pipeline even if one step fails (prints error, marks failure)"
    )
    
    parser.add_argument(
        "--input",
        default="examples/pcap/dummy.pcap",
        help="Path to input PCAP file (default: examples/pcap/dummy.pcap)"
    )
    
    parser.add_argument(
        "--out-stem",
        default="dummy",
        help="Output stem for generated files (default: dummy)"
    )
    
    args = parser.parse_args()
    
    # Setup paths
    ROOT = pathlib.Path(__file__).resolve().parents[1]
    CORE = ROOT / "core"
    BIN = CORE / "target" / "release"
    
    PCAP = ROOT / args.input
    FLOW = ROOT / "examples" / "pcap" / "decoded" / (args.out_stem + "_from_pcap.bin")
    REASS = ROOT / "examples" / "pcap" / "decoded" / (args.out_stem + "_reassembled.json")
    PARSED = ROOT / "examples" / "pcap" / "decoded" / (args.out_stem + "_parsed_all.json")
    NDJSON = ROOT / "examples" / "pcap" / "decoded" / (args.out_stem + "_parsed_all.ndjson")
    
    print(f"Dummy Pipeline Starting...")
    print(f"Working directory: {ROOT}")
    print(f"Flags: skip-registry={args.skip_registry}, core-only={args.core_only}, no-stop={args.no_stop}")
    
    # Track overall success
    overall_success = True
    step_count = 0
    
    try:
        # 1) Generate registry (unless skipped)
        step_count += 1
        if not args.skip_registry:
            success, output = run_with_output_streaming(
                [sys.executable, "tools/gen_parser_registry.py"],
                cwd=ROOT,
                step_name=f"Generate Registry ({step_count}/6)"
            )
            if not success:
                overall_success = False
                if not args.no_stop:
                    print("Pipeline stopped due to registry generation failure.")
                    sys.exit(1)
        else:
            print(f"\n[{step_count}/6] SKIPPING: Generate Registry (--skip-registry specified)")
        
        # 2) Build
        step_count += 1
        if args.core_only:
            build_cmd = ["cargo", "build", "--release", "-p", "dofus-core"]
            step_name = f"Build dofus-core only ({step_count}/6)"
        else:
            build_cmd = ["cargo", "build", "--release"]
            step_name = f"Build full workspace ({step_count}/6)"
        
        success, output = run_with_output_streaming(
            build_cmd,
            cwd=CORE,
            step_name=step_name
        )
        if not success:
            overall_success = False
            if not args.no_stop:
                print("Pipeline stopped due to build failure.")
                sys.exit(1)
        
        # 3) Make flow from PCAP (only if it doesn't exist)
        step_count += 1
        FLOW.parent.mkdir(parents=True, exist_ok=True)
        if not FLOW.exists():
            success, output = run_with_output_streaming(
                [str(BIN/"pcap2flow.exe"), "--pcap", str(PCAP), "--out", str(FLOW)],
                cwd=ROOT,
                step_name=f"PCAP to Flow ({step_count}/6)"
            )
            if not success:
                overall_success = False
                if not args.no_stop:
                    print("Pipeline stopped due to pcap2flow failure.")
                    sys.exit(1)
        else:
            print(f"\n[{step_count}/6] SKIPPING: PCAP to Flow (file already exists)")
        
        # 4) Reassemble TCP into logical frames
        step_count += 1
        success, output = run_with_output_streaming(
            [str(BIN/"reassemble.exe"), "--input", str(FLOW), "--output", str(REASS)],
            cwd=ROOT,
            step_name=f"Reassemble TCP ({step_count}/6)"
        )
        if not success:
            overall_success = False
            if not args.no_stop:
                print("Pipeline stopped due to reassembly failure.")
                sys.exit(1)
        
        # 5) Parse with registry-backed parser
        step_count += 1
        success, output = run_with_output_streaming(
            [str(BIN/"parse_messages.exe"), str(REASS), str(PARSED), str(NDJSON)],
            cwd=ROOT,
            step_name=f"Parse Messages ({step_count}/6)"
        )
        if not success:
            overall_success = False
            if not args.no_stop:
                print("Pipeline stopped due to parsing failure.")
                sys.exit(1)
        
        # 6) Summarize
        step_count += 1
        print(f"\n[{step_count}/6] SUMMARIZING RESULTS...")
        try:
            data = json.load(open(PARSED, "r", encoding="utf-8"))
            unknown = [d for d in data if d.get("parse_error")]
            summary = {
                "total": len(data),
                "unknown": len(unknown),
                "first": data[:5]
            }
            print(json.dumps(summary, indent=2))
            print("\nOutputs:")
            print(f"  JSON  : {PARSED}")
            print(f"  NDJSON: {NDJSON}")
        except Exception as e:
            print(f"Error summarizing results: {e}")
            overall_success = False
        
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user.")
        overall_success = False
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        overall_success = False
    
    # Final status
    print(f"\n{'='*80}")
    if overall_success:
        print("✓ PIPELINE COMPLETED SUCCESSFULLY")
        sys.exit(0)
    else:
        print("✗ PIPELINE FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()