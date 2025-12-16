#!/usr/bin/env python3
"""
Subagent Example - Incident Management with Specialized Agents

This demonstrates how to use subagents in the Claude Agent SDK.
Each subagent is specialized for a specific task:
- MonitoringAgent: Analyzes Datadog monitors and alerts
- IncidentAgent: Manages incident creation and tracking
- ReportingAgent: Generates reports and summaries

The main agent orchestrates these subagents to handle complex workflows.
"""

import os
import sys
import anyio
from typing import Dict, Any, List

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, SubagentConfig
from config.mcp_config import get_all_mcp_servers


class IncidentManagerWithSubagents:
    """
    Main incident manager that uses specialized subagents.
    
    Subagents:
    - monitoring_agent: Specialized in analyzing Datadog monitors
    - incident_agent: Specialized in incident management (future: JIRA integration)
    - reporting_agent: Specialized in generating reports
    """
    
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        """Initialize the incident manager with subagents."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.model = model
        mcp_servers = get_all_mcp_servers()
        
        # Define subagents with specialized instructions
        self.subagents = self._create_subagents(mcp_servers)
        
        # Create main agent with subagents
        self.options = ClaudeAgentOptions(
            model=model,
            mcp_servers=mcp_servers,
            agents=self.subagents,  # Register subagents
            permission_mode="bypassPermissions"
        )
        
        self.client = None
        
        print(f"IncidentManager initialized with {len(self.subagents)} subagents")
        print(f"Subagents: {list(self.subagents.keys())}")
    
    def _create_subagents(self, mcp_servers: Dict[str, Any]) -> Dict[str, SubagentConfig]:
        """
        Create specialized subagents for different tasks.
        
        Returns:
            Dictionary of subagent configurations
        """
        return {
            "monitoring_agent": SubagentConfig(
                name="monitoring_agent",
                instructions="""You are a Datadog monitoring specialist.
                
Your responsibilities:
- Analyze Datadog monitors and their states
- Identify critical alerts and their root causes
- Provide detailed analysis of monitoring data
- Suggest remediation steps for alerts

When analyzing monitors:
1. Check current state (OK, Alert, Warn, No Data)
2. Look at monitor metadata (tags, priority, type)
3. Identify patterns in alerting monitors
4. Prioritize by severity and impact

Always provide actionable insights.""",
                mcp_servers=mcp_servers,
                model=self.model
            ),
            
            "incident_agent": SubagentConfig(
                name="incident_agent",
                instructions="""You are an incident management specialist.

Your responsibilities:
- Create and track incidents
- Coordinate incident response
- Link incidents to monitoring alerts
- Manage incident lifecycle (create, update, resolve)

When managing incidents:
1. Gather all relevant context from monitoring
2. Create clear, actionable incident descriptions
3. Set appropriate priority and severity
4. Track incident status and updates

Future: You will integrate with JIRA for ticket creation.""",
                mcp_servers=mcp_servers,
                model=self.model
            ),
            
            "reporting_agent": SubagentConfig(
                name="reporting_agent",
                instructions="""You are a reporting and analytics specialist.

Your responsibilities:
- Generate incident reports
- Analyze trends in monitoring and incidents
- Create executive summaries
- Provide metrics and KPIs

When creating reports:
1. Summarize key findings clearly
2. Use data to support conclusions
3. Highlight critical issues first
4. Provide actionable recommendations
5. Format output for easy reading

Always structure reports with:
- Executive Summary
- Key Metrics
- Critical Issues
- Recommendations""",
                mcp_servers=mcp_servers,
                model=self.model
            )
        }
    
    async def start(self):
        """Start the main agent and all subagents."""
        self.client = ClaudeSDKClient(options=self.options)
        await self.client.__aenter__()
        print("IncidentManager and subagents started")
    
    async def stop(self):
        """Stop the main agent and all subagents."""
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None
        print("IncidentManager and subagents stopped")
    
    async def query(self, prompt: str, verbose: bool = True) -> str:
        """
        Send a query to the main agent.
        
        The main agent will automatically delegate to subagents as needed.
        """
        if not self.client:
            raise RuntimeError("Client not started. Call start() first.")
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"Main Agent Query: {prompt}")
            print(f"{'='*70}\n")
        
        await self.client.query(prompt)
        
        response_text = ""
        async for message in self.client.receive_response():
            if verbose:
                print(message)
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        response_text += block.text
        
        return response_text

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()
        return False


async def main():
    """Demonstrate subagent usage for incident management."""
    print("="*70)
    print("Incident Manager with Subagents - Demo")
    print("="*70)
    print()
    print("This demo shows how the main agent delegates to specialized subagents:")
    print("  - monitoring_agent: Analyzes Datadog monitors")
    print("  - incident_agent: Manages incidents")
    print("  - reporting_agent: Generates reports")
    print()

    try:
        async with IncidentManagerWithSubagents() as manager:

            # Example 1: Main agent delegates to monitoring_agent
            print("\n" + "="*70)
            print("Example 1: Monitoring Analysis (delegates to monitoring_agent)")
            print("="*70)
            print("\nQuery: 'Analyze my Datadog monitors and tell me what's critical'")
            print("\nThe main agent will delegate this to the monitoring_agent subagent...")
            print()
            input("Press Enter to run...")

            result = await manager.query(
                "Use the monitoring_agent to analyze my Datadog monitors. "
                "What monitors are in alert state and what should I prioritize?",
                verbose=True
            )

            # Example 2: Main agent delegates to reporting_agent
            print("\n" + "="*70)
            print("Example 2: Generate Report (delegates to reporting_agent)")
            print("="*70)
            print("\nQuery: 'Generate a monitoring health report'")
            print("\nThe main agent will delegate this to the reporting_agent subagent...")
            print()
            input("Press Enter to run...")

            result = await manager.query(
                "Use the reporting_agent to generate a comprehensive monitoring health report. "
                "Include current state, critical issues, and recommendations.",
                verbose=True
            )

            # Example 3: Complex workflow using multiple subagents
            print("\n" + "="*70)
            print("Example 3: Complex Workflow (multiple subagents)")
            print("="*70)
            print("\nQuery: 'Analyze alerts, create incidents, and generate a report'")
            print("\nThe main agent will orchestrate multiple subagents:")
            print("  1. monitoring_agent: Find critical alerts")
            print("  2. incident_agent: Create incidents for critical issues")
            print("  3. reporting_agent: Generate summary report")
            print()
            input("Press Enter to run...")

            result = await manager.query(
                "Coordinate a full incident response workflow:\n"
                "1. Use monitoring_agent to find critical Datadog alerts\n"
                "2. Use incident_agent to plan incident creation for critical issues\n"
                "3. Use reporting_agent to generate an executive summary\n"
                "Provide a complete incident response plan.",
                verbose=True
            )

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
    print("Demo Complete!")
    print("="*70)
    print("\nKey Takeaways:")
    print("  ✓ Subagents are specialized for specific tasks")
    print("  ✓ Main agent delegates to appropriate subagents")
    print("  ✓ Each subagent has its own instructions and context")
    print("  ✓ Subagents can be reused across multiple queries")
    print("  ✓ Complex workflows can orchestrate multiple subagents")
    print()
    print("Next Steps:")
    print("  - Add JIRA MCP server for incident_agent to create real tickets")
    print("  - Add GitHub MCP server for code-related incident tracking")
    print("  - Create more specialized subagents (e.g., triage_agent, escalation_agent)")


if __name__ == "__main__":
    anyio.run(main)

