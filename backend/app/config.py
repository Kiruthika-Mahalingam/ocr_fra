# from pydantic_settings import BaseSettings
# from typing import Optional

# class Settings(BaseSettings):
#     # Database
#     DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/fra_db"
    
#     # API Keys
#     GEMINI_API_KEY: str
#     OPENAI_API_KEY: str
    
#     # File Storage
#     UPLOAD_DIR: str = "uploads"
#     PROCESSED_DIR: str = "processed"
#     MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
#     # Server
#     HOST: str = "0.0.0.0"
#     PORT: int = 8000
    
#     # CORS
#     FRONTEND_URL: str = "http://localhost:3000"
    
#     class Config:
#         env_file = ".env"
#         case_sensitive = True

# settings = Settings()

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/fra_db"
    
    # API Keys
    GEMINI_API_KEY: str          # For OCR & NER
    GROQ_API_KEY: str            # For TTS (future use)
    OPENAI_API_KEY: str          # For Whisper STT
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    PROCESSED_DIR: str = "processed"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()