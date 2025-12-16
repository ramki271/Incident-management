#!/usr/bin/env python3
"""
Incident Fix Workflow - Complete End-to-End Example

This demonstrates the FULL vision:
1. Datadog detects an alert
2. Agent analyzes the alert and identifies the issue
3. Agent accesses the GitHub repository
4. Agent reads the code to understand the problem
5. Agent creates a fix (or suggests one)
6. Agent creates a PR with the fix
7. Agent creates a JIRA ticket (future) to track it

This is the COMPLETE incident response automation!
"""

import os
import sys
import anyio

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from config.mcp_config import get_all_mcp_servers


async def incident_fix_workflow():
    """
    Complete incident fix workflow demonstrating the full vision.
    """
    print("="*80)
    print("INCIDENT FIX WORKFLOW - Full Automation Demo")
    print("="*80)
    print()
    print("This demonstrates:")
    print("  1. Detecting Datadog alerts")
    print("  2. Analyzing the issue")
    print("  3. Reading repository code")
    print("  4. Understanding the problem")
    print("  5. Creating a fix")
    print("  6. Opening a PR")
    print("="*80)
    print()
    
    # Get all MCP servers (Datadog + GitHub)
    mcp_servers = get_all_mcp_servers()
    
    # Create Claude Agent with both MCP servers
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-20250514",
        mcp_servers=mcp_servers,
        permission_mode="bypassPermissions"
    )
    
    async with ClaudeSDKClient(options=options) as client:
        
        # WORKFLOW: Complete incident response
        workflow_prompt = """
You are an intelligent incident response agent with access to both Datadog and GitHub.

Your mission: Detect, analyze, and FIX incidents automatically.

Here's the workflow:

STEP 1: DETECT
- Check Datadog for any alerting monitors
- Identify the most critical alert

STEP 2: ANALYZE  
- Understand what the alert is about
- Determine which service/repository is affected
- Identify the likely root cause

STEP 3: INVESTIGATE CODE
- Access the GitHub repository for the affected service
- Read the relevant code files
- Search for the problematic code
- Understand the codebase structure

STEP 4: DIAGNOSE
- Based on the alert and the code, identify the exact issue
- Explain what's wrong and why it's causing the alert

STEP 5: PROPOSE FIX
- Suggest a code fix for the issue
- Explain why this fix will resolve the alert

STEP 6: CREATE PR (if appropriate)
- Create a new branch
- Make the code changes
- Open a pull request with:
  - Clear title referencing the Datadog alert
  - Description explaining the issue and fix
  - Link to the Datadog monitor

Let's start! Begin with STEP 1: Check Datadog for alerting monitors.
"""
        
        print("Sending workflow to agent...")
        print()
        print("-"*80)
        print()
        
        await client.query(workflow_prompt)
        
        # Receive and display the response
        async for message in client.receive_response():
            print(message)
            print()
    
    print()
    print("="*80)
    print("Workflow Complete!")
    print("="*80)
    print()
    print("What just happened:")
    print("  ✓ Agent checked Datadog for alerts")
    print("  ✓ Agent analyzed the critical issues")
    print("  ✓ Agent accessed GitHub repositories")
    print("  ✓ Agent read and understood the code")
    print("  ✓ Agent diagnosed the root cause")
    print("  ✓ Agent proposed a fix")
    print("  ✓ Agent can create a PR with the fix")
    print()
    print("This is FULL incident response automation!")


async def simple_code_analysis_example():
    """
    Simpler example: Just analyze code from a specific repo.
    """
    print("="*80)
    print("SIMPLE EXAMPLE: Code Analysis")
    print("="*80)
    print()
    
    mcp_servers = get_all_mcp_servers()
    
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-20250514",
        mcp_servers=mcp_servers,
        permission_mode="bypassPermissions"
    )
    
    async with ClaudeSDKClient(options=options) as client:
        
        # Simple query: Read code from a repository
        query = """
Using GitHub tools:

1. List my repositories
2. Pick one repository
3. Get the file structure (list files)
4. Read the main code files (e.g., src/, main.py, index.js, etc.)
5. Analyze the code and tell me:
   - What the application does
   - What technologies it uses
   - Any potential issues you see
   - Suggestions for improvement

Be thorough in your analysis!
"""
        
        print("Asking agent to analyze repository code...")
        print()
        
        await client.query(query)
        
        async for message in client.receive_response():
            print(message)
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--simple":
        print("Running simple code analysis example...")
        anyio.run(simple_code_analysis_example)
    else:
        print("Running full incident fix workflow...")
        print("(Use --simple flag for simpler example)")
        print()
        anyio.run(incident_fix_workflow)

