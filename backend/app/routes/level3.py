# from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from ..database import get_db
# from ..models.fra_record import FRARecord, ProcessingLevel
# from ..schemas.fra_schema import FRARecordResponse, ProcessingResponse
# from ..services.gemini_service import gemini_service
# from ..services.storage_service import storage_service

# router = APIRouter(prefix="/api/level3", tags=["Level 3 - Translation + Processing"])

# @router.post("/process", response_model=ProcessingResponse)
# async def process_translate_document(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     """Process Hindi/Marathi FRA document - Translate to English and perform NER"""
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
#             "level3"
#         )
        
#         # Extract text based on file type
#         if file_ext == '.pdf':
#             extracted_text = await gemini_service.extract_text_from_pdf(file_path)
#         else:
#             extracted_text = await gemini_service.extract_text_from_image(file_content)
        
#         # Detect source language
#         language = detect_language(extracted_text)
        
#         # Translate and perform NER
#         translation_result = await gemini_service.translate_and_ner(extracted_text, language)
        
#         # Extract data
#         translated_text = translation_result.get("translated_text", "")
#         extracted_fields = translation_result.get("extracted_fields", {})
#         entities = translation_result.get("entities", {})
        
#         # Create database record
#         fra_record = FRARecord(
#             level=ProcessingLevel.LEVEL3,
#             status="completed",
#             original_filename=file.filename,
#             file_path=file_path,
#             language=language,
#             raw_text=extracted_text,
#             translated_text=translated_text,
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
#             metadata={
#                 "source_language": language,
#                 "translated": True
#             }
#         )
        
#         db.add(fra_record)
#         db.commit()
#         db.refresh(fra_record)
        
#         return ProcessingResponse(
#             success=True,
#             message="Document translated and processed successfully",
#             record_id=fra_record.id,
#             data={
#                 "original_text": extracted_text,
#                 "translated_text": translated_text,
#                 "source_language": language,
#                 "ner_entities": entities,
#                 "extracted_fields": extracted_fields
#             }
#         )
    
#     except Exception as e:
#         # Log error and create failed record
#         db_record = FRARecord(
#             level=ProcessingLevel.LEVEL3,
#             status="failed",
#             original_filename=file.filename if file else "unknown",
#             language="unknown",
#             metadata={"error": str(e)}
#         )
#         db.add(db_record)
#         db.commit()
        
#         raise HTTPException(500, f"Processing failed: {str(e)}")

# @router.get("/records", response_model=List[FRARecordResponse])
# async def get_level3_records(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     """Get all Level 3 processed records"""
#     records = db.query(FRARecord).filter(
#         FRARecord.level == ProcessingLevel.LEVEL3
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
#     """Simple language detection based on character presence"""
#     # Check for Devanagari script (Hindi/Marathi)
#     devanagari_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
#     if devanagari_chars > 10:
#         # Simple heuristic to differentiate Hindi vs Marathi
#         marathi_chars = sum(1 for char in text if char in 'ळ')
#         if marathi_chars > 0:
#             return "marathi"
#         return "hindi"
    
#     return "hindi"  # Default


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

router = APIRouter(prefix="/api/level3", tags=["Level 3 - Translation + Processing"])


@router.post("/process", response_model=ProcessingResponse)
async def process_translate_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Process multi-language FRA document - Translate to English and store in English
    
    Flow:
    1. OCR in native language
    2. Detect source language
    3. Detect form type
    4. Translate to English
    5. Extract fields in English
    6. Check duplicates
    7. Store in English
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
            "level3"
        )
        
        # Step 3: Extract text (OCR in native language)
        print(f"📄 Extracting text from {file.filename}...")
        if file_ext == '.pdf':
            extracted_text = await gemini_service.extract_text_from_pdf(file_path)
        else:
            extracted_text = await gemini_service.extract_text_from_image(file_content)
        
        # Step 4: Detect source language
        print("🔍 Detecting language...")
        source_language = detect_language(extracted_text)
        print(f"✅ Detected language: {source_language}")
        
        # Step 5: Detect form type (before translation)
        print("📋 Detecting form type...")
        form_type = await fra_ner_service.detect_form_type(extracted_text)
        print(f"✅ Detected form type: {form_type}")
        
        if form_type == "UNKNOWN":
            raise HTTPException(400, "Could not identify FRA form type")
        
        # Step 6: Translate to English and extract fields
        print(f"🌐 Translating from {source_language} to English...")
        translation_result = await translate_and_extract(
            extracted_text, 
            form_type, 
            source_language
        )
        
        translated_text = translation_result.get("translated_text", "")
        extracted_fields = translation_result.get("extracted_fields", {})
        
        print("✅ Translation and extraction complete")
        
        # Step 7: Check for duplicates (using English fields)
        print("🔎 Checking for duplicates...")
        is_duplicate, duplicate_records, warning = duplicate_detection_service.check_duplicate(
            db, form_type, extracted_fields
        )
        
        if is_duplicate:
            print(f"⚠️ WARNING: Found {len(duplicate_records)} potential duplicate(s)")
        
        # Step 8: Store in database (in English)
        print("💾 Storing in database (English)...")
        claim_id = fra_storage_service.create_claim_record(
            db=db,
            form_type=form_type,
            extracted_fields=extracted_fields,
            file_path=file_path,
            raw_text=translated_text,  # Store translated text as raw_text
            language=f"{source_language}_to_english",
            processing_level="level3"
        )
        
        # Mark as duplicate if found
        if is_duplicate:
            fra_storage_service.mark_as_duplicate(db, claim_id)
        
        # Store original text in OCR table
        from ..models import OCRRaw
        ocr_record = OCRRaw(
            claim_id=claim_id,
            raw_text=extracted_text,  # Original text
            extracted_fields={"translation": translated_text}
        )
        db.add(ocr_record)
        db.commit()
        
        print(f"✅ Successfully stored with claim_id: {claim_id}")
        
        # Step 9: Return response
        return ProcessingResponse(
            success=True,
            message=f"Document translated from {source_language} to English and processed as {form_type}. {warning}",
            record_id=str(claim_id),
            data={
                "form_type": form_type,
                "source_language": source_language,
                "original_text": extracted_text,
                "translated_text": translated_text,
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


async def translate_and_extract(text: str, form_type: str, source_language: str) -> dict:
    """
    Translate text to English and extract form-specific fields
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
    
    language_name = language_map.get(source_language, source_language.title())
    
    # Get form-specific field structure (same as Level 1/2)
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
        # Use generic translation
        return await gemini_service.translate_and_ner(text, source_language)
    
    try:
        prompt = f"""
        You are an expert translator and FRA document analyzer.
        
        TASK:
        1. Translate this {form_type} document from {language_name} to English
        2. Extract structured information in English
        
        ORIGINAL TEXT IN {language_name.upper()}:
        {text}
        
        Return ONLY a valid JSON object:
        {{
            "translated_text": "Full English translation of the entire document...",
            "extracted_fields": {field_structure}
        }}
        
        CRITICAL RULES:
        - Translate ALL text to proper English
        - Preserve names in original script but also provide transliteration
        - For place names: use both - e.g., "Devgarh (देवगढ़)"
        - Extract ALL fields in English
        - For numbers, use numeric values
        - Return ONLY JSON (no markdown, no code blocks, no explanations)
        """
        
        response = await fra_ner_service.model.generate_content_async(prompt)
        raw = response.text.strip()
        
        # Clean up response
        raw = raw.replace("```json", "").replace("```", "").strip()
        
        import json
        result = json.loads(raw)
        
        return {
            "translated_text": result.get("translated_text", ""),
            "extracted_fields": result.get("extracted_fields", {})
        }
        
    except Exception as e:
        print(f"Translation + extraction error: {e}")
        return {
            "translated_text": text,  # Fallback to original
            "extracted_fields": {}
        }


def detect_language(text: str) -> str:
    """
    Enhanced language detection for all Indian languages
    (Same as Level 2)
    """
    if not text or len(text) < 10:
        return "unknown"
    
    char_counts = {
        "devanagari": 0,
        "bengali": 0,
        "telugu": 0,
        "tamil": 0,
        "odia": 0,
        "arabic": 0,
    }
    
    for char in text:
        code = ord(char)
        if 0x0900 <= code <= 0x097F:
            char_counts["devanagari"] += 1
        elif 0x0980 <= code <= 0x09FF:
            char_counts["bengali"] += 1
        elif 0x0C00 <= code <= 0x0C7F:
            char_counts["telugu"] += 1
        elif 0x0B80 <= code <= 0x0BFF:
            char_counts["tamil"] += 1
        elif 0x0B00 <= code <= 0x0B7F:
            char_counts["odia"] += 1
        elif 0x0600 <= code <= 0x06FF:
            char_counts["arabic"] += 1
    
    max_script = max(char_counts, key=char_counts.get)
    max_count = char_counts[max_script]
    
    if max_count < 10:
        return "english"
    
    if max_script == "devanagari":
        marathi_chars = sum(1 for char in text if char == 'ळ')
        if marathi_chars > 0:
            return "marathi"
        
        kokborok_keywords = ['त्रिपुरा', 'कोकबोरोक', 'त्रिपुरी']
        for keyword in kokborok_keywords:
            if keyword in text:
                return "kokborok"
        
        return "hindi"
        
    elif max_script == "bengali":
        kokborok_bengali_keywords = ['ত্রিপুরা', 'কোকবরক']
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
    
    return "english"


@router.get("/records", response_model=List[dict])
async def get_level3_records(
    skip: int = 0,
    limit: int = 100,
    form_type: str = None,
    source_language: str = None,
    db: Session = Depends(get_db)
):
    """Get all Level 3 processed records"""
    query = db.query(Claim).filter(Claim.processing_level == "level3")
    
    if form_type:
        query = query.filter(Claim.claim_type == form_type)
    
    if source_language:
        # Filter by language (stored as "hindi_to_english", etc.)
        query = query.filter(Claim.language.like(f"{source_language}%"))
    
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
    """Get specific record with original and translated text"""
    from uuid import UUID
    
    try:
        claim_uuid = UUID(claim_id)
    except ValueError:
        raise HTTPException(400, "Invalid claim_id format")
    
    claim = db.query(Claim).filter(Claim.claim_id == claim_uuid).first()
    
    if not claim:
        raise HTTPException(404, "Record not found")
    
    # Get original text from OCR table
    original_text = ""
    if claim.ocr_records:
        original_text = claim.ocr_records[0].raw_text
    
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
        "original_text": original_text,
        "translated_text": claim.summary.get("raw_text") if claim.summary else "",
        "duplicate_flag": claim.duplicate_flag,
        "created_at": claim.created_at.isoformat() if claim.created_at else None,
        "form_specific_data": form_data
    }


@router.delete("/records/{claim_id}")
async def delete_record(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """Delete a record"""
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
    """Get statistics for Level 3 processing"""
    from sqlalchemy import func
    
    total = db.query(func.count(Claim.claim_id)).filter(
        Claim.processing_level == "level3"
    ).scalar()
    
    by_form = db.query(
        Claim.claim_type,
        func.count(Claim.claim_id).label('count')
    ).filter(
        Claim.processing_level == "level3"
    ).group_by(Claim.claim_type).all()
    
    # Extract source language from "hindi_to_english" format
    records = db.query(Claim.language).filter(
        Claim.processing_level == "level3"
    ).all()
    
    by_language = {}
    for r in records:
        if r.language:
            source_lang = r.language.split("_to_")[0] if "_to_" in r.language else r.language
            by_language[source_lang] = by_language.get(source_lang, 0) + 1
    
    duplicates_count = db.query(func.count(Claim.claim_id)).filter(
        Claim.processing_level == "level3",
        Claim.duplicate_flag == True
    ).scalar()
    
    return {
        "total_records": total,
        "by_form_type": {f.claim_type: f.count for f in by_form},
        "by_source_language": by_language,
        "duplicates_flagged": duplicates_count
    }
