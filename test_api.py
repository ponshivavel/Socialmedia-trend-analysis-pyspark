import sys
sys.path.insert(0, 'c:/Users/ponshivavel/pysprak/Socialmedia-trend-analysis-pyspark')

# Test data file exists
import json
import os

data_path = 'c:/Users/ponshivavel/pysprak/Socialmedia-trend-analysis-pyspark/data/processed_data_latest.json'
if os.path.exists(data_path):
    with open(data_path) as f:
        data = json.load(f)
    print(f"Data loaded: {len(data.get('popularity', []))} popularity, {len(data.get('temporal', []))} temporal entries")
    print("Sample temporal:", data.get('temporal', [])[:2] if data.get('temporal') else "None")
else:
    print("Data file not found!")

# Test importing main
try:
    from backend.main import app
    print("Backend app imported successfully!")
except Exception as e:
    print(f"Error importing app: {e}")
