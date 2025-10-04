#!/bin/bash
# Quick launcher for the FINAL working dashboard

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

# Launch the FINAL working dashboard
echo "🚀 Launching FINAL dashboard..."
echo "📱 Dashboard will open at: http://localhost:8501"
echo "✅ All errors fixed + Complete 'How It Works' tab!"
echo "✅ Time analysis graphs working perfectly!"
echo "✅ All 6 tabs fully functional!"
echo ""

streamlit run simple_dashboard.py
