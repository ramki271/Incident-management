# Python Version Issue - Resolved

## The Problem

You have **two Python installations** on your system:

1. **System Python 3.9.6** at `/usr/bin/python3`
   - ❌ Too old for Claude Agent SDK (requires Python 3.10+)
   - ❌ Claude Agent SDK NOT installed

2. **Homebrew Python 3.11** at `/opt/homebrew/bin/python3.11`
   - ✅ Meets requirements (Python 3.10+)
   - ✅ Claude Agent SDK installed (v0.1.16)

## Why This Caused Confusion

When running `python3 <script>`, it uses the **system Python 3.9**, which doesn't have the Claude Agent SDK installed.

This is why the test initially failed with:
```
ModuleNotFoundError: No module named 'claude_agent_sdk'
```

## The Solution

### Option 1: Use the Helper Script (Recommended)

```bash
./run.sh examples/test_github_mcp.py
./run.sh src/autonomous_agent.py
```

The `run.sh` script automatically uses Python 3.11.

### Option 2: Use Python 3.11 Directly

```bash
/opt/homebrew/bin/python3.11 examples/test_github_mcp.py
```

### Option 3: Create an Alias (Permanent Fix)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias python3="/opt/homebrew/bin/python3.11"
alias pip3="/opt/homebrew/bin/python3.11 -m pip"
```

Then reload:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Option 4: Use a Virtual Environment (Best Practice)

```bash
# Create virtual environment with Python 3.11
/opt/homebrew/bin/python3.11 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Now you can use python3 normally
python3 examples/test_github_mcp.py
```

## Verification

Check which Python you're using:

```bash
which python3
python3 --version
python3 -c "import claude_agent_sdk; print('SDK installed!')"
```

Expected output:
```
/opt/homebrew/bin/python3.11  # or your venv path
Python 3.11.x
SDK installed!
```

## Why We Didn't Notice Earlier

The existing code in `src/autonomous_agent.py` was probably being run with Python 3.11 already (either manually or through an IDE that detected the correct version).

The issue only surfaced when creating the new test script and running it with the default `python3` command.

## Summary

✅ **Problem Identified**: Multiple Python versions, wrong one being used by default
✅ **Solution Provided**: Helper script (`run.sh`) to use correct Python
✅ **Verified Working**: GitHub MCP Server test passed with Python 3.11
✅ **Documentation Updated**: README now mentions Python version requirement

## Next Steps

Choose one of the solutions above and stick with it for consistency. I recommend either:
- Using the `run.sh` helper script, OR
- Creating a virtual environment (best practice for Python projects)

