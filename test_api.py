"""
Test API with real messy file
"""

import requests
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000/api/v1"

# Test file
test_file = Path("data/synthetic/messy/messy_001_titanic_v0.csv")

if not test_file.exists():
    print(f"❌ Test file not found: {test_file}")
    exit(1)

print("=" * 60)
print("TESTING DATACLEAN.AI API")
print("=" * 60)

# Test 1: Health check
print("\n1️⃣ Testing health endpoint...")
response = requests.get(f"{API_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Analyze file
print("\n2️⃣ Testing analyze endpoint...")
with open(test_file, 'rb') as f:
    files = {'file': (test_file.name, f, 'text/csv')}
    response = requests.post(f"{API_URL}/analyze", files=files)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Analysis successful!")
    print(f"   File: {data['filename']}")
    print(f"   Rows: {data['file_info']['rows']}")
    print(f"   Columns: {data['file_info']['columns']}")
    print(f"   Problems found: {data['summary']['total_problems']}")
    print(f"   Recommendations: {data['summary']['recommended_operations']}")
    
    if data['problems_detected']:
        print(f"\n   Top 3 problems:")
        for i, problem in enumerate(data['problems_detected'][:3], 1):
            print(f"      {i}. {problem['column']}: {problem['problem_type']} ({problem['probability']:.1%})")
else:
    print(f"❌ Error: {response.text}")

# Test 3: Clean file
print("\n3️⃣ Testing clean endpoint...")
with open(test_file, 'rb') as f:
    files = {'file': (test_file.name, f, 'text/csv')}
    response = requests.post(f"{API_URL}/clean", files=files)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    # Save cleaned file
    output_file = Path("data/processed/test_cleaned.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'wb') as f:
        f.write(response.content)
    
    print(f"✅ Cleaning successful!")
    print(f"   Original rows: {response.headers.get('X-Original-Rows')}")
    print(f"   Cleaned rows: {response.headers.get('X-Cleaned-Rows')}")
    print(f"   Problems fixed: {response.headers.get('X-Problems-Fixed')}")
    print(f"   Saved to: {output_file}")
else:
    print(f"❌ Error: {response.text}")

print("\n" + "=" * 60)
print("✅ API TESTING COMPLETE!")
print("=" * 60)