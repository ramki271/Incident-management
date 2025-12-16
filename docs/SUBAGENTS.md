# Subagents in Claude Agent SDK

## What are Subagents?

Subagents are specialized agents that can be invoked by a main agent to handle specific tasks. Think of them as expert consultants that the main agent can call upon.

## Why Use Subagents?

### 1. **Separation of Concerns**
Each subagent focuses on one specific domain:
- `monitoring_agent` → Datadog monitoring analysis
- `incident_agent` → Incident management
- `reporting_agent` → Report generation

### 2. **Specialized Instructions**
Each subagent has tailored instructions for its domain, leading to better results.

### 3. **Context Isolation**
Each subagent maintains its own conversation history, preventing context pollution.

### 4. **Reusability**
Define once, use many times across different workflows.

### 5. **Scalability**
Easy to add new specialized agents without modifying existing ones.

## How to Create Subagents

### Basic Pattern

```python
from claude_agent_sdk import SubagentConfig

# Define a specialized subagent
monitoring_agent = SubagentConfig(
    name="monitoring_agent",
    instructions="""You are a Datadog monitoring specialist.
    
Your responsibilities:
- Analyze Datadog monitors
- Identify critical alerts
- Suggest remediation steps

Always be concise and actionable.""",
    mcp_servers=mcp_servers,
    model="claude-sonnet-4-20250514"
)
```

### Using Subagents

#### Option 1: With `query()` function

```python
from claude_agent_sdk import query

async for message in query(
    prompt="Use monitoring_agent to check my alerts",
    mcp_servers=mcp_servers,
    agents={"monitoring_agent": monitoring_agent}
):
    print(message)
```

#### Option 2: With `ClaudeSDKClient`

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

options = ClaudeAgentOptions(
    model="claude-sonnet-4-20250514",
    mcp_servers=mcp_servers,
    agents={
        "monitoring_agent": monitoring_agent,
        "reporting_agent": reporting_agent
    }
)

client = ClaudeSDKClient(options=options)
await client.query("Use monitoring_agent to analyze alerts")
```

## Practical Examples

### Example 1: Single Subagent

```python
# Simple delegation to one subagent
await client.query(
    "Use the monitoring_agent to check what monitors are alerting"
)
```

### Example 2: Multiple Subagents in Sequence

```python
# Main agent orchestrates multiple subagents
await client.query(
    "First, use monitoring_agent to find critical alerts. "
    "Then, use incident_agent to create incidents. "
    "Finally, use reporting_agent to generate a summary."
)
```

### Example 3: Conditional Delegation

```python
# Main agent decides which subagent to use
await client.query(
    "Check my Datadog monitors. If there are critical alerts, "
    "use incident_agent to create incidents. Otherwise, "
    "use reporting_agent to generate a health report."
)
```

## Subagent Design Patterns

### Pattern 1: Domain Specialists
Each subagent is an expert in one domain:
- `datadog_agent` → Datadog operations
- `jira_agent` → JIRA ticket management
- `github_agent` → GitHub operations

### Pattern 2: Task Specialists
Each subagent handles one type of task:
- `analyzer_agent` → Data analysis
- `executor_agent` → Action execution
- `reporter_agent` → Report generation

### Pattern 3: Workflow Stages
Each subagent represents a stage in a workflow:
- `triage_agent` → Initial assessment
- `investigation_agent` → Deep dive analysis
- `resolution_agent` → Fix implementation
- `verification_agent` → Validation

## Best Practices

### 1. Clear Instructions
Give each subagent clear, specific instructions:
```python
instructions="""You are a [ROLE].

Your responsibilities:
- [Task 1]
- [Task 2]
- [Task 3]

Always [guideline]."""
```

### 2. Descriptive Names
Use clear, descriptive names:
- ✅ `datadog_monitoring_specialist`
- ✅ `jira_ticket_creator`
- ❌ `agent1`
- ❌ `helper`

### 3. Single Responsibility
Each subagent should have ONE clear purpose.

### 4. Appropriate Tools
Give each subagent only the MCP servers it needs:
```python
# Monitoring agent only needs Datadog
monitoring_agent = SubagentConfig(
    name="monitoring_agent",
    mcp_servers={"datadog": datadog_config}
)

# Incident agent needs both Datadog and JIRA
incident_agent = SubagentConfig(
    name="incident_agent",
    mcp_servers={
        "datadog": datadog_config,
        "jira": jira_config
    }
)
```

## Running the Examples

### Simple Example
```bash
python examples/simple_subagent.py
```

### Full Incident Manager Example
```bash
python examples/subagent_example.py
```

## Next Steps

1. **Add JIRA MCP Server** - Enable `incident_agent` to create real tickets
2. **Add GitHub MCP Server** - Enable code-related incident tracking
3. **Create More Subagents**:
   - `triage_agent` - Initial incident assessment
   - `escalation_agent` - Handle escalations
   - `postmortem_agent` - Generate incident postmortems

