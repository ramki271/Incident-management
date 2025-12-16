#!/bin/bash

# Setup script for Datadog Incident Manager

set -e

echo "=========================================="
echo "Datadog Incident Manager - Setup"
echo "=========================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check for Node.js
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed"
    echo "Please install Node.js and npm"
    exit 1
fi

echo "✓ npm found: $(npm --version)"

# Check if datadog-mcp-server is installed
if ! command -v datadog-mcp-server &> /dev/null; then
    echo ""
    echo "Installing datadog-mcp-server globally..."
    npm install -g datadog-mcp-server
    echo "✓ datadog-mcp-server installed"
else
    echo "✓ datadog-mcp-server already installed"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo ""
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Python dependencies installed"

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Warning: .env file not found"
    echo "Please create a .env file with your credentials:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your actual API keys"
else
    echo "✓ .env file found"

    # Validate .env has real credentials
    if grep -q "your_datadog_api_key_here" .env || grep -q "your_datadog_application_key_here" .env; then
        echo "⚠️  Warning: .env file still has placeholder values"
        echo "Please update .env with your actual Datadog API keys"
    else
        echo "✓ .env file appears to be configured"
    fi
fi

# Check for ANTHROPIC_API_KEY
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  Warning: ANTHROPIC_API_KEY not found in environment"
    echo "You'll need to set this to use the Agent SDK:"
    echo "  export ANTHROPIC_API_KEY='your_key_here'"
    echo "  # Or add it to your .env file"
else
    echo "✓ ANTHROPIC_API_KEY is set"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Ensure your .env file has valid credentials"
echo ""
echo "3. Test the configuration:"
echo "   python config/mcp_config.py"
echo ""
echo "4. Run examples:"
echo "   python examples/basic_usage.py"
echo ""
echo "5. Or use the agent directly:"
echo "   python src/datadog_agent.py"
echo ""
