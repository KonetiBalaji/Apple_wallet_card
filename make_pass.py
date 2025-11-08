#!/usr/bin/env python3
"""
Legacy script for backward compatibility.
Use 'wallet-card generate' CLI command or web UI for new projects.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wallet_card.templates.business_card import BusinessCardTemplate
from wallet_card.utils.config_loader import ConfigLoader

def main():
    """Generate wallet card using default or example config."""
    # Try to load example config, fallback to default
    config_paths = [
        "config/example.yaml",
        "config/default.yaml",
        "config.yaml",
    ]
    
    config = None
    for path in config_paths:
        if Path(path).exists():
            print(f"Using configuration: {path}")
            config = ConfigLoader.load_config(path)
            break
    
    if not config:
        print("No configuration file found. Using defaults.")
        print("Run 'wallet-card init-config' to create a configuration file.")
        config = ConfigLoader.load_config()
    
    # Generate pass
    template = BusinessCardTemplate()
    output_path = template.generate(config)
    
    print(f"✅ Pass created: {output_path}")
    print("Airdrop/email this file to your iPhone and tap 'Add to Wallet'.")

if __name__ == "__main__":
    main()

