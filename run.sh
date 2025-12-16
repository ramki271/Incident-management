#!/bin/bash
# Helper script to run Python scripts with the correct Python version
# This ensures we use Python 3.11 which has Claude Agent SDK installed

PYTHON_CMD="/opt/homebrew/bin/python3.11"

# Check if Python 3.11 is available
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "Error: Python 3.11 not found at $PYTHON_CMD"
    echo "Install it with: brew install python@3.11"
    exit 1
fi

# Check Python version
VERSION=$($PYTHON_CMD --version)
echo "Using: $VERSION"
echo ""

# Run the provided script
if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh <script.py> [args...]"
    echo ""
    echo "Examples:"
    echo "  ./run.sh examples/test_github_mcp.py"
    echo "  ./run.sh src/autonomous_agent.py"
    exit 1
fi

$PYTHON_CMD "$@"

