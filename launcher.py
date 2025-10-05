

import subprocess
import sys
import os

def check_requirements():

    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly',
        'seaborn', 'matplotlib', 'scikit-learn', 'tensorflow'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements_advanced.txt")
        return False

    return True

def check_database():

    if not os.path.exists("skyhack.db"):
        print("❌ Database file 'skyhack.db' not found!")
        print("   Please ensure the database file is in the current directory.")
        return False
    return True

def launch_dashboard():

    print("🚀 Launching United Airlines Flight Difficulty Dashboard...")
    print("=" * 60)

    if not check_requirements():
        return False

    if not check_database():
        return False

    print("✅ All requirements satisfied!")
    print("🌐 Dashboard will open in your default browser...")
    print("📊 Navigate through different sections using the sidebar")
    print("🔄 Refresh the page if needed")
    print("\n" + "=" * 60)

    try:

        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "flight_difficulty_dashboard.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard closed by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return False

    return True

def run_analysis():

    print("🔬 Running Comprehensive Analysis...")
    print("=" * 60)

    try:
        subprocess.run([sys.executable, "comprehensive_analysis.py"])
    except KeyboardInterrupt:
        print("\n👋 Analysis stopped by user")
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False

    return True

def main():

    print("✈️ United Airlines Flight Difficulty Scoring System")
    print("Advanced Analytics Dashboard with ML, Deep Learning & RL")
    print("=" * 60)

    while True:
        print("\n📋 Choose an option:")
        print("1. 🚀 Launch Interactive Dashboard")
        print("2. 🔬 Run Comprehensive Analysis")
        print("3. 📊 View Available Files")
        print("4. ❓ Help & Documentation")
        print("5. 🚪 Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            launch_dashboard()
        elif choice == "2":
            run_analysis()
        elif choice == "3":
            show_files()
        elif choice == "4":
            show_help()
        elif choice == "5":
            print("👋 Thank you for using the Flight Difficulty Dashboard!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

def show_files():

    print("\n📁 Available Files:")
    print("-" * 30)

    files = [
        ("skyhack.db", "SQLite database with flight data"),
        ("test_arnav.csv", "Original flight difficulty results"),
        ("flight_difficulty_dashboard.py", "Main Streamlit dashboard"),
        ("comprehensive_analysis.py", "Complete analysis script"),
        ("advanced_ml_models.py", "Advanced ML models"),
        ("reinforcement_learning.py", "RL agents"),
        ("requirements_advanced.txt", "Python dependencies"),
        ("README_Python_Dashboard.md", "Documentation")
    ]

    for filename, description in files:
        if os.path.exists(filename):
            print(f"✅ {filename:<30} - {description}")
        else:
            print(f"❌ {filename:<30} - {description} (Missing)")

def show_help():

    print("\n❓ Help & Documentation")
    print("=" * 40)
    print("\n📊 Dashboard Features:")
    print("• EDA Dashboard: Exploratory data analysis")
    print("• Machine Learning: Model training and comparison")
    print("• Deep Learning: Neural network visualization")
    print("• Reinforcement Learning: RL agent training")
    print("• Real-Time Monitoring: Live flight status")

    print("\n🔬 Analysis Features:")
    print("• Advanced feature engineering")
    print("• Multiple ML model training")
    print("• RL agent optimization")
    print("• Comprehensive visualizations")
    print("• Business insights generation")

    print("\n📋 Requirements:")
    print("• Python 3.8+")
    print("• All packages from requirements_advanced.txt")
    print("• skyhack.db database file")

    print("\n🚀 Quick Start:")
    print("1. Install dependencies: pip install -r requirements_advanced.txt")
    print("2. Launch dashboard: python launcher.py (option 1)")
    print("3. Run analysis: python launcher.py (option 2)")

    print("\n📞 Support:")
    print("• Check README_Python_Dashboard.md for detailed documentation")
    print("• All code includes comprehensive comments")
    print("• Error handling and logging included")

if __name__ == "__main__":
    main()
