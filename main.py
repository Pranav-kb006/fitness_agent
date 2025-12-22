from fastapi import FastAPI, HTTPException
from models import UserHealthData
from brain import analyze_wellness

app = FastAPI(title="Fitness Agent Swarm - Wellness Node")

# This simulated "Database" holds the latest state for other agents to read
SYSTEM_STATE = {
    "latest_wellness_context": {}
}

@app.post("/ingest-wellness-data")
async def process_wearable_data(data: UserHealthData):
    """
    1. Receives data from frontend (Watch)
    2. Validates it
    3. Sends to Gemini (Brain)
    4. Updates the System State for other agents
    """
    try:
        print(f"Received data for {data.user_id}...")
        
        # Call the AI Brain
        analysis = analyze_wellness(data)
        
        # Update the Global State (This is the 'Feed' for other agents)
        SYSTEM_STATE["latest_wellness_context"] = analysis
        
        return {
            "status": "success", 
            "message": "Wellness data processed. Context updated for Nutrition/Exercise agents.",
            "generated_context": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-agent-context")
async def get_context():
    """
    Your Nutrition/Exercise Agents will call this endpoint 
    to know what to do today.
    """
    return SYSTEM_STATE["latest_wellness_context"]

# Run with: uvicorn main:app --reload