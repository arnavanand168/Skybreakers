#!/bin/bash
# Database Regeneration Script for United Airlines Flight Difficulty Analysis

echo "🔧 United Airlines Flight Difficulty Analysis - Database Regeneration"
echo "==================================================================="
echo ""

# Check if required CSV files exist
required_files=(
    "Airports Data.csv"
    "Bag+Level+Data.csv"
    "Flight Level Data.csv"
    "PNR+Flight+Level+Data.csv"
    "PNR Remark Level Data.csv"
)

echo "📋 Checking required files..."
missing_files=()
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    echo "❌ Missing required files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "Please ensure all CSV files are present before regenerating the database."
    exit 1
fi

echo ""
echo "🚀 Starting database regeneration..."

# Run the complete analysis to regenerate the database
python3 comprehensive_analysis.py

# Check if database was created successfully
if [ -f "skyhack.db" ]; then
    size=$(du -h skyhack.db | cut -f1)
    echo ""
    echo "✅ Database regenerated successfully!"
    echo "📊 Database size: $size"
    echo "📁 Location: $(pwd)/skyhack.db"
    echo ""
    echo "🎉 You can now run the dashboard:"
    echo "   ./launch_working_dashboard.sh"
else
    echo ""
    echo "❌ Database generation failed!"
    echo "Please check for any errors above and try again."
    exit 1
fi
