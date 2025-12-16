#!/usr/bin/env python3
"""
Simple SDK Query Example

This demonstrates the simplest way to use the Claude Agent SDK
for one-off queries without managing the agent lifecycle.
"""

import os
import sys
import anyio

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.autonomous_agent import simple_query


async def main():
    """Demonstrate simple SDK query usage."""
    print("="*70)
    print("Simple Claude Agent SDK Query Example")
    print("="*70)
    print()
    
    # Example 1: Quick query
    print("Example 1: Quick status check")
    print("-"*70)
    result = await simple_query(
        "How many Datadog monitors do I have in total?",
        verbose=True
    )
    print(f"\nResult: {result}\n")
    
    # Example 2: Another quick query
    print("\nExample 2: Alert check")
    print("-"*70)
    result = await simple_query(
        "Are there any monitors in alert state right now?",
        verbose=True
    )
    print(f"\nResult: {result}\n")
    
    print("="*70)
    print("✓ Simple queries complete!")
    print("="*70)


if __name__ == "__main__":
    anyio.run(main)

