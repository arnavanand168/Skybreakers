#!/usr/bin/env python3
"""
Test script for Flask Flight Difficulty Dashboard
Tests all API endpoints and functionality
"""

import requests
import json
import sys
from app import app, analyzer

def test_database():
    """Test database connection and data loading"""
    print("🔄 Testing database connection...")
    
    try:
        data = analyzer.load_flight_data()
        if data is not None:
            print(f"✅ Database connected successfully")
            print(f"📊 Loaded {len(data)} flight records")
            print(f"📈 Data shape: {data.shape}")
            return True
        else:
            print("❌ Failed to load flight data")
            return False
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    base_url = 'http://localhost:5000'
    endpoints = [
        '/api/stats',
        '/api/health',
        '/api/classification-chart',
        '/api/destination-chart',
        '/api/time-chart',
        '/api/destinations',
        '/api/fleet'
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            print(f"🔄 Testing {endpoint}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    print(f"❌ {endpoint}: {data['error']}")
                    results[endpoint] = False
                else:
                    print(f"✅ {endpoint}: Success")
                    results[endpoint] = True
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
                results[endpoint] = False
                
        except Exception as e:
            print(f"❌ {endpoint}: Connection error - {e}")
            results[endpoint] = False
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n📊 API Test Results: {success_count}/{total_count} endpoints working")
    return success_count == total_count

def test_static_files():
    """Test static file serving"""
    print("\n📁 Testing static file serving...")
    
    static_files = [
        '/static/css/style.css',
        '/static/js/dashboard.js'
    ]
    
    base_url = 'http://localhost:5000'
    results = {}
    
    for file_path in static_files:
        try:
            response = requests.get(f"{base_url}{file_path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {file_path}: Available")
                results[file_path] = True
            else:
                print(f"❌ {file_path}: HTTP {response.status_code}")
                results[file_path] = False
        except Exception as e:
            print(f"❌ {file_path}: {e}")
            results[file_path] = False
    
    return all(results.values())

def test_templates():
    """Test template rendering"""
    print("\n🎨 Testing template rendering...")
    
    pages = [
        '/',
        '/about'
    ]
    
    base_url = 'http://localhost:5000'
    results = {}
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}{page}", timeout=5)
            if response.status_code == 200:
                content = response.text
                if '<title>' in content and '<body>' in content:
                    print(f"✅ {page}: Template rendered")
                    results[page] = True
                else:
                    print(f"❌ {page}: Template incomplete")
                    results[page] = False
            else:
                print(f"❌ {page}: HTTP {response.status_code}")
                results[page] = False
        except Exception as e:
            print(f"❌ {page}: {e}")
            results[page] = False
    
    return all(results.values())

def run_server_tests():
    """Run tests with Flask test client"""
    print("\n🧪 Running server-side tests...")
    
    test_client = app.test_client()
    results = {}
    
    # Test main pages
    response = test_client.get('/')
    results['homepage'] = response.status_code == 200
    
    response = test_client.get('/about')
    results['about_page'] = response.status_code == 200
    
    # Test API endpoints
    response = test_client.get('/api/health')
    results['health_api'] = response.status_code == 200
    
    response = test_client.get('/api/stats')
    results['stats_api'] = response.status_code == 200
    
    print("✅ Homepage:", results['homepage'])
    print("✅ About Page:", results['about_page'])
    print("✅ Health API:", results['health_api'])
    print("✅ Stats API:", results['stats_api'])
    
    return all(results.values())

def main():
    """Main test function"""
    print("🚀 United Airlines Flight Difficulty Dashboard - Test Suite")
    print("=" * 60)
    
    # Test database
    db_ok = test_database()
    
    # Test server-side functionality
    server_ok = run_server_tests()
    
    print("\n📋 Test Summary:")
    print(f"Database Connection: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"Server Functionality: {'✅ PASS' if server_ok else '❌ FAIL'}")
    
    if db_ok and server_ok:
        print("\n🎉 All tests passed! The Flask app is ready for deployment.")
        print("\n🚀 Next steps:")
        print("1. Install Flask dependencies: pip install -r requirements_flask.txt")
        print("2. Run the app: python app.py")
        print("3. Open http://localhost:5000 in your browser")
        print("4. Follow DEPLOYMENT_GUIDE.md for cloud deployment")
        return True
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
