from fastapi import FastAPI, Request
from pydantic import BaseModel
from brain import analyze_wellness
from memory import store_memory  # <--- IMPORT MEMORY

app = FastAPI()

# This is the data structure we expect from the watch
class VitalData(BaseModel):
    user_id: str
    date: str
    sleep_hours: float
    hrv: int
    rhr: int

@app.get("/")
def home():
    return {"status": "active", "message": "Fitness Agent is Ready"}

@app.post("/webhook/vital")
async def receive_vital_data(data: VitalData):
    print(f"📥 Received Vital Event: {data}")

    # 1. Ask the Brain (Gemini)
    analysis = analyze_wellness(data)
    
    # 2. Store in Memory (Pinecone) <--- THIS PART WAS LIKELY MISSING
    # We pass the data we received + the analysis we just made
    store_memory(
        user_id=data.user_id,
        date=data.date,
        analysis_json=analysis
    )

    print("✅ Analysis Complete & Saved.")
    return analysis