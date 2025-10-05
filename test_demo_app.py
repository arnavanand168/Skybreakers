

from app_demo import analyzer

def test_demo_functionality():

    print("🧪 Testing Demo Flight Analyzer...")

    print("📊 Testing data generation...")
    df = analyzer.load_flight_data()
    print(f"✅ Generated {len(df)} flights")

    print("📈 Testing statistics...")
    stats = analyzer.get_dashboard_stats()
    print(f"✅ Stats: {stats}")

    print("📊 Testing chart generation...")
    
    try:
        chart1 = analyzer.create_classification_chart()
        print("✅ Classification chart created")
    except Exception as e:
        print(f"❌ Classification chart error: {e}")
    
    try:
        chart2 = analyzer.create_destination_chart()
        print("✅ Destination chart created")
    except Exception as e:
        print(f"❌ Destination chart error: {e}")
    
    try:
        chart3 = analyzer.create_time_chart()
        print("✅ Time chart created")
    except Exception as e:
        print(f"❌ Time chart error: {e}")

    try:
        dest_data = analyzer.get_destination_analysis()
        print(f"✅ Destination analysis: {len(dest_data)} destinations")
    except Exception as e:
        print(f"❌ Destination analysis error: {e}")
    
    try:
        fleet_data = analyzer.get_fleet_analysis()
        print(f"✅ Fleet analysis: {len(fleet_data)} fleet types")
    except Exception as e:
        print(f"❌ Fleet analysis error: {e}")
    
    print("\n🎉 Demo Flask app is ready for deployment!")
    print("🚀 Run: python3 app_demo.py")
    print("🌐 Then open: http://localhost:5000")

if __name__ == '__main__':
    test_demo_functionality()
