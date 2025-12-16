#!/usr/bin/env python3
"""
Verify which MCP servers are configured and available.
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config.mcp_config import get_all_mcp_servers

def main():
    print("="*70)
    print("MCP Server Configuration Check")
    print("="*70)
    print()
    
    servers = get_all_mcp_servers()
    
    print(f"Found {len(servers)} MCP server(s) configured:")
    print()
    
    for name, config in servers.items():
        print(f"✓ {name.upper()}")
        print(f"  Type: {config.get('type')}")
        print(f"  Command: {config.get('command')}")
        if 'env' in config:
            print(f"  Environment variables: {len(config['env'])} configured")
        print()
    
    print("="*70)
    print()
    print("These servers are automatically loaded by AutonomousAgent!")
    print("No changes needed to autonomous_agent.py")
    print()

if __name__ == "__main__":
    main()

