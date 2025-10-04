# Installation & Setup Guide
## United Airlines Flight Difficulty Scoring System

### 🚀 Quick Start (5 minutes)

#### Step 1: Verify Files
Ensure you have all required files in your directory:
```bash
ls -la *.py *.db *.csv *.txt *.md
```

#### Step 2: Test System
Run the system test to verify everything works:
```bash
python3 simple_test.py
```

#### Step 3: Install Dependencies (Optional)
If you want to use the full dashboard with ML/RL features:
```bash
pip install -r requirements_advanced.txt
```

#### Step 4: Launch Dashboard
```bash
python3 launcher.py
```

### 📋 System Requirements

#### Minimum Requirements:
- **Python 3.8+** (tested with Python 3.13.3)
- **SQLite3** (included with Python)
- **8GB RAM** (for full ML/RL features)
- **2GB disk space** (for database and models)

#### Optional Requirements (for full features):
- **Streamlit** (interactive dashboard)
- **TensorFlow** (deep learning)
- **XGBoost/LightGBM** (advanced ML)
- **Plotly** (interactive visualizations)

### 🔧 Troubleshooting

#### Common Issues:

**1. Database Connection Error**
```bash
# Check if database exists
ls -la skyhack.db

# Test database connection
python3 -c "import sqlite3; conn = sqlite3.connect('skyhack.db'); print('✅ Database OK')"
```

**2. Missing Dependencies**
```bash
# Install basic requirements
pip install pandas numpy matplotlib seaborn

# Install advanced requirements
pip install -r requirements_advanced.txt
```

**3. Permission Errors**
```bash
# Make scripts executable
chmod +x *.py

# Run with proper permissions
python3 simple_test.py
```

### 📊 Available Features

#### Without External Dependencies:
- ✅ Database analysis and queries
- ✅ Basic statistical analysis
- ✅ CSV export functionality
- ✅ Simple report generation
- ✅ Flight classification analysis

#### With Full Dependencies:
- ✅ Interactive Streamlit dashboard
- ✅ Advanced ML models (XGBoost, LightGBM)
- ✅ Deep learning neural networks
- ✅ Reinforcement learning agents
- ✅ Real-time monitoring
- ✅ Interactive visualizations

### 🎯 Usage Examples

#### Basic Analysis:
```bash
python3 simple_test.py
```

#### Full Dashboard:
```bash
python3 launcher.py
# Choose option 1 for dashboard
```

#### Comprehensive Analysis:
```bash
python3 comprehensive_analysis.py
```

### 📈 Expected Outputs

#### Generated Files:
- `simple_analysis_report.txt` - Basic analysis report
- `test_sample_export.csv` - Sample data export
- `comprehensive_analysis.png` - Visualization suite
- `models/` - Trained ML models (if dependencies installed)

#### Dashboard Features:
- Interactive flight analysis
- Real-time difficulty scoring
- ML model performance comparison
- RL agent training visualization
- Business insights and recommendations

### 🆘 Support

#### If You Need Help:
1. **Check the logs** - Error messages provide specific guidance
2. **Run the test script** - `python3 simple_test.py` diagnoses issues
3. **Verify file structure** - Ensure all files are present
4. **Check Python version** - Requires Python 3.8+

#### Common Solutions:
- **Import errors**: Install missing packages with pip
- **Database errors**: Ensure skyhack.db is in the same directory
- **Permission errors**: Run with proper user permissions
- **Memory errors**: Close other applications or use smaller datasets

### 🎉 Success Indicators

#### System Working Correctly:
- ✅ Test script shows "All tests passed!"
- ✅ Database connection successful
- ✅ All files present and accessible
- ✅ Report generated successfully

#### Dashboard Working Correctly:
- ✅ Dashboard opens in browser
- ✅ Data loads without errors
- ✅ Visualizations display properly
- ✅ Navigation works smoothly

---

*Ready to optimize United Airlines flight operations with advanced analytics!*
