#!/bin/bash
# Quick start script for Contax Brain.tech Portal

echo "🧠 Contax Brain.tech Portal - Quick Start"
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY before starting the server"
    echo ""
    read -p "Press Enter to continue after configuring your .env file..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python -m pytest test_main.py -v

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo ""
    echo "🚀 Starting server..."
    echo "📍 Access the portal at: http://localhost:8000"
    echo "📍 Health check at: http://localhost:8000/health"
    echo ""
    python main.py
else
    echo ""
    echo "❌ Tests failed. Please check the errors above."
    exit 1
fi
