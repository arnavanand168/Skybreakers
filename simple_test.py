

import sqlite3
import csv
import json
import os
from datetime import datetime

def test_database_connection():

    print("🔍 Testing Database Connection...")

    try:
        conn = sqlite3.connect('skyhack.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM ClassifiedFlights")
        count = cursor.fetchone()[0]
        print(f"✅ Database connected successfully! Found {count} flights.")

        cursor.execute(
    print("\n🔍 Testing CSV Export...")

    try:
        conn = sqlite3.connect('skyhack.db')

        query =
    print("\n🔍 Testing Basic Analysis...")

    try:
        conn = sqlite3.connect('skyhack.db')

        cursor = conn.cursor()

        cursor.execute("SELECT AVG(departure_delay_minutes) FROM ClassifiedFlights")
        avg_delay = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(is_delayed) FROM ClassifiedFlights")
        delayed_pct = cursor.fetchone()[0] * 100

        cursor.execute("SELECT AVG(ground_time_pressure) FROM ClassifiedFlights")
        avg_ground_pressure = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(transfer_bag_ratio) FROM ClassifiedFlights WHERE total_bags > 0")
        avg_transfer_ratio = cursor.fetchone()[0]

        print("📈 Basic Analysis Results:")
        print(f"   Average delay: {avg_delay:.2f} minutes")
        print(f"   Delayed flights: {delayed_pct:.2f}%")
        print(f"   Average ground time pressure: {avg_ground_pressure:.2f}")
        print(f"   Average transfer bag ratio: {avg_transfer_ratio:.3f}")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Basic analysis test failed: {e}")
        return False

def test_file_structure():

    print("\n🔍 Testing File Structure...")

    required_files = [
        'skyhack.db',
        'test_arnav.csv',
        'flight_difficulty_dashboard.py',
        'comprehensive_analysis.py',
        'advanced_ml_models.py',
        'reinforcement_learning.py',
        'launcher.py',
        'requirements_advanced.txt',
        'README_Python_Dashboard.md'
    ]

    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file} (Missing)")
            missing_files.append(file)

    if missing_files:
        print(f"\n⚠️ Missing files: {len(missing_files)}")
        return False
    else:
        print(f"\n✅ All {len(required_files)} files present!")
        return True

def generate_simple_report():

    print("\n📝 Generating Simple Report...")

    try:
        conn = sqlite3.connect('skyhack.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM ClassifiedFlights")
        total_flights = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(departure_delay_minutes) FROM ClassifiedFlights")
        avg_delay = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(is_delayed) FROM ClassifiedFlights")
        delayed_pct = cursor.fetchone()[0] * 100

        cursor.execute(
    print("🚀 United Airlines Flight Difficulty Analysis - System Test")
    print("=" * 60)

    tests = [
        ("Database Connection", test_database_connection),
        ("File Structure", test_file_structure),
        ("Basic Analysis", test_basic_analysis),
        ("Simple Report Generation", generate_simple_report)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")

    print(f"\n{'='*60}")
    print(f"🎯 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
        print("\n📋 Next Steps:")
        print("1. Install Python dependencies: pip install -r requirements_advanced.txt")
        print("2. Launch dashboard: python3 launcher.py")
        print("3. Run comprehensive analysis: python3 comprehensive_analysis.py")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")

    print(f"\n📁 Generated Files:")
    if os.path.exists('test_sample_export.csv'):
        print("• test_sample_export.csv")
    if os.path.exists('simple_analysis_report.txt'):
        print("• simple_analysis_report.txt")

if __name__ == "__main__":
    main()
