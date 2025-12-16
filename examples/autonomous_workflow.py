#!/usr/bin/env python3
"""
Autonomous Workflow Example

This demonstrates how Claude autonomously decides which MCP tools to use
based on natural language queries using the official Claude Agent SDK.
This is the key feature that will allow us to add JIRA and GitHub MCP servers
- Claude will know when to use each one.
"""

import os
import sys
import anyio

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.autonomous_agent import AutonomousAgent


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


async def main():
    """Demonstrate autonomous workflows with Claude Agent SDK."""
    print_section("Autonomous Agent - Demo (Claude Agent SDK)")

    async with AutonomousAgent() as agent:

        # Example 1: Simple information query
        print_section("Example 1: Simple Query")
        print("Ask: 'What monitors are alerting?'")
        print("Claude will:")
        print("  1. Decide to use datadog_get_monitors tool")
        print("  2. Filter for alert state")
        print("  3. Summarize the results")
        print()
        input("Press Enter to run...")

        result = await agent.query(
            "What monitors are currently alerting in Datadog?",
            verbose=False
        )
        print(f"\nResult:\n{result}")

        # Example 2: Analysis query
        print_section("Example 2: Analysis Query")
        print("Ask: 'Analyze my production health'")
        print("Claude will:")
        print("  1. Call get_monitors to see overall state")
        print("  2. Identify concerning patterns")
        print("  3. Provide recommendations")
        print()
        input("Press Enter to run...")

        result = await agent.query(
            "Analyze the health of my production environment based on Datadog monitors. "
            "What should I be concerned about?",
            verbose=False
        )
        print(f"\nResult:\n{result}")

        # Example 3: Multi-step investigation
        print_section("Example 3: Multi-Step Investigation")
        print("Ask: 'What's the most critical issue and how can I fix it?'")
        print("Claude will:")
        print("  1. List monitors to find alerts")
        print("  2. Get detailed info on alerting monitors")
        print("  3. Analyze the root cause")
        print("  4. Suggest remediation steps")
        print()
        input("Press Enter to run...")

        result = await agent.query(
            "What is the most critical issue in my Datadog monitoring right now? "
            "Get the details and tell me what I should do to fix it.",
            verbose=False
        )
        print(f"\nResult:\n{result}")

        # Example 4: Future multi-MCP query (demonstrates vision)
        print_section("Example 4: Future Multi-MCP Capability")
        print("In the future, with JIRA and GitHub MCP added, you could ask:")
        print()
        print("  'Create a JIRA ticket for the alerting monitor and")
        print("   open a GitHub issue to track the fix'")
        print()
        print("Claude would:")
        print("  1. Use datadog_get_monitors to find the alert")
        print("  2. Use jira_create_issue to create a ticket")
        print("  3. Use github_create_issue to open an issue")
        print("  4. Link them all together")
        print()
        print("This is the power of autonomous MCP orchestration!")

    print_section("Demo Complete")
    print("Key Takeaways:")
    print("  ✓ Claude autonomously decides which tools to use (via Agent SDK)")
    print("  ✓ Can call multiple tools in sequence")
    print("  ✓ Synthesizes results into human-readable responses")
    print("  ✓ Ready to add more MCP servers (JIRA, GitHub, etc.)")
    print("  ✓ No need to manually specify which tool to call")
    print("  ✓ Built-in features: hooks, subagents, context compaction")
    print()
    print("Next: Add JIRA and GitHub MCP servers to enable full workflow automation!")


if __name__ == "__main__":
    anyio.run(main)
