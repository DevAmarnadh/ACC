"""
AI Content Creation Engine - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uvicorn
from pathlib import Path

from engine.content_generator import ContentGenerator
from database.db import Database, ContentHistory

# Initialize FastAPI app
app = FastAPI(
    title="AI Content Creation Engine",
    description="Autonomous AI engine for multi-platform viral content generation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = Database()
content_generator = ContentGenerator()

# Pydantic Models
class ContentRequest(BaseModel):
    topic: str = Field(..., min_length=5, description="The main topic or idea for content generation")
    context: Optional[str] = Field(None, description="Additional context or information")

class ContentResponse(BaseModel):
    id: int
    category: str
    master_storyline: str
    youtube_script: str
    instagram_script: str
    twitter_thread: List[str]
    caption: str
    cta: List[str]
    hashtags: List[str]
    created_at: str

class HistoryItem(BaseModel):
    id: int
    topic: str
    category: str
    created_at: str

# API Routes
@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.post("/api/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """
    Generate multi-platform content from a topic
    
    - **topic**: The main idea or topic to generate content for
    - **context**: Optional additional information or context
    """
    try:
        # Generate content using the AI engine
        result = content_generator.generate(
            topic=request.topic,
            context=request.context
        )
        
        # Save to database
        content_id = db.save_content(
            topic=request.topic,
            category=result['category'],
            content_data=result
        )
        
        # Add ID and timestamp to response
        result['id'] = content_id
        result['created_at'] = datetime.now().isoformat()
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@app.get("/api/history", response_model=List[HistoryItem])
async def get_history(limit: int = 20):
    """
    Get content generation history
    
    - **limit**: Maximum number of items to return (default: 20)
    """
    try:
        history = db.get_history(limit=limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")

@app.get("/api/content/{content_id}", response_model=ContentResponse)
async def get_content(content_id: int):
    """
    Get a specific content by ID
    
    - **content_id**: The ID of the content to retrieve
    """
    try:
        content = db.get_content_by_id(content_id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch content: {str(e)}")

@app.delete("/api/content/{content_id}")
async def delete_content(content_id: int):
    """
    Delete a specific content by ID
    
    - **content_id**: The ID of the content to delete
    """
    try:
        success = db.delete_content(content_id)
        if not success:
            raise HTTPException(status_code=404, detail="Content not found")
        return {"message": "Content deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete content: {str(e)}")

@app.get("/api/categories")
async def get_categories():
    """Get all available content categories"""
    return {
        "categories": [
            {
                "id": "new_tool_intro",
                "name": "New Tool Introduction",
                "description": "Introducing newly released AI tools"
            },
            {
                "id": "tool_detailed_tutorial",
                "name": "Detailed Tutorial",
                "description": "Step-by-step guides and tutorials"
            },
            {
                "id": "trending_ai_model",
                "name": "Trending AI Model",
                "description": "Coverage of trending AI models and capabilities"
            },
            {
                "id": "ai_trending_news",
                "name": "AI News",
                "description": "Latest AI news and trending discussions"
            },
            {
                "id": "github_open_source_repo",
                "name": "Open Source Repository",
                "description": "GitHub repos and open-source projects"
            },
            {
                "id": "instagram_engagement_content",
                "name": "Engagement Content",
                "description": "Casual tips and audience interaction content"
            }
        ]
    }

@app.get("/api/stats")
async def get_stats():
    """Get usage statistics"""
    try:
        stats = db.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    db.init_db()
    print("✅ Database initialized")
    print("✅ AI Content Engine is ready!")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Create static directory if it doesn't exist
    Path("static").mkdir(exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
