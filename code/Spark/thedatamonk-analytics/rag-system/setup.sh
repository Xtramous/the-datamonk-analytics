#!/bin/bash

# RAG System Setup Script

set -e

echo "🚀 Setting up RAG System..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo "   Get it from: https://console.anthropic.com/account/keys"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your ANTHROPIC_API_KEY"
echo "2. Run: python -m src.cli.main demo"
echo "3. Query: python -m src.cli.main query \"What is Spark?\""
echo ""
echo "For more help, see README.md"
