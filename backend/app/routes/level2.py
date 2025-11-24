# # from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# # from sqlalchemy.orm import Session
# # from typing import List
# # from ..database import get_db
# # from ..models.fra_record import FRARecord, ProcessingLevel
# # from ..schemas.fra_schema import FRARecordResponse, ProcessingResponse
# # from ..services.gemini_service import gemini_service
# # from ..services.storage_service import storage_service

# # router = APIRouter(prefix="/api/level2", tags=["Level 2 - Hindi/Marathi Processing"])

# # @router.post("/process", response_model=ProcessingResponse)
# # async def process_hindi_marathi_document(
# #     file: UploadFile = File(...),
# #     db: Session = Depends(get_db)
# # ):
# #     """Process Hindi/Marathi FRA document - Extract text and perform NER in native language"""
# #     try:
# #         # Validate file type
# #         allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
# #         file_ext = storage_service.get_file_extension(file.filename)
        
# #         if file_ext not in allowed_extensions:
# #             raise HTTPException(400, "Invalid file type. Allowed: PDF, PNG, JPG, JPEG")
        
# #         # Read file content
# #         file_content = await file.read()
        
# #         # Save uploaded file
# #         file_path = await storage_service.save_upload(
# #             file_content, 
# #             file.filename, 
# #             "level2"
# #         )
        
# #         # Extract text based on file type
# #         if file_ext == '.pdf':
# #             extracted_text = await gemini_service.extract_text_from_pdf(file_path)
# #         else:
# #             extracted_text = await gemini_service.extract_text_from_image(file_content)
        
# #         # Detect language (simple heuristic - can be improved)
# #         language = detect_language(extracted_text)
        
# #         # Perform NER in native language
# #         ner_result = await gemini_service.perform_ner_native_language(extracted_text, language)
        
# #         # Extract structured fields
# #         extracted_fields = ner_result.get("extracted_fields", {})
# #         entities = ner_result.get("entities", {})
        
# #         # Create database record
# #         fra_record = FRARecord(
# #             level=ProcessingLevel.LEVEL2,
# #             status="completed",
# #             original_filename=file.filename,
# #             file_path=file_path,
# #             language=language,
# #             raw_text=extracted_text,
# #             ner_entities=entities,
# #             patta_holder_name=extracted_fields.get("patta_holder_name"),
# #             village_name=extracted_fields.get("village_name"),
# #             state=extracted_fields.get("state"),
# #             district=extracted_fields.get("district"),
# #             block=extracted_fields.get("block"),
# #             claim_number=extracted_fields.get("claim_number"),
# #             claim_type=extracted_fields.get("claim_type"),
# #             claim_status=extracted_fields.get("claim_status"),
# #             survey_number=extracted_fields.get("survey_number"),
# #             area_in_hectares=extracted_fields.get("area_in_hectares"),
# #             coordinates=extracted_fields.get("coordinates"),
# #             metadata={"language_detected": language}
# #         )
        
# #         db.add(fra_record)
# #         db.commit()
# #         db.refresh(fra_record)
        
# #         return ProcessingResponse(
# #             success=True,
# #             message="Document processed successfully",
# #             record_id=fra_record.id,
# #             data={
# #                 "extracted_text": extracted_text,
# #                 "language": language,
# #                 "ner_entities": entities,
# #                 "extracted_fields": extracted_fields
# #             }
# #         )
    
# #     except Exception as e:
# #         # Log error and create failed record
# #         db_record = FRARecord(
# #             level=ProcessingLevel.LEVEL2,
# #             status="failed",
# #             original_filename=file.filename if file else "unknown",
# #             language="unknown",
# #             metadata={"error": str(e)}
# #         )
# #         db.add(db_record)
# #         db.commit()
        
# #         raise HTTPException(500, f"Processing failed: {str(e)}")

# # @router.get("/records", response_model=List[FRARecordResponse])
# # async def get_level2_records(
# #     skip: int = 0,
# #     limit: int = 100,
# #     db: Session = Depends(get_db)
# # ):
# #     """Get all Level 2 processed records"""
# #     records = db.query(FRARecord).filter(
# #         FRARecord.level == ProcessingLevel.LEVEL2
# #     ).offset(skip).limit(limit).all()
    
# #     return records

# # @router.get("/records/{record_id}", response_model=FRARecordResponse)
# # async def get_record_by_id(
# #     record_id: int,
# #     db: Session = Depends(get_db)
# # ):
# #     """Get specific record by ID"""
# #     record = db.query(FRARecord).filter(FRARecord.id == record_id).first()
    
# #     if not record:
# #         raise HTTPException(404, "Record not found")
    
# #     return record

# # @router.delete("/records/{record_id}")
# # async def delete_record(
# #     record_id: int,
# #     db: Session = Depends(get_db)
# # ):
# #     """Delete a record"""
# #     record = db.query(FRARecord).filter(FRARecord.id == record_id).first()
    
# #     if not record:
# #         raise HTTPException(404, "Record not found")
    
# #     db.delete(record)
# #     db.commit()
    
# #     return {"success": True, "message": "Record deleted successfully"}


# # def detect_language(text: str) -> str:
# #     """Simple language detection based on character presence"""
# #     # Check for Devanagari script (Hindi/Marathi)
# #     devanagari_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
# #     if devanagari_chars > 10:
# #         # Simple heuristic to differentiate Hindi vs Marathi
# #         # Marathi has some unique characters
# #         marathi_chars = sum(1 for char in text if char in 'ळ')
# #         if marathi_chars > 0:
# #             return "marathi"
# #         return "hindi"
    
# #     return "hindi"  # Default

# # all language
# from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from ..database import get_db
# from ..models.fra_record import FRARecord, ProcessingLevel
# from ..schemas.fra_schema import FRARecordResponse, ProcessingResponse
# from ..services.gemini_service import gemini_service
# from ..services.storage_service import storage_service

# router = APIRouter(prefix="/api/level2", tags=["Level 2 - Multi-language Processing"])

# @router.post("/process", response_model=ProcessingResponse)
# async def process_multilanguage_document(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     """Process multi-language FRA document - Extract text and perform NER in native language"""
#     try:
#         # Validate file type
#         allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
#         file_ext = storage_service.get_file_extension(file.filename)
        
#         if file_ext not in allowed_extensions:
#             raise HTTPException(400, "Invalid file type. Allowed: PDF, PNG, JPG, JPEG")
        
#         # Read file content
#         file_content = await file.read()
        
#         # Save uploaded file
#         file_path = await storage_service.save_upload(
#             file_content, 
#             file.filename, 
#             "level2"
#         )
        
#         # Extract text based on file type
#         if file_ext == '.pdf':
#             extracted_text = await gemini_service.extract_text_from_pdf(file_path)
#         else:
#             extracted_text = await gemini_service.extract_text_from_image(file_content)
        
#         # Detect language
#         language = detect_language(extracted_text)
        
#         # Perform NER in native language
#         ner_result = await gemini_service.perform_ner_native_language(extracted_text, language)
        
#         # Extract structured fields
#         extracted_fields = ner_result.get("extracted_fields", {})
#         entities = ner_result.get("entities", {})
        
#         # Create database record
#         fra_record = FRARecord(
#             level=ProcessingLevel.LEVEL2,
#             status="completed",
#             original_filename=file.filename,
#             file_path=file_path,
#             language=language,
#             raw_text=extracted_text,
#             ner_entities=entities,
#             patta_holder_name=extracted_fields.get("patta_holder_name"),
#             village_name=extracted_fields.get("village_name"),
#             state=extracted_fields.get("state"),
#             district=extracted_fields.get("district"),
#             block=extracted_fields.get("block"),
#             claim_number=extracted_fields.get("claim_number"),
#             claim_type=extracted_fields.get("claim_type"),
#             claim_status=extracted_fields.get("claim_status"),
#             survey_number=extracted_fields.get("survey_number"),
#             area_in_hectares=extracted_fields.get("area_in_hectares"),
#             coordinates=extracted_fields.get("coordinates"),
#             metadata={"language_detected": language}
#         )
        
#         db.add(fra_record)
#         db.commit()
#         db.refresh(fra_record)
        
#         return ProcessingResponse(
#             success=True,
#             message="Document processed successfully",
#             record_id=fra_record.id,
#             data={
#                 "extracted_text": extracted_text,
#                 "language": language,
#                 "ner_entities": entities,
#                 "extracted_fields": extracted_fields
#             }
#         )
    
#     except Exception as e:
#         # Log error and create failed record
#         db_record = FRARecord(
#             level=ProcessingLevel.LEVEL2,
#             status="failed",
#             original_filename=file.filename if file else "unknown",
#             language="unknown",
#             metadata={"error": str(e)}
#         )
#         db.add(db_record)
#         db.commit()
        
#         raise HTTPException(500, f"Processing failed: {str(e)}")

# @router.get("/records", response_model=List[FRARecordResponse])
# async def get_level2_records(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     """Get all Level 2 processed records"""
#     records = db.query(FRARecord).filter(
#         FRARecord.level == ProcessingLevel.LEVEL2
#     ).offset(skip).limit(limit).all()
    
#     return records

# @router.get("/records/{record_id}", response_model=FRARecordResponse)
# async def get_record_by_id(
#     record_id: int,
#     db: Session = Depends(get_db)
# ):
#     """Get specific record by ID"""
#     record = db.query(FRARecord).filter(FRARecord.id == record_id).first()
    
#     if not record:
#         raise HTTPException(404, "Record not found")
    
#     return record

# @router.delete("/records/{record_id}")
# async def delete_record(
#     record_id: int,
#     db: Session = Depends(get_db)
# ):
#     """Delete a record"""
#     record = db.query(FRARecord).filter(FRARecord.id == record_id).first()
    
#     if not record:
#         raise HTTPException(404, "Record not found")
    
#     db.delete(record)
#     db.commit()
    
#     return {"success": True, "message": "Record deleted successfully"}


# def detect_language(text: str) -> str:
#     """
#     Enhanced language detection for all Indian languages
#     """
#     if not text or len(text) < 10:
#         return "unknown"
    
#     # Character ranges for different scripts
#     char_counts = {
#         "devanagari": 0,  # Hindi, Marathi
#         "bengali": 0,      # Bengali
#         "telugu": 0,       # Telugu
#         "tamil": 0,        # Tamil
#         "odia": 0,         # Odia
#         "arabic": 0,       # Urdu
#     }
    
#     for char in text:
#         code = ord(char)
#         # Devanagari (Hindi, Marathi): U+0900 to U+097F
#         if 0x0900 <= code <= 0x097F:
#             char_counts["devanagari"] += 1
#         # Bengali: U+0980 to U+09FF
#         elif 0x0980 <= code <= 0x09FF:
#             char_counts["bengali"] += 1
#         # Telugu: U+0C00 to U+0C7F
#         elif 0x0C00 <= code <= 0x0C7F:
#             char_counts["telugu"] += 1
#         # Tamil: U+0B80 to U+0BFF
#         elif 0x0B80 <= code <= 0x0BFF:
#             char_counts["tamil"] += 1
#         # Odia: U+0B00 to U+0B7F
#         elif 0x0B00 <= code <= 0x0B7F:
#             char_counts["odia"] += 1
#         # Arabic script (Urdu): U+0600 to U+06FF
#         elif 0x0600 <= code <= 0x06FF:
#             char_counts["arabic"] += 1
    
#     # Find the script with most characters
#     max_script = max(char_counts, key=char_counts.get)
#     max_count = char_counts[max_script]
    
#     # Need at least 10 characters to confidently detect
#     if max_count < 10:
#         return "english"  # Default to English if uncertain
    
#     # Map script to language
#     if max_script == "devanagari":
#         # Differentiate between Hindi and Marathi
#         # Marathi has unique characters: ळ (0x0933)
#         marathi_chars = sum(1 for char in text if char == 'ळ')
#         if marathi_chars > 0:
#             return "marathi"
#         return "hindi"
#     elif max_script == "bengali":
#         return "bengali"
#     elif max_script == "telugu":
#         return "telugu"
#     elif max_script == "tamil":
#         return "tamil"
#     elif max_script == "odia":
#         return "odia"
#     elif max_script == "arabic":
#         return "urdu"
    
#     return "english"  # Default fallback



# 2 changes
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Claim
from ..schemas import ProcessingResponse
from ..services.gemini_service import gemini_service
from ..services.storage_service import storage_service
from ..services.fra_ner_service import fra_ner_service
from ..services.duplicate_detection_service import duplicate_detection_service
from ..services.fra_storage_service import fra_storage_service

router = APIRouter(prefix="/api/level2", tags=["Level 2 - Multi-language Processing"])


@router.post("/process", response_model=ProcessingResponse)
async def process_multilanguage_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Process multi-language FRA document - Extract text and perform NER in native language
    
    Supports: Hindi, Marathi, Bengali, Telugu, Tamil, Odia, Urdu, Kokborok
    Stores data in original language
    """
    try:
        # Step 1: Validate file type
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
        file_ext = storage_service.get_file_extension(file.filename)
        
        if file_ext not in allowed_extensions:
            raise HTTPException(400, "Invalid file type. Allowed: PDF, PNG, JPG, JPEG")
        
        # Step 2: Read and save file
        file_content = await file.read()
        file_path = await storage_service.save_upload(
            file_content, 
            file.filename, 
            "level2"
        )
        
        # Step 3: Extract text (OCR)
        print(f"📄 Extracting text from {file.filename}...")
        if file_ext == '.pdf':
            extracted_text = await gemini_service.extract_text_from_pdf(file_path)
        else:
            extracted_text = await gemini_service.extract_text_from_image(file_content)
        
        # Step 4: Detect language
        print("🔍 Detecting language...")
        language = detect_language(extracted_text)
        print(f"✅ Detected language: {language}")
        
        # Step 5: Detect form type (works with any language)
        print("📋 Detecting form type...")
        form_type = await fra_ner_service.detect_form_type(extracted_text)
        print(f"✅ Detected form type: {form_type}")
        
        if form_type == "UNKNOWN":
            raise HTTPException(400, "Could not identify FRA form type")
        
        # Step 6: Perform NER in native language
        print(f"🔍 Performing NER in {language}...")
        extracted_fields = await extract_fields_native(extracted_text, form_type, language)
        
        # Step 7: Check for duplicates
        print("🔎 Checking for duplicates...")
        is_duplicate, duplicate_records, warning = duplicate_detection_service.check_duplicate(
            db, form_type, extracted_fields
        )
        
        if is_duplicate:
            print(f"⚠️ WARNING: Found {len(duplicate_records)} potential duplicate(s)")
        
        # Step 8: Store in database
        print("💾 Storing in database...")
        claim_id = fra_storage_service.create_claim_record(
            db=db,
            form_type=form_type,
            extracted_fields=extracted_fields,
            file_path=file_path,
            raw_text=extracted_text,
            language=language,
            processing_level="level2"
        )
        
        # Mark as duplicate if found
        if is_duplicate:
            fra_storage_service.mark_as_duplicate(db, claim_id)
        
        print(f"✅ Successfully stored with claim_id: {claim_id}")
        
        # Step 9: Return response
        return ProcessingResponse(
            success=True,
            message=f"Document processed successfully as {form_type} in {language}. {warning}",
            record_id=str(claim_id),
            data={
                "form_type": form_type,
                "language": language,
                "extracted_text": extracted_text,
                "extracted_fields": extracted_fields,
                "is_duplicate": is_duplicate,
                "duplicate_records": duplicate_records if is_duplicate else []
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Processing failed: {str(e)}")


async def extract_fields_native(text: str, form_type: str, language: str) -> dict:
    """
    Extract fields in native language based on form type
    """
    if not fra_ner_service.model:
        raise Exception("NER service not initialized")
    
    fra_ner_service._rate_limit()
    
    # Language mapping
    language_map = {
        "hindi": "Hindi (हिंदी)",
        "marathi": "Marathi (मराठी)",
        "bengali": "Bengali (বাংলা)",
        "telugu": "Telugu (తెలుగు)",
        "tamil": "Tamil (தமிழ்)",
        "odia": "Odia (ଓଡ଼ିଆ)",
        "urdu": "Urdu (اردو)",
        "kokborok": "Kokborok"
    }
    
    language_name = language_map.get(language, language.title())
    
    # Get form-specific prompt template
    if form_type == "FORM_A":
        field_structure = """
        {
            "claimant_name": "",
            "spouse_name": "",
            "father_mother_name": "",
            "address": "",
            "village": "",
            "gram_panchayat": "",
            "tehsil": "",
            "district": "",
            "state": "",
            "is_scheduled_tribe": true/false/null,
            "is_otfd": true/false/null,
            "family_members": [{"name": "", "age": 0, "relation": ""}],
            "habitation_area": 0.0,
            "cultivation_area": 0.0,
            "disputed_lands": "",
            "pattas_or_leases": "",
            "khasra_numbers": [],
            "other_traditional_rights": ""
        }
        """
    elif form_type == "FORM_B":
        field_structure = """
        {
            "community_name": "",
            "village": "",
            "gram_panchayat": "",
            "tehsil": "",
            "district": "",
            "state": "",
            "is_fdst": true/false/null,
            "is_otfd": true/false/null,
            "nistar_rights": "",
            "minor_forest_produce": "",
            "community_uses": "",
            "grazing": "",
            "khasra_numbers": [],
            "boundary_description": ""
        }
        """
    elif form_type == "FORM_C":
        field_structure = """
        {
            "village": "",
            "gram_panchayat": "",
            "tehsil": "",
            "district": "",
            "state": "",
            "gram_sabha_member_list": [{"name": "", "category": "ST"}],
            "cfr_map_attached": true/false/null,
            "khasra_numbers": [],
            "bordering_villages": [],
            "boundary_description": ""
        }
        """
    elif form_type == "ANNEXURE_II":
        field_structure = """
        {
            "holder_name": "",
            "father_mother_name": "",
            "address": "",
            "village": "",
            "gram_panchayat": "",
            "tehsil": "",
            "district": "",
            "state": "",
            "is_st_or_otfd": "",
            "area_hectares": 0.0,
            "boundary_description": "",
            "khasra_numbers": [],
            "signed_by": []
        }
        """
    else:
        # Use generic extraction
        return await fra_ner_service.perform_ner(text)
    
    try:
        prompt = f"""
        Extract structured information from this {form_type} document written in {language_name}.
        
        KEEP ALL EXTRACTED VALUES IN THE ORIGINAL {language_name.upper()} LANGUAGE/SCRIPT.
        DO NOT TRANSLATE. PRESERVE ORIGINAL TEXT EXACTLY.
        
        TEXT TO ANALYZE:
        {text}
        
        Return ONLY a valid JSON object with this structure:
        {field_structure}
        
        CRITICAL RULES:
        - Return ONLY JSON (no explanation, no markdown, no code blocks)
        - Keep ALL values in original {language_name} script
        - For numbers (age, area), use numeric values
        - For booleans, use true/false/null
        - If field is missing, use empty string "" or empty array []
        """
        
        response = await fra_ner_service.model.generate_content_async(prompt)
        raw = response.text.strip()
        
        # Clean up response
        raw = raw.replace("```json", "").replace("```", "").strip()
        
        import json
        return json.loads(raw)
        
    except Exception as e:
        print(f"Native language extraction error: {e}")
        return {}


def detect_language(text: str) -> str:
    """
    Enhanced language detection for all Indian languages including Kokborok
    """
    if not text or len(text) < 10:
        return "unknown"
    
    # Character ranges for different scripts
    char_counts = {
        "devanagari": 0,  # Hindi, Marathi, Kokborok (when written in Devanagari)
        "bengali": 0,      # Bengali, Kokborok (native script similar)
        "telugu": 0,       # Telugu
        "tamil": 0,        # Tamil
        "odia": 0,         # Odia
        "arabic": 0,       # Urdu
    }
    
    # Count characters in different scripts
    for char in text:
        code = ord(char)
        # Devanagari (Hindi, Marathi, Kokborok in Devanagari): U+0900 to U+097F
        if 0x0900 <= code <= 0x097F:
            char_counts["devanagari"] += 1
        # Bengali (also covers Kokborok native script): U+0980 to U+09FF
        elif 0x0980 <= code <= 0x09FF:
            char_counts["bengali"] += 1
        # Telugu: U+0C00 to U+0C7F
        elif 0x0C00 <= code <= 0x0C7F:
            char_counts["telugu"] += 1
        # Tamil: U+0B80 to U+0BFF
        elif 0x0B80 <= code <= 0x0BFF:
            char_counts["tamil"] += 1
        # Odia: U+0B00 to U+0B7F
        elif 0x0B00 <= code <= 0x0B7F:
            char_counts["odia"] += 1
        # Arabic script (Urdu): U+0600 to U+06FF
        elif 0x0600 <= code <= 0x06FF:
            char_counts["arabic"] += 1
    
    # Find the script with most characters
    max_script = max(char_counts, key=char_counts.get)
    max_count = char_counts[max_script]
    
    # Need at least 10 characters to confidently detect
    if max_count < 10:
        return "english"  # Default to English if uncertain
    
    # Map script to language
    if max_script == "devanagari":
        # Differentiate between Hindi, Marathi, Kokborok
        
        # Marathi has unique characters: ळ (0x0933)
        marathi_chars = sum(1 for char in text if char == 'ळ')
        if marathi_chars > 0:
            return "marathi"
        
        # Kokborok-specific keywords (common in Tripura FRA documents)
        kokborok_keywords = ['त्रिपुरा', 'कोकबोरोक', 'त्रिपुरी', 'त्रिपुरा जनजाति']
        for keyword in kokborok_keywords:
            if keyword in text:
                return "kokborok"
        
        # Check for Tripura-related locations
        if 'त्रिपुरा' in text or 'अगरतला' in text:
            return "kokborok"
        
        return "hindi"
        
    elif max_script == "bengali":
        # Bengali vs Kokborok (both can use Bengali script)
        # Kokborok indicators
        kokborok_bengali_keywords = ['ত্রিপুরা', 'কোকবরক', 'ককবরক']
        for keyword in kokborok_bengali_keywords:
            if keyword in text:
                return "kokborok"
        
        return "bengali"
        
    elif max_script == "telugu":
        return "telugu"
    elif max_script == "tamil":
        return "tamil"
    elif max_script == "odia":
        return "odia"
    elif max_script == "arabic":
        return "urdu"
    
    return "english"  # Default fallback


@router.get("/records", response_model=List[dict])
async def get_level2_records(
    skip: int = 0,
    limit: int = 100,
    form_type: str = None,
    language: str = None,
    db: Session = Depends(get_db)
):
    """Get all Level 2 processed records with optional filters"""
    query = db.query(Claim).filter(Claim.processing_level == "level2")
    
    if form_type:
        query = query.filter(Claim.claim_type == form_type)
    
    if language:
        query = query.filter(Claim.language == language)
    
    records = query.offset(skip).limit(limit).all()
    
    return [
        {
            "claim_id": str(r.claim_id),
            "form_type": r.claim_type,
            "claimant_name": r.claimant_name,
            "village": r.village,
            "district": r.district,
            "state": r.state,
            "status": r.status,
            "language": r.language,
            "duplicate_flag": r.duplicate_flag,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in records
    ]


@router.get("/records/{claim_id}", response_model=dict)
async def get_record_by_id(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """Get specific record by claim_id"""
    from uuid import UUID
    
    try:
        claim_uuid = UUID(claim_id)
    except ValueError:
        raise HTTPException(400, "Invalid claim_id format")
    
    claim = db.query(Claim).filter(Claim.claim_id == claim_uuid).first()
    
    if not claim:
        raise HTTPException(404, "Record not found")
    
    # Get form-specific data
    form_data = {}
    if claim.claim_type == "FORM_A" and claim.ifr:
        form_data = {
            "spouse_name": claim.ifr.spouse_name,
            "father_mother_name": claim.ifr.father_mother_name,
            "habitation_area": float(claim.ifr.habitation_area) if claim.ifr.habitation_area else None,
            "cultivation_area": float(claim.ifr.cultivation_area) if claim.ifr.cultivation_area else None,
            "family_members": [
                {"name": f.name, "age": f.age, "relation": f.relation}
                for f in claim.ifr.family_members
            ]
        }
    elif claim.claim_type == "FORM_B" and claim.cr:
        form_data = {
            "community_name": claim.cr.community_name,
            "nistar_rights": claim.cr.nistar_rights,
            "minor_forest_produce": claim.cr.minor_forest_produce
        }
    
    return {
        "claim_id": str(claim.claim_id),
        "form_type": claim.claim_type,
        "claimant_name": claim.claimant_name,
        "village": claim.village,
        "district": claim.district,
        "state": claim.state,
        "status": claim.status,
        "language": claim.language,
        "duplicate_flag": claim.duplicate_flag,
        "created_at": claim.created_at.isoformat() if claim.created_at else None,
        "form_specific_data": form_data
    }


@router.delete("/records/{claim_id}")
async def delete_record(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """Delete a record (cascade deletes form-specific data)"""
    from uuid import UUID
    
    try:
        claim_uuid = UUID(claim_id)
    except ValueError:
        raise HTTPException(400, "Invalid claim_id format")
    
    claim = db.query(Claim).filter(Claim.claim_id == claim_uuid).first()
    
    if not claim:
        raise HTTPException(404, "Record not found")
    
    db.delete(claim)
    db.commit()
    
    return {"success": True, "message": "Record deleted successfully"}


@router.get("/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """Get statistics for Level 2 processing"""
    from sqlalchemy import func
    
    # Total records
    total = db.query(func.count(Claim.claim_id)).filter(
        Claim.processing_level == "level2"
    ).scalar()
    
    # By form type
    by_form = db.query(
        Claim.claim_type,
        func.count(Claim.claim_id).label('count')
    ).filter(
        Claim.processing_level == "level2"
    ).group_by(Claim.claim_type).all()
    
    # By language
    by_language = db.query(
        Claim.language,
        func.count(Claim.claim_id).label('count')
    ).filter(
        Claim.processing_level == "level2"
    ).group_by(Claim.language).all()
    
    # Duplicates
    duplicates_count = db.query(func.count(Claim.claim_id)).filter(
        Claim.processing_level == "level2",
        Claim.duplicate_flag == True
    ).scalar()
    
    return {
        "total_records": total,
        "by_form_type": {f.claim_type: f.count for f in by_form},
        "by_language": {l.language: l.count for l in by_language},
        "duplicates_flagged": duplicates_count
    }
