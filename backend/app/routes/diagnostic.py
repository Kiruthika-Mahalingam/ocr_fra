from fastapi import APIRouter
import sys
import os

router = APIRouter(prefix="/api/debug", tags=["Diagnostics"])

@router.get("/info")
async def get_system_info():
    """Get system information for debugging"""
    try:
        import google.generativeai as genai
        from ..config import settings
        
        return {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "gemini_configured": bool(settings.GEMINI_API_KEY),
            "openai_configured": bool(settings.OPENAI_API_KEY),
            "database_url": settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "configured",
            "environment": "OK"
        }
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__
        }