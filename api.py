from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
import sys

# Add current directory to path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.content_generator import ContentGenerator
from engine.ai_content_generator import AIContentGenerator
from engine.multi_category_generator import MultiCategoryGenerator
from database.supabase_db import SupabaseDB

app = FastAPI(title="AI Content Engine API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize generators
try:
    content_generator = ContentGenerator()
    ai_generator = AIContentGenerator()
    multi_generator = MultiCategoryGenerator()
    print("Generators initialized successfully")
except Exception as e:
    print(f"Error initializing generators: {e}")
    content_generator = None
    ai_generator = None
    multi_generator = None

# Initialize database
try:
    db = SupabaseDB()
    db_connected = db.test_connection()
    print(f"Database connected: {db_connected}")
except Exception as e:
    print(f"Database error: {e}")
    db = None
    db_connected = False

class GenerateRequest(BaseModel):
    topic: str
    context: Optional[str] = None
    model: Optional[str] = "openai/gpt-3.5-turbo"
    generate_all: Optional[bool] = False
    use_ai: Optional[bool] = True

class HistoryRequest(BaseModel):
    limit: Optional[int] = 10
    category: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "online", "service": "AI Content Engine API"}

@app.post("/api/generate")
async def generate_content(request: GenerateRequest):
    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    try:
        # Check if AI is available
        ai_available = ai_generator.ai_available if ai_generator else False
        
        # Decide which generator to use
        if request.generate_all and ai_available and multi_generator:
            # Generate all categories
            results = multi_generator.generate_all(
                topic=request.topic,
                context=request.context,
                model=request.model
            )
            return {"status": "success", "mode": "multi", "data": results}
            
        elif request.use_ai and ai_available and ai_generator:
            # Generate single category with AI
            result = ai_generator.generate(
                topic=request.topic,
                context=request.context,
                model=request.model
            )
            
            # Save to DB if connected
            if db and db_connected:
                try:
                    content_id = db.save_content(
                        topic=request.topic,
                        category=result['category'],
                        content_data=result
                    )
                    result['id'] = content_id
                except Exception as e:
                    print(f"Failed to save to DB: {e}")
            
            return {"status": "success", "mode": "single_ai", "data": result}
            
        else:
            # Fallback to template generator
            if not content_generator:
                raise HTTPException(status_code=500, detail="Content generator not initialized")
                
            result = content_generator.generate(
                topic=request.topic,
                context=request.context
            )
            return {"status": "success", "mode": "template", "data": result}
            
    except Exception as e:
        print(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history(limit: int = 10, category: Optional[str] = None):
    if not db or not db_connected:
        return {"status": "error", "message": "Database not connected", "data": []}
    
    try:
        history = db.get_history(limit=limit, category_filter=category)
        return {"status": "success", "data": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/content/{content_id}")
async def get_content(content_id: int):
    if not db or not db_connected:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    try:
        content = db.get_content_by_id(content_id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return {"status": "success", "data": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
