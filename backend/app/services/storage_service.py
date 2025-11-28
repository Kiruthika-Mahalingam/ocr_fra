import os
import aiofiles
from pathlib import Path
from datetime import datetime
from ..config import settings

class StorageService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.processed_dir = Path(settings.PROCESSED_DIR)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        for level in ["level1", "level2", "level3", "level4"]:
            (self.upload_dir / level).mkdir(parents=True, exist_ok=True)
            (self.processed_dir / level).mkdir(parents=True, exist_ok=True)
    
    async def save_upload(self, file_content: bytes, filename: str, level: str) -> str:
        """Save uploaded file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        file_path = self.upload_dir / level / safe_filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        return str(file_path)
    
    async def save_processed_data(self, data: str, filename: str, level: str) -> str:
        """Save processed data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}.txt"
        file_path = self.processed_dir / level / safe_filename
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(data)
        
        return str(file_path)
    
    def get_file_extension(self, filename: str) -> str:
        """Get file extension"""
        return Path(filename).suffix.lower()

storage_service = StorageService()