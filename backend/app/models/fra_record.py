from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Enum
from sqlalchemy.sql import func
from ..database import Base
import enum

class ProcessingLevel(enum.Enum):
    LEVEL1 = "level1"
    LEVEL2 = "level2"
    LEVEL3 = "level3"
    LEVEL4 = "level4"

class FRARecord(Base):
    __tablename__ = "fra_records"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Processing metadata
    level = Column(Enum(ProcessingLevel), nullable=False)
    status = Column(String(50), default="processing")  # processing, completed, failed
    
    # File information
    original_filename = Column(String(255))
    file_path = Column(String(500))
    language = Column(String(50))
    
    # Extracted text
    raw_text = Column(Text)
    translated_text = Column(Text, nullable=True)
    
    # NER Results (stored as JSON)
    ner_entities = Column(JSON)
    
    # Extracted FRA Information
    patta_holder_name = Column(String(255))
    village_name = Column(String(255))
    state = Column(String(100))
    district = Column(String(100))
    block = Column(String(100))
    
    # Claim information
    claim_number = Column(String(100))
    claim_type = Column(String(50))  # IFR, CR, CFR
    claim_status = Column(String(50))
    
    # Land details
    survey_number = Column(String(100))
    area_in_hectares = Column(String(50))
    coordinates = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional metadata
    # metadata = Column(JSON)
    record_metadata = Column(JSON)
