# # # # # # # level-1
# # # # # # # from fastapi import FastAPI
# # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # from .config import settings
# # # # # # # from .database import init_db
# # # # # # # from .routes import level1

# # # # # # # app = FastAPI(
# # # # # # #     title="FRA Digitization System",
# # # # # # #     description="AI-powered FRA document processing and digitization",
# # # # # # #     version="1.0.0"
# # # # # # # )

# # # # # # # # CORS Configuration
# # # # # # # app.add_middleware(
# # # # # # #     CORSMiddleware,
# # # # # # #     allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
# # # # # # #     allow_credentials=True,
# # # # # # #     allow_methods=["*"],
# # # # # # #     allow_headers=["*"],
# # # # # # # )

# # # # # # # # Initialize database
# # # # # # # @app.on_event("startup")
# # # # # # # async def startup_event():
# # # # # # #     init_db()

# # # # # # # # Include routers
# # # # # # # app.include_router(level1.router)

# # # # # # # # Health check
# # # # # # # @app.get("/")
# # # # # # # async def root():
# # # # # # #     return {
# # # # # # #         "message": "FRA Digitization System API",
# # # # # # #         "status": "running",
# # # # # # #         "version": "1.0.0"
# # # # # # #     }

# # # # # # # @app.get("/health")
# # # # # # # async def health_check():
# # # # # # #     return {"status": "healthy"}

# # # # # # # if __name__ == "__main__":
# # # # # # #     import uvicorn
# # # # # # #     uvicorn.run(
# # # # # # #         "app.main:app",
# # # # # # #         host=settings.HOST,
# # # # # # #         port=settings.PORT,
# # # # # # #         reload=True
# # # # # # #     )


# # # # # # # level-2
# # # # # # from fastapi import FastAPI
# # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # from .config import settings
# # # # # # from .database import init_db
# # # # # # from .routes import level1, level2

# # # # # # app = FastAPI(
# # # # # #     title="FRA Digitization System",
# # # # # #     description="AI-powered FRA document processing and digitization",
# # # # # #     version="1.0.0"
# # # # # # )

# # # # # # # CORS Configuration
# # # # # # app.add_middleware(
# # # # # #     CORSMiddleware,
# # # # # #     allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
# # # # # #     allow_credentials=True,
# # # # # #     allow_methods=["*"],
# # # # # #     allow_headers=["*"],
# # # # # # )

# # # # # # # Initialize database
# # # # # # @app.on_event("startup")
# # # # # # async def startup_event():
# # # # # #     init_db()

# # # # # # # Include routers
# # # # # # app.include_router(level1.router)
# # # # # # app.include_router(level2.router)

# # # # # # # Health check
# # # # # # @app.get("/")
# # # # # # async def root():
# # # # # #     return {
# # # # # #         "message": "FRA Digitization System API",
# # # # # #         "status": "running",
# # # # # #         "version": "1.0.0",
# # # # # #         "available_levels": ["level1", "level2"]
# # # # # #     }

# # # # # # @app.get("/health")
# # # # # # async def health_check():
# # # # # #     return {"status": "healthy"}

# # # # # # if __name__ == "__main__":
# # # # # #     import uvicorn
# # # # # #     uvicorn.run(
# # # # # #         "app.main:app",
# # # # # #         host=settings.HOST,
# # # # # #         port=settings.PORT,
# # # # # #         reload=True
# # # # # #     )


# # # # # # level-3
# # # # # from fastapi import FastAPI
# # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # from .config import settings
# # # # # from .database import init_db
# # # # # from .routes import level1, level2, level3

# # # # # app = FastAPI(
# # # # #     title="FRA Digitization System",
# # # # #     description="AI-powered FRA document processing and digitization",
# # # # #     version="1.0.0"
# # # # # )

# # # # # # CORS Configuration
# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )

# # # # # # Initialize database
# # # # # @app.on_event("startup")
# # # # # async def startup_event():
# # # # #     init_db()

# # # # # # Include routers
# # # # # app.include_router(level1.router)
# # # # # app.include_router(level2.router)
# # # # # app.include_router(level3.router)

# # # # # # Health check
# # # # # @app.get("/")
# # # # # async def root():
# # # # #     return {
# # # # #         "message": "FRA Digitization System API",
# # # # #         "status": "running",
# # # # #         "version": "1.0.0",
# # # # #         "available_levels": ["level1", "level2", "level3"]
# # # # #     }

# # # # # @app.get("/health")
# # # # # async def health_check():
# # # # #     return {"status": "healthy"}

# # # # # if __name__ == "__main__":
# # # # #     import uvicorn
# # # # #     uvicorn.run(
# # # # #         "app.main:app",
# # # # #         host=settings.HOST,
# # # # #         port=settings.PORT,
# # # # #         reload=True
# # # # #     )

# # # # # level-3
# # # # from fastapi import FastAPI
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # from .config import settings
# # # # from .database import init_db
# # # # from .routes import level1, level2, level3

# # # # app = FastAPI(
# # # #     title="FRA Digitization System",
# # # #     description="AI-powered FRA document processing and digitization",
# # # #     version="1.0.0"
# # # # )

# # # # # -------------------------
# # # # # ✅ FIXED CORS CONFIG
# # # # # -------------------------
# # # # allowed_origins = [
# # # #     settings.FRONTEND_URL,        # From .env
# # # #     "http://localhost:3000",
# # # #     "http://localhost:3001",      # REQUIRED for your current frontend
# # # #     "http://127.0.0.1:3001",
# # # #     "http://127.0.0.1:3000"
# # # # ]

# # # # app.add_middleware(
# # # #     CORSMiddleware,
# # # #     allow_origins=allowed_origins,
# # # #     allow_credentials=True,
# # # #     allow_methods=["*"],
# # # #     allow_headers=["*"],
# # # # )

# # # # # -------------------------
# # # # # DB INIT
# # # # # -------------------------
# # # # @app.on_event("startup")
# # # # async def startup_event():
# # # #     init_db()

# # # # # -------------------------
# # # # # ROUTERS
# # # # # -------------------------
# # # # app.include_router(level1.router)
# # # # app.include_router(level2.router)
# # # # app.include_router(level3.router)

# # # # # -------------------------
# # # # # HEALTH ENDPOINTS
# # # # # -------------------------
# # # # @app.get("/")
# # # # async def root():
# # # #     return {
# # # #         "message": "FRA Digitization System API",
# # # #         "status": "running",
# # # #         "version": "1.0.0",
# # # #         "available_levels": ["level1", "level2", "level3"]
# # # #     }

# # # # @app.get("/health")
# # # # async def health_check():
# # # #     return {"status": "healthy"}

# # # # # -------------------------
# # # # # RUN SERVER
# # # # # -------------------------
# # # # if __name__ == "__main__":
# # # #     import uvicorn
# # # #     uvicorn.run(
# # # #         "app.main:app",
# # # #         host=settings.HOST,
# # # #         port=settings.PORT,
# # # #         reload=True
# # # #     )


# # # # level-4  without cors
# # # from fastapi import FastAPI
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from .config import settings
# # # from .database import init_db
# # # from .routes import level1, level2, level3, level4

# # # app = FastAPI(
# # #     title="FRA Digitization System",
# # #     description="AI-powered FRA document processing and digitization",
# # #     version="1.0.0"
# # # )

# # # # CORS Configuration
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # # Initialize database
# # # @app.on_event("startup")
# # # async def startup_event():
# # #     init_db()

# # # # Include routers
# # # app.include_router(level1.router)
# # # app.include_router(level2.router)
# # # app.include_router(level3.router)
# # # app.include_router(level4.router)

# # # # Health check
# # # @app.get("/")
# # # async def root():
# # #     return {
# # #         "message": "FRA Digitization System API",
# # #         "status": "running",
# # #         "version": "1.0.0",
# # #         "available_levels": ["level1", "level2", "level3", "level4"]
# # #     }

# # # @app.get("/health")
# # # async def health_check():
# # #     return {"status": "healthy"}

# # # if __name__ == "__main__":
# # #     import uvicorn
# # #     uvicorn.run(
# # #         "app.main:app",
# # #         host=settings.HOST,
# # #         port=settings.PORT,
# # #         reload=True
# # #     )


# # # voice with cors
# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from .config import settings
# # from .database import init_db
# # from .routes import level1, level2, level3, level4

# # app = FastAPI(
# #     title="FRA Digitization System",
# #     description="AI-powered FRA document processing and digitization",
# #     version="1.0.0"
# # )

# # # ----------------------------------------------------
# # # ✅ FIXED CORS CONFIGURATION (WORKS FOR ALL FRONTENDS)
# # # ----------------------------------------------------
# # allowed_origins = [
# #     settings.FRONTEND_URL,           # From .env
# #     "http://localhost:3000",
# #     "http://localhost:3001",         # Your React frontend running here
# #     "http://127.0.0.1:3000",
# #     "http://127.0.0.1:3001"
# # ]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=allowed_origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Initialize database
# # @app.on_event("startup")
# # async def startup_event():
# #     init_db()

# # # Include routers
# # app.include_router(level1.router)
# # app.include_router(level2.router)
# # app.include_router(level3.router)
# # app.include_router(level4.router)

# # # Health check
# # @app.get("/")
# # async def root():
# #     return {
# #         "message": "FRA Digitization System API",
# #         "status": "running",
# #         "version": "1.0.0",
# #         "available_levels": ["level1", "level2", "level3", "level4"]
# #     }

# # @app.get("/health")
# # async def health_check():
# #     return {"status": "healthy"}

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(
# #         "app.main:app",
# #         host=settings.HOST,
# #         port=settings.PORT,
# #         reload=True
# #     )


# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from .config import settings
# from .database import init_db
# import traceback

# app = FastAPI(
#     title="FRA Digitization System",
#     description="AI-powered FRA document processing and digitization",
#     version="1.0.0"
# )

# # ============================================================
# # ✅ FULL CORS CONFIGURATION (UPDATED)
# # Supports: React (3000), Vite (5173), Mobile, Production URL
# # ============================================================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         settings.FRONTEND_URL,      # Production or deployed frontend
#         "http://localhost:3000",    # React default
#         "http://127.0.0.1:3000",
#         "http://localhost:5173",    # Vite default
#         "http://127.0.0.1:5173",
#         "*"                         # Temporary for development
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"],
# )

# # ============================================================
# # GLOBAL EXCEPTION HANDLER
# # ============================================================
# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     """Catch all exceptions and return detailed error"""
#     error_detail = {
#         "error": str(exc),
#         "type": type(exc).__name__,
#         "path": request.url.path,
#     }

#     print("=" * 80)
#     print(f"ERROR on {request.url.path}")
#     print("=" * 80)
#     traceback.print_exc()
#     print("=" * 80)

#     return JSONResponse(status_code=500, content=error_detail)

# # ============================================================
# # DATABASE STARTUP
# # ============================================================
# @app.on_event("startup")
# async def startup_event():
#     try:
#         init_db()
#         print("✓ Database initialized")
#     except Exception as e:
#         print(f"✗ Database initialization failed: {e}")

# # ============================================================
# # LOAD ROUTES SAFELY
# # ============================================================
# try:
#     from .routes import level1
#     app.include_router(level1.router)
#     print("✓ Level 1 routes loaded")
# except Exception as e:
#     print(f"✗ Failed to load Level 1: {e}")

# try:
#     from .routes import level2
#     app.include_router(level2.router)
#     print("✓ Level 2 routes loaded")
# except Exception as e:
#     print(f"✗ Failed to load Level 2: {e}")

# try:
#     from .routes import level3
#     app.include_router(level3.router)
#     print("✓ Level 3 routes loaded")
# except Exception as e:
#     print(f"✗ Failed to load Level 3: {e}")


# try:
#     from .routes import level4
#     app.include_router(level4.router)
#     print("✓ Level 4 routes loaded")
# except Exception as e:
#     print(f"✗ Failed to load Level 4: {e}")

# # ============================================================
# # ROOT ROUTE
# # ============================================================
# @app.get("/")
# async def root():
#     available_levels = []

#     for route in app.routes:
#         if hasattr(route, "path"):
#             if "/api/level1/" in route.path and "level1" not in available_levels:
#                 available_levels.append("level1")
#             elif "/api/level2/" in route.path and "level2" not in available_levels:
#                 available_levels.append("level2")
#             elif "/api/level3/" in route.path and "level3" not in available_levels:
#                 available_levels.append("level3")
#             elif "/api/level4/" in route.path and "level4" not in available_levels:
#                 available_levels.append("level4")

#     return {
#         "message": "FRA Digitization System API",
#         "status": "running",
#         "version": "1.0.0",
#         "available_levels": sorted(available_levels)
#     }

# # ============================================================
# # HEALTH CHECK ENDPOINT
# # ============================================================
# @app.get("/health")
# async def health_check():
#     health_status = {
#         "status": "healthy",
#         "database": "unknown",
#         "gemini_api": "unknown",
#         "openai_api": "unknown",
#     }

#     # Database Check
#     try:
#         from .database import SessionLocal
#         db = SessionLocal()
#         db.execute("SELECT 1")
#         db.close()
#         health_status["database"] = "connected"
#     except Exception as e:
#         health_status["database"] = f"error: {str(e)}"

#     # Gemini Check
#     try:
#         from .services.gemini_service import gemini_service
#         if gemini_service and gemini_service.model:
#             health_status["gemini_api"] = "configured"
#         else:
#             health_status["gemini_api"] = "not configured"
#     except Exception as e:
#         health_status["gemini_api"] = f"error: {str(e)}"

#     # OpenAI Check
#     try:
#         from .services.whisper_service import whisper_service
#         if whisper_service and whisper_service.client:
#             health_status["openai_api"] = "configured"
#         else:
#             health_status["openai_api"] = "not configured"
#     except Exception as e:
#         health_status["openai_api"] = f"error: {str(e)}"

#     return health_status

# # ============================================================
# # RUN SERVER
# # ============================================================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "app.main:app",
#         host=settings.HOST,
#         port=settings.PORT,
#         reload=True
#     )



from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .database import init_db
import traceback

app = FastAPI(
    title="FRA Digitization System",
    description="AI-powered FRA document processing and digitization",
    version="1.0.0"
)

# ============================================================
# ✅ FULL CORS CONFIGURATION (UPDATED)
# Supports: React (3000), Vite (5173), Mobile, Production URL
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,      # Production or deployed frontend
        "http://localhost:3000",    # React default
        "http://127.0.0.1:3000",
        "http://localhost:5173",    # Vite default
        "http://127.0.0.1:5173",
        "*"                         # Temporary for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all exceptions and return detailed error"""
    error_detail = {
        "error": str(exc),
        "type": type(exc).__name__,
        "path": request.url.path,
    }

    print("=" * 80)
    print(f"ERROR on {request.url.path}")
    print("=" * 80)
    traceback.print_exc()
    print("=" * 80)

    return JSONResponse(status_code=500, content=error_detail)

# ============================================================
# DATABASE STARTUP
# ============================================================
@app.on_event("startup")
async def startup_event():
    try:
        init_db()
        print("✓ Database initialized")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")

# ============================================================
# LOAD ROUTES SAFELY
# ============================================================
try:
    from .routes import level1
    app.include_router(level1.router)
    print("✓ Level 1 routes loaded")
except Exception as e:
    print(f"✗ Failed to load Level 1: {e}")
    traceback.print_exc()

try:
    from .routes import level2
    app.include_router(level2.router)
    print("✓ Level 2 routes loaded")
except Exception as e:
    print(f"✗ Failed to load Level 2: {e}")
    traceback.print_exc()

try:
    from .routes import level3
    app.include_router(level3.router)
    print("✓ Level 3 routes loaded")
except Exception as e:
    print(f"✗ Failed to load Level 3: {e}")
    traceback.print_exc()

try:
    from .routes import level4
    app.include_router(level4.router)
    print("✓ Level 4 routes loaded")
except Exception as e:
    print(f"✗ Failed to load Level 4: {e}")
    traceback.print_exc()

# ============================================================
# ROOT ROUTE
# ============================================================
@app.get("/")
async def root():
    available_levels = []

    for route in app.routes:
        if hasattr(route, "path"):
            if "/api/level1/" in route.path and "level1" not in available_levels:
                available_levels.append("level1")
            elif "/api/level2/" in route.path and "level2" not in available_levels:
                available_levels.append("level2")
            elif "/api/level3/" in route.path and "level3" not in available_levels:
                available_levels.append("level3")
            elif "/api/level4/" in route.path and "level4" not in available_levels:
                available_levels.append("level4")

    return {
        "message": "FRA Digitization System API",
        "status": "running",
        "version": "1.0.0",
        "available_levels": sorted(available_levels),
        "endpoints": {
            "level1": "/api/level1/ - Basic OCR with Tesseract",
            "level2": "/api/level2/ - AI-powered OCR with Gemini",
            "level3": "/api/level3/ - Multilingual support (9 languages)",
            "level4": "/api/level4/ - Voice-based form filling (Form A, B, C)"
        }
    }

# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================
@app.get("/health")
async def health_check():
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "gemini_api": "unknown",
        "openai_api": "unknown",
        "level4_questions": "unknown",
    }

    # Database Check
    try:
        from .database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        health_status["database"] = "connected"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Gemini Check
    try:
        from .services.gemini_service import gemini_service
        if gemini_service and gemini_service.model:
            health_status["gemini_api"] = "configured"
        else:
            health_status["gemini_api"] = "not configured"
    except Exception as e:
        health_status["gemini_api"] = f"error: {str(e)}"

    # OpenAI Check
    try:
        from .services.voice_service import voice_service
        if voice_service and voice_service.openai_client:
            health_status["openai_api"] = "configured"
        else:
            health_status["openai_api"] = "not configured"
    except Exception as e:
        health_status["openai_api"] = f"error: {str(e)}"

    # Level 4 Questions Service Check
    try:
        from .services.level4_questions import level4_questions_service
        form_a_questions = level4_questions_service.get_form_a_questions()
        if len(form_a_questions) > 0:
            health_status["level4_questions"] = f"loaded ({len(form_a_questions)} Form A questions)"
        else:
            health_status["level4_questions"] = "no questions loaded"
    except Exception as e:
        health_status["level4_questions"] = f"error: {str(e)}"

    return health_status

# ============================================================
# API INFO ENDPOINT
# ============================================================
@app.get("/api/info")
async def api_info():
    """Get detailed API information"""
    return {
        "api_version": "1.0.0",
        "levels": {
            "level1": {
                "name": "Basic OCR",
                "description": "Tesseract-based OCR with form detection",
                "endpoints": [
                    "POST /api/level1/process",
                    "GET /api/level1/records",
                    "GET /api/level1/records/{claim_id}",
                    "PUT /api/level1/records/{claim_id}/status",
                    "DELETE /api/level1/records/{claim_id}",
                    "GET /api/level1/stats"
                ]
            },
            "level2": {
                "name": "AI OCR",
                "description": "Gemini-powered OCR with NER",
                "endpoints": [
                    "POST /api/level2/process",
                    "GET /api/level2/records",
                    "GET /api/level2/records/{id}",
                    "DELETE /api/level2/records/{id}"
                ]
            },
            "level3": {
                "name": "Multilingual",
                "description": "Support for 9 Indian languages",
                "endpoints": [
                    "POST /api/level3/process",
                    "GET /api/level3/records",
                    "GET /api/level3/records/{id}",
                    "DELETE /api/level3/records/{id}"
                ],
                "supported_languages": [
                    "English", "Hindi", "Marathi", "Bengali", 
                    "Telugu", "Tamil", "Odia", "Urdu", "Kokborok"
                ]
            },
            "level4": {
                "name": "Voice Assistant",
                "description": "Voice-based form filling for Form A, B, C",
                "endpoints": [
                    "GET /api/level4/questions?form_type=FORM_A",
                    "POST /api/level4/text-to-speech",
                    "POST /api/level4/speech-to-text",
                    "POST /api/level4/submit-form",
                    "POST /api/level4/validate-response",
                    "GET /api/level4/records",
                    "GET /api/level4/records/{id}",
                    "DELETE /api/level4/records/{id}"
                ],
                "supported_forms": ["FORM_A", "FORM_B", "FORM_C"],
                "form_descriptions": {
                    "FORM_A": "Individual Forest Rights (16 questions)",
                    "FORM_B": "Community Rights (14 questions)",
                    "FORM_C": "Community Forest Resource (9 questions)"
                }
            }
        }
    }

# ============================================================
# RUN SERVER
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )