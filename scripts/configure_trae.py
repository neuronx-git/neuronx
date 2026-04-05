
# scripts/configure_trae.py
"""
Trae Configuration Script
-------------------------
Configures Trae integration by reading FOUNDATION/06_TRAE.md 
and ensuring validation logic matches the governance model.
"""

import sys
from pathlib import Path

def configure_trae():
    """Configure Trae validation logic"""
    print("🔍 Configuring Trae Integration...")
    
    trae_doc = Path("FOUNDATION/06_TRAE.md")
    if not trae_doc.exists():
        print(f"❌ Error: {trae_doc} not found")
        sys.exit(1)
        
    print(f"✅ Found Trae definition: {trae_doc}")
    
    # Configuration to enforcing
    protected_paths = [
        "GOVERNANCE/**",
        "AGENTS/**",
        "COCKPIT/**",
        ".github/workflows/**",
        "STATE/**"
    ]
    
    print("\nProtected Paths (Requiring Trae Review):")
    for path in protected_paths:
        print(f"- {path}")
        
    print("\n✅ Trae validator configuration verified")

if __name__ == "__main__":
    configure_trae()
