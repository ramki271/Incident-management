# Subagents Quick Start

## TL;DR

Subagents let you create specialized AI agents that the main agent can delegate tasks to.

```python
from claude_agent_sdk import query, SubagentConfig

# 1. Define a specialized subagent
specialist = SubagentConfig(
    name="datadog_expert",
    instructions="You are a Datadog monitoring expert. Analyze monitors and alerts.",
    mcp_servers=mcp_servers,
    model="claude-sonnet-4-20250514"
)

# 2. Use it
async for message in query(
    prompt="Use datadog_expert to check my alerts",
    mcp_servers=mcp_servers,
    agents={"datadog_expert": specialist}
):
    print(message)
```

## When to Use Subagents

### ✅ Use Subagents When:
- You have **distinct domains** (Datadog, JIRA, GitHub)
- You need **specialized expertise** (monitoring vs. incident management)
- You want **reusable components** (same agent, different workflows)
- You have **complex workflows** (multi-stage processes)

### ❌ Don't Use Subagents When:
- You have a simple, single-step task
- All tasks use the same tools and context
- You're just starting out (use simple agent first)

## Real-World Example: Incident Management

```python
# Define specialized subagents
monitoring_agent = SubagentConfig(
    name="monitoring_agent",
    instructions="Analyze Datadog monitors. Identify critical alerts.",
    mcp_servers={"datadog": datadog_config}
)

incident_agent = SubagentConfig(
    name="incident_agent",
    instructions="Create and manage incidents. Link to monitoring data.",
    mcp_servers={"datadog": datadog_config, "jira": jira_config}
)

reporting_agent = SubagentConfig(
    name="reporting_agent",
    instructions="Generate executive reports. Summarize incidents.",
    mcp_servers={"datadog": datadog_config}
)

# Use them together
async with AutonomousAgent() as agent:
    result = await agent.query(
        "1. Use monitoring_agent to find critical alerts\n"
        "2. Use incident_agent to create JIRA tickets\n"
        "3. Use reporting_agent to generate a summary"
    )
```

## Key Benefits

### 1. **Separation of Concerns**
```
monitoring_agent → Only monitors
incident_agent   → Only incidents
reporting_agent  → Only reports
```

### 2. **Better Results**
Each agent has specialized instructions = better performance

### 3. **Easier Debugging**
Problem with incident creation? Check `incident_agent` only.

### 4. **Scalability**
Add new agents without touching existing ones:
```python
# Add a new agent
escalation_agent = SubagentConfig(
    name="escalation_agent",
    instructions="Handle incident escalations to on-call engineers.",
    mcp_servers={"pagerduty": pagerduty_config}
)
```

## Common Patterns

### Pattern 1: Sequential Workflow
```python
"First use agent_a, then agent_b, finally agent_c"
```

### Pattern 2: Conditional Delegation
```python
"If critical alerts exist, use incident_agent. Otherwise, use reporting_agent."
```

### Pattern 3: Parallel Analysis
```python
"Use monitoring_agent to check Datadog and use logs_agent to check logs. Compare results."
```

## Examples in This Project

1. **Simple Example**: `examples/simple_subagent.py`
   - Basic subagent usage
   - Single delegation

2. **Full Example**: `examples/subagent_example.py`
   - Multiple subagents
   - Complex workflows
   - Real incident management

3. **Documentation**: `docs/SUBAGENTS.md`
   - Complete guide
   - Best practices
   - Design patterns

## Next Steps

1. **Run the simple example**:
   ```bash
   python examples/simple_subagent.py
   ```

2. **Read the full docs**:
   ```bash
   cat docs/SUBAGENTS.md
   ```

3. **Try the full example**:
   ```bash
   python examples/subagent_example.py
   ```

4. **Create your own subagent**:
   - Identify a specialized task
   - Write clear instructions
   - Test it!

## FAQ

**Q: Can subagents call other subagents?**
A: Yes! Subagents can delegate to other subagents.

**Q: How many subagents can I have?**
A: As many as you need, but keep it manageable (3-5 is typical).

**Q: Do subagents share context?**
A: No, each has its own conversation history (that's a feature!).

**Q: Can I use different models for different subagents?**
A: Yes! Specify `model` in `SubagentConfig`.

**Q: Do I need subagents for my use case?**
A: Start simple. Add subagents when you need specialization.

