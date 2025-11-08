fn main() {
    // Only apply npcap linking when pcap feature is enabled
    if std::env::var("CARGO_FEATURE_PCAP").is_ok() {
        if let Ok(npcap_dir) = std::env::var("NPCAP_SDK_DIR") {
            println!("cargo:rustc-link-search=native={}/Lib/x64", npcap_dir);
            println!("cargo:rustc-link-lib=wpcap");
            println!("cargo:rerun-if-env-changed=NPCAP_SDK_DIR");
        } else {
            println!("Warning: NPCAP_SDK_DIR environment variable not set. pcap feature will fail to link without it.");
        }
    }
}