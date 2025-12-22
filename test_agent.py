import requests
import json

# The URL where your Wellness Agent is listening
API_URL = "http://localhost:8000/ingest-wellness-data"

def test_scenario(scenario_name, data):
    print(f"\n--- TESTING SCENARIO: {scenario_name} ---")
    print(f"Sending Watch Data: Sleep {data['total_sleep_hours']}h | HRV {data['hrv_score']} | RHR {data['resting_heart_rate']}")
    
    try:
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Agent Response:")
            # Pretty print the JSON output from the agent
            print(json.dumps(result["generated_context"], indent=2))
        else:
            print(f"❌ FAILED: {response.text}")
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("Make sure your uvicorn server is running!")

# SCENARIO 1: Ideal Recovery (The "Green" Zone)
good_data = {
    "user_id": "user_good_sleep",
    "date": "2024-05-21",
    "total_sleep_hours": 8.5,
    "deep_sleep_minutes": 90,
    "rem_sleep_minutes": 110,
    "resting_heart_rate": 52,
    "hrv_score": 75,
    "steps": 8000,
    "active_calories": 450
}

# SCENARIO 2: High Stress/Bad Sleep (The "Red" Zone)
bad_data = {
    "user_id": "user_bad_sleep",
    "date": "2024-05-21",
    "total_sleep_hours": 4.5,
    "deep_sleep_minutes": 15,
    "rem_sleep_minutes": 30,
    "resting_heart_rate": 85,  # High RHR (Stress)
    "hrv_score": 25,           # Low HRV (Fatigue)
    "steps": 12000,
    "active_calories": 600
}

if __name__ == "__main__":
    test_scenario("High Performance", good_data)
    test_scenario("Critical Fatigue", bad_data)