import os
import json
from google import genai
from models import UserHealthData

def analyze_wellness(data: UserHealthData):
    # 1. Initialize the Client using the new library
    # Make sure you ran $env:GOOGLE_API_KEY="..." in your terminal first!
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    
    # 2. The Prompt
    system_prompt = f"""
    You are the Wellness Agent. Analyze this user health data.
    
    DATA:
    - Sleep: {data.total_sleep_hours} hrs
    - HRV: {data.hrv_score}
    - RHR: {data.resting_heart_rate}
    
    RULES:
    1. If Sleep < 6h OR HRV < 40: Set "readiness_score" low (0-40).
    2. If Sleep > 7h AND HRV > 60: Set "readiness_score" high (70-100).
    
    OUTPUT SCHEMA (JSON ONLY):
    {{
        "readiness_score": (int),
        "exercise_instruction": (string),
        "nutrition_instruction": (string),
        "flag_manager": (boolean)
    }}
    """
    
    try:
        # 3. Call the model (New Syntax)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
        
        # 4. Parse JSON
        if response.text is None:
            return {"error": "Empty response from AI"}
        return json.loads(response.text)
        
    except Exception as e:
        print(f"AI Error: {e}")
        return {"error": "AI processing failed", "details": str(e)}