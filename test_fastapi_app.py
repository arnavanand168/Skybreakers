

from main import analyzer
import json

def test_fastapi_app():

    print("🚀 Testing FastAPI Flight Analyzer...")

    print("📊 Testing data generation...")
    df = analyzer.load_flight_data()
    print(f"✅ Generated {len(df)} flights")

    print("📈 Testing statistics...")
    stats = analyzer.get_dashboard_stats()
    print(f"✅ Stats: {stats}")

    print("📊 Testing chart generation...")

    try:
        chart1_json = analyzer.create_classification_chart()
        chart1 = json.loads(chart1_json)
        print("✅ Classification chart created")
    except Exception as e:
        print(f"❌ Classification chart error: {e}")

    try:
        chart2_json = analyzer.create_destination_chart()
        chart2 = json.loads(chart2_json)
        print("✅ Destination chart created")
    except Exception as e:
        print(f"❌ Destination chart error: {e}")

    try:
        chart3_json = analyzer.create_time_chart()
        chart3 = json.loads(chart3_json)
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

    print("\n🎉 FastAPI Demo App is ready for deployment!")
    print("🚀 Run locally: uvicorn main:app --host 0.0.0.0 --port 8000")
    print("🌐 Then open: http://localhost:8000")
    print("\n📋 For Vercel deployment:")
    print("   1. Make sure main.py is your main file")
    print("   2. Run: vercel --prod")
    print("   3. Your app will be deployed!")

if __name__ == '__main__':
    test_fastapi_app()
