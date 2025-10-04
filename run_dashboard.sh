#!/bin/bash
# United Airlines Flight Difficulty Dashboard - Easy Activation Script

echo "✈️ United Airlines Flight Difficulty Scoring System"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then run: source venv/bin/activate"
    echo "Then run: pip install -r requirements_fixed.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if packages are installed
echo "🔍 Checking packages..."
python -c "import streamlit, pandas, numpy, plotly, seaborn, matplotlib, sklearn, tensorflow, xgboost, lightgbm; print('✅ All packages ready!')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 System ready! Choose an option:"
    echo "1. 🚀 Launch Interactive Dashboard"
    echo "2. 🔬 Run Comprehensive Analysis"
    echo "3. 🧪 Run System Test"
    echo "4. 📊 View Available Files"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            echo "🚀 Launching Streamlit Dashboard..."
            echo "📱 Dashboard will open at: http://localhost:8501"
            streamlit run flight_difficulty_dashboard.py
            ;;
        2)
            echo "🔬 Running Comprehensive Analysis..."
            python comprehensive_analysis.py
            ;;
        3)
            echo "🧪 Running System Test..."
            python simple_test.py
            ;;
        4)
            echo "📊 Available Files:"
            ls -la *.py *.db *.csv *.txt *.md 2>/dev/null | grep -E "\.(py|db|csv|txt|md)$"
            ;;
        *)
            echo "❌ Invalid choice. Please run the script again."
            ;;
    esac
else
    echo "❌ Some packages are missing!"
    echo "Please install them with: pip install -r requirements_fixed.txt"
fi
