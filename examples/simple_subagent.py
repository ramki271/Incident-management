#!/usr/bin/env python3
"""
Simple Subagent Example

This shows the basic pattern for using subagents with the Claude Agent SDK.
A subagent is just a specialized agent with specific instructions and tools.
"""

import os
import sys
import anyio

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from claude_agent_sdk import query, SubagentConfig
from config.mcp_config import get_all_mcp_servers


async def main():
    """Simple subagent demonstration."""
    print("="*70)
    print("Simple Subagent Example")
    print("="*70)
    print()
    
    # Get MCP servers
    mcp_servers = get_all_mcp_servers()
    
    # Define a specialized subagent for monitoring
    monitoring_subagent = SubagentConfig(
        name="datadog_monitor_specialist",
        instructions="""You are a Datadog monitoring expert.
        
Your job is to:
1. Analyze Datadog monitors
2. Identify critical alerts
3. Explain what's wrong in simple terms
4. Suggest fixes

Always be concise and actionable.""",
        mcp_servers=mcp_servers,
        model="claude-sonnet-4-20250514"
    )
    
    # Define a specialized subagent for reporting
    reporting_subagent = SubagentConfig(
        name="report_generator",
        instructions="""You are a technical report writer.

Your job is to:
1. Take technical data and make it readable
2. Create executive summaries
3. Highlight key metrics
4. Format reports clearly

Always structure reports with:
- Summary (2-3 sentences)
- Key Findings (bullet points)
- Recommendations (actionable items)""",
        mcp_servers=mcp_servers,
        model="claude-sonnet-4-20250514"
    )
    
    # Example 1: Use the monitoring subagent
    print("\n" + "-"*70)
    print("Example 1: Delegating to monitoring subagent")
    print("-"*70)
    print("\nAsking the main agent to use the monitoring subagent...")
    print()
    
    response_text = ""
    async for message in query(
        prompt="Use the datadog_monitor_specialist subagent to check my Datadog monitors. "
               "What's the current state?",
        mcp_servers=mcp_servers,
        agents={
            "datadog_monitor_specialist": monitoring_subagent,
            "report_generator": reporting_subagent
        }
    ):
        print(message)
        if hasattr(message, 'content'):
            for block in message.content:
                if hasattr(block, 'text'):
                    response_text += block.text
    
    print(f"\n\nFinal Response:\n{response_text}")
    
    # Example 2: Use the reporting subagent
    print("\n\n" + "-"*70)
    print("Example 2: Delegating to reporting subagent")
    print("-"*70)
    print("\nAsking the main agent to use the reporting subagent...")
    print()
    
    response_text = ""
    async for message in query(
        prompt="First, use datadog_monitor_specialist to get monitor data. "
               "Then use report_generator to create an executive summary report.",
        mcp_servers=mcp_servers,
        agents={
            "datadog_monitor_specialist": monitoring_subagent,
            "report_generator": reporting_subagent
        }
    ):
        print(message)
        if hasattr(message, 'content'):
            for block in message.content:
                if hasattr(block, 'text'):
                    response_text += block.text
    
    print(f"\n\nFinal Response:\n{response_text}")
    
    print("\n" + "="*70)
    print("Demo Complete!")
    print("="*70)
    print("\nHow Subagents Work:")
    print("  1. You define subagents with specialized instructions")
    print("  2. You pass them to the main agent via the 'agents' parameter")
    print("  3. The main agent can delegate tasks to subagents")
    print("  4. Each subagent has its own context and expertise")
    print()
    print("Benefits:")
    print("  ✓ Separation of concerns (each agent has one job)")
    print("  ✓ Reusable agents (define once, use many times)")
    print("  ✓ Better results (specialized instructions)")
    print("  ✓ Easier debugging (isolated contexts)")


if __name__ == "__main__":
    anyio.run(main)

