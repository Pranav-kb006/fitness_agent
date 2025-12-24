import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
# 1. Initialize Pinecone (Database)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

# 2. Initialize Local Embedding Model
# We use 'all-mpnet-base-v2' because it outputs 768 dimensions (same as Gemini)
# This downloads the model to your computer the first time you run it.
print("⏳ Loading local embedding model (this happens once)...")
embed_model = SentenceTransformer('all-mpnet-base-v2')
print("✅ Local model loaded.")

def store_memory(user_id, date, analysis_json):
    print(f"🧠 Storing memory for {user_id} on {date}...")
    
    # Create the text summary
    text_content = f"""
    Date: {date}
    User: {user_id}
    Readiness Score: {analysis_json.get('readiness_score')}
    Advice: {analysis_json.get('exercise_instruction')}
    Nutrition: {analysis_json.get('nutrition_instruction')}
    """
    
    try:
        # --- THE CHANGE ---
        # Instead of calling Google, we use the local model
        vector = embed_model.encode(text_content).tolist()

        # Save to Pinecone
        index.upsert(
            vectors=[{
                "id": f"{user_id}_{date}",
                "values": vector,
                "metadata": {
                    "user_id": user_id,
                    "date": date,
                    "text_content": text_content
                }
            }]
        )
        print("✅ Memory successfully stored in Pinecone (Local Embeddings).")
        
    except Exception as e:
        print(f"❌ Failed to store memory: {e}")