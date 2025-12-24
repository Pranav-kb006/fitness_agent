import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_wellness(data):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 1. Create the Prompt
    # Note: We changed data.total_sleep_hours -> data.sleep_hours
    prompt = f"""
    Act as a professional athletic coach. Analyze this daily data:
    
    - Sleep: {data.sleep_hours} hrs  <--- FIXED HERE
    - HRV: {data.hrv} ms
    - Resting Heart Rate: {data.rhr} bpm
    
    Output ONLY valid JSON with this structure (no markdown, no quotes around the block):
    {{
      "readiness_score": (0-100),
      "exercise_instruction": "string",
      "nutrition_instruction": "string",
      "flag_manager": true/false
    }}
    """
    
    # 2. Get the Response
    response = model.generate_content(prompt)
    
    # 3. Clean the Response (Remove ```json ... ``` if Gemini adds it)
    clean_text = response.text.replace("```json", "").replace("```", "").strip()
    
    return json.loads(clean_text)