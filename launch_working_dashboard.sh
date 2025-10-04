#!/bin/bash
# Quick launcher for the ENHANCED working dashboard

echo "✈️ United Airlines Flight Difficulty Dashboard"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Launch the ENHANCED working dashboard
echo "🚀 Launching ENHANCED dashboard..."
echo "📱 Dashboard will open at: http://localhost:8501"
echo "✅ All errors fixed + New 'How It Works' tab added!"
echo "✅ Time analysis graphs now working properly!"
echo ""

streamlit run simple_dashboard.py
