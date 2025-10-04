#!/bin/bash

# United Airlines Flight Difficulty Dashboard - Web App Launcher
# Launches Flask demo application for local testing and cloud deployment preparation

echo "🛫 United Airlines Flight Difficulty Dashboard"
echo "🚀 Web Application Launcher"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📋 Installing Flask dependencies..."
pip install flask pandas plotly numpy

# Check if app_demo.py exists
if [ ! -f "app_demo.py" ]; then
    echo "❌ app_demo.py not found!"
    echo "Please ensure all Flask files are present."
    exit 1
fi

# Run tests
echo "🧪 Running deployment tests..."
python3 test_demo_app.py

# Launch Flask app
echo ""
echo "🚀 Launching Flask demo application..."
echo "📊 Features:"
echo "   • Real-time dashboard"
echo "   • Interactive charts"
echo "   • Mobile responsive"
echo "   • Ready for cloud deployment"
echo ""
echo "🌐 Dashboard will be available at: http://localhost:5000"
echo "📱 About page: http://localhost:5000/about"
echo "🏥 Health check: http://localhost:5000/api/health"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo "=============================================="

# Start Flask app
python3 app_demo.py
