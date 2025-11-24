# # from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
# # from fastapi.responses import StreamingResponse
# # from sqlalchemy.orm import Session
# # from typing import List, Optional
# # import io
# # from ..database import get_db
# # from ..models.fra_record import FRARecord, ProcessingLevel
# # from ..schemas.fra_schema import FRARecordResponse, ProcessingResponse
# # from ..services.gemini_service import gemini_service
# # from ..services.whisper_service import whisper_service

# # router = APIRouter(prefix="/api/level4", tags=["Level 4 - Voice Assistant"])

# # # FRA Form Questions
# # FRA_FORM_QUESTIONS = [
# #     {
# #         "id": "name",
# #         "question_en": "What is your name?",
# #         "question_hi": "आपका नाम क्या है?",
# #         "field": "patta_holder_name"
# #     },
# #     {
# #         "id": "village",
# #         "question_en": "What is your village name?",
# #         "question_hi": "आपके गाँव का नाम क्या है?",
# #         "field": "village_name"
# #     },
# #     {
# #         "id": "district",
# #         "question_en": "What is your district?",
# #         "question_hi": "आपका जिला क्या है?",
# #         "field": "district"
# #     },
# #     {
# #         "id": "state",
# #         "question_en": "What is your state?",
# #         "question_hi": "आपका राज्य क्या है?",
# #         "field": "state"
# #     },
# #     {
# #         "id": "block",
# #         "question_en": "What is your block?",
# #         "question_hi": "आपका ब्लॉक क्या है?",
# #         "field": "block"
# #     },
# #     {
# #         "id": "claim_type",
# #         "question_en": "What type of claim is this? Individual, Community, or Community Forest Resource?",
# #         "question_hi": "यह किस प्रकार का दावा है? व्यक्तिगत, सामुदायिक, या सामुदायिक वन संसाधन?",
# #         "field": "claim_type"
# #     },
# #     {
# #         "id": "survey_number",
# #         "question_en": "What is the survey number or khasra number?",
# #         "question_hi": "सर्वेक्षण संख्या या खसरा संख्या क्या है?",
# #         "field": "survey_number"
# #     },
# #     {
# #         "id": "area",
# #         "question_en": "What is the total area in hectares?",
# #         "question_hi": "हेक्टेयर में कुल क्षेत्रफल कितना है?",
# #         "field": "area_in_hectares"
# #     }
# # ]

# # @router.get("/questions")
# # async def get_form_questions():
# #     """Get all FRA form questions"""
# #     return {"questions": FRA_FORM_QUESTIONS}

# # @router.post("/text-to-speech")
# # async def text_to_speech(
# #     text: str = Form(...),
# #     language: str = Form(default="hindi")
# # ):
# #     """Convert text to speech"""
# #     try:
# #         audio_bytes = await gemini_service.generate_speech(text, language)
        
# #         return StreamingResponse(
# #             io.BytesIO(audio_bytes),
# #             media_type="audio/mpeg",
# #             headers={
# #                 "Content-Disposition": "inline; filename=speech.mp3"
# #             }
# #         )
# #     except Exception as e:
# #         raise HTTPException(500, f"TTS failed: {str(e)}")

# # @router.post("/speech-to-text")
# # async def speech_to_text(
# #     audio: UploadFile = File(...),
# #     language: str = Form(default="hi")
# # ):
# #     """Convert speech to text using Whisper"""
# #     try:
# #         audio_bytes = await audio.read()
        
# #         text = await whisper_service.transcribe_audio(audio_bytes, language)
        
# #         return {
# #             "success": True,
# #             "text": text
# #         }
# #     except Exception as e:
# #         raise HTTPException(500, f"STT failed: {str(e)}")

# # @router.post("/submit-form", response_model=ProcessingResponse)
# # async def submit_voice_form(
# #     form_data: dict,
# #     db: Session = Depends(get_db)
# # ):
# #     """Submit completed voice form"""
# #     try:
# #         # Extract form responses
# #         responses = form_data.get("responses", {})
# #         language = form_data.get("language", "hindi")
        
# #         # Build text representation
# #         form_text_lines = []
# #         for question in FRA_FORM_QUESTIONS:
# #             answer = responses.get(question["id"], "")
# #             if answer:
# #                 form_text_lines.append(f"{question['question_en']}: {answer}")
        
# #         form_text = "\n".join(form_text_lines)
        
# #         # Perform NER on collected data
# #         ner_result = await gemini_service.perform_ner(form_text)
# #         extracted_fields = ner_result.get("extracted_fields", {})
# #         entities = ner_result.get("entities", {})
        
# #         # Override with direct form responses
# #         for question in FRA_FORM_QUESTIONS:
# #             field_name = question["field"]
# #             if question["id"] in responses:
# #                 extracted_fields[field_name] = responses[question["id"]]
        
# #         # Create database record
# #         fra_record = FRARecord(
# #             level=ProcessingLevel.LEVEL4,
# #             status="completed",
# #             original_filename="voice_form",
# #             language=language,
# #             raw_text=form_text,
# #             ner_entities=entities,
# #             patta_holder_name=extracted_fields.get("patta_holder_name"),
# #             village_name=extracted_fields.get("village_name"),
# #             state=extracted_fields.get("state"),
# #             district=extracted_fields.get("district"),
# #             block=extracted_fields.get("block"),
# #             claim_type=extracted_fields.get("claim_type"),
# #             survey_number=extracted_fields.get("survey_number"),
# #             area_in_hectares=extracted_fields.get("area_in_hectares"),
# #             metadata={
# #                 "input_method": "voice",
# #                 "language": language,
# #                 "responses": responses
# #             }
# #         )
        
# #         db.add(fra_record)
# #         db.commit()
# #         db.refresh(fra_record)
        
# #         return ProcessingResponse(
# #             success=True,
# #             message="Voice form submitted successfully",
# #             record_id=fra_record.id,
# #             data={
# #                 "extracted_text": form_text,
# #                 "ner_entities": entities,
# #                 "extracted_fields": extracted_fields,
# #                 "responses": responses
# #             }
# #         )
    
# #     except Exception as e:
# #         raise HTTPException(500, f"Form submission failed: {str(e)}")

# # @router.get("/records", response_model=List[FRARecordResponse])
# # async def get_level4_records(
# #     skip: int = 0,
# #     limit: int = 100,
# #     db: Session = Depends(get_db)
# # ):
# #     """Get all Level 4 processed records"""
# #     records = db.query(FRARecord).filter(
# #         FRARecord.level == ProcessingLevel.LEVEL4
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



# from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
# from fastapi.responses import StreamingResponse
# from sqlalchemy.orm import Session
# from typing import List, Optional
# import io
# from ..database import get_db
# from ..models.fra_record import FRARecord, ProcessingLevel
# from ..schemas.fra_schema import FRARecordResponse, ProcessingResponse
# from ..services.gemini_service import gemini_service
# from ..services.voice_service import voice_service  # New unified voice service

# router = APIRouter(prefix="/api/level4", tags=["Level 4 - Voice Assistant"])

# # FRA Form Questions
# FRA_FORM_QUESTIONS = [
#     {
#         "id": "name",
#         "question_en": "What is your name?",
#         "question_hi": "आपका नाम क्या है?",
#         "field": "patta_holder_name"
#     },
#     {
#         "id": "village",
#         "question_en": "What is your village name?",
#         "question_hi": "आपके गाँव का नाम क्या है?",
#         "field": "village_name"
#     },
#     {
#         "id": "district",
#         "question_en": "What is your district?",
#         "question_hi": "आपका जिला क्या है?",
#         "field": "district"
#     },
#     {
#         "id": "state",
#         "question_en": "What is your state?",
#         "question_hi": "आपका राज्य क्या है?",
#         "field": "state"
#     },
#     {
#         "id": "block",
#         "question_en": "What is your block?",
#         "question_hi": "आपका ब्लॉक क्या है?",
#         "field": "block"
#     },
#     {
#         "id": "claim_type",
#         "question_en": "What type of claim is this? Individual, Community, or Community Forest Resource?",
#         "question_hi": "यह किस प्रकार का दावा है? व्यक्तिगत, सामुदायिक, या सामुदायिक वन संसाधन?",
#         "field": "claim_type"
#     },
#     {
#         "id": "survey_number",
#         "question_en": "What is the survey number or khasra number?",
#         "question_hi": "सर्वेक्षण संख्या या खसरा संख्या क्या है?",
#         "field": "survey_number"
#     },
#     {
#         "id": "area",
#         "question_en": "What is the total area in hectares?",
#         "question_hi": "हेक्टेयर में कुल क्षेत्रफल कितना है?",
#         "field": "area_in_hectares"
#     }
# ]

# @router.get("/questions")
# async def get_form_questions():
#     """Get all FRA form questions"""
#     return {"questions": FRA_FORM_QUESTIONS}

# @router.post("/text-to-speech")
# async def text_to_speech(
#     text: str = Form(...),
#     language: str = Form(default="hindi")
# ):
#     """
#     Convert text to speech using Groq TTS
#     Currently using gTTS as fallback until Groq TTS is available
#     """
#     try:
#         if not voice_service:
#             raise HTTPException(503, "Voice service not available")
        
#         print(f"TTS Request: text='{text[:50]}...', language={language}")
            
#         audio_bytes = await voice_service.generate_speech(text, language)
        
#         return StreamingResponse(
#             io.BytesIO(audio_bytes),
#             media_type="audio/mpeg",
#             headers={
#                 "Content-Disposition": "inline; filename=speech.mp3"
#             }
#         )
#     except Exception as e:
#         print(f"TTS Error: {e}")
#         raise HTTPException(500, f"TTS failed: {str(e)}")

# @router.post("/speech-to-text")
# async def speech_to_text(
#     audio: UploadFile = File(...),
#     language: str = Form(default="hi")
# ):
#     """
#     Convert speech to text using OpenAI Whisper
#     """
#     try:
#         if not voice_service:
#             raise HTTPException(503, "Voice service not available")
        
#         print(f"STT Request: filename={audio.filename}, language={language}")
            
#         audio_bytes = await audio.read()
        
#         text = await voice_service.transcribe_audio(audio_bytes, language)
        
#         print(f"STT Result: '{text}'")
        
#         return {
#             "success": True,
#             "text": text
#         }
#     except Exception as e:
#         print(f"STT Error: {e}")
#         raise HTTPException(500, f"STT failed: {str(e)}")

# @router.post("/submit-form", response_model=ProcessingResponse)
# async def submit_voice_form(
#     form_data: dict,
#     db: Session = Depends(get_db)
# ):
#     """Submit completed voice form"""
#     try:
#         # Extract form responses
#         responses = form_data.get("responses", {})
#         language = form_data.get("language", "hindi")
        
#         print(f"Form submission: {len(responses)} responses, language={language}")
        
#         # Build text representation
#         form_text_lines = []
#         for question in FRA_FORM_QUESTIONS:
#             answer = responses.get(question["id"], "")
#             if answer:
#                 form_text_lines.append(f"{question['question_en']}: {answer}")
        
#         form_text = "\n".join(form_text_lines)
        
#         # Perform NER on collected data
#         if gemini_service and gemini_service.model:
#             ner_result = await gemini_service.perform_ner(form_text)
#             extracted_fields = ner_result.get("extracted_fields", {})
#             entities = ner_result.get("entities", {})
#         else:
#             extracted_fields = {}
#             entities = {}
        
#         # Override with direct form responses
#         for question in FRA_FORM_QUESTIONS:
#             field_name = question["field"]
#             if question["id"] in responses:
#                 extracted_fields[field_name] = responses[question["id"]]
        
#         # Create database record
#         fra_record = FRARecord(
#             level=ProcessingLevel.LEVEL4,
#             status="completed",
#             original_filename="voice_form",
#             language=language,
#             raw_text=form_text,
#             ner_entities=entities,
#             patta_holder_name=extracted_fields.get("patta_holder_name"),
#             village_name=extracted_fields.get("village_name"),
#             state=extracted_fields.get("state"),
#             district=extracted_fields.get("district"),
#             block=extracted_fields.get("block"),
#             claim_type=extracted_fields.get("claim_type"),
#             survey_number=extracted_fields.get("survey_number"),
#             area_in_hectares=extracted_fields.get("area_in_hectares"),
#             metadata={
#                 "input_method": "voice",
#                 "language": language,
#                 "responses": responses
#             }
#         )
        
#         db.add(fra_record)
#         db.commit()
#         db.refresh(fra_record)
        
#         print(f"Form saved: record_id={fra_record.id}")
        
#         return ProcessingResponse(
#             success=True,
#             message="Voice form submitted successfully",
#             record_id=fra_record.id,
#             data={
#                 "extracted_text": form_text,
#                 "ner_entities": entities,
#                 "extracted_fields": extracted_fields,
#                 "responses": responses
#             }
#         )
    
#     except Exception as e:
#         print(f"Form submission error: {e}")
#         raise HTTPException(500, f"Form submission failed: {str(e)}")

# @router.get("/records", response_model=List[FRARecordResponse])
# async def get_level4_records(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     """Get all Level 4 processed records"""
#     records = db.query(FRARecord).filter(
#         FRARecord.level == ProcessingLevel.LEVEL4
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

# app/routes/level4.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional
import json

from ..database import get_db
from ..services.voice_service import voice_service
from ..services.level4_questions import level4_questions_service
# from ..services.fra_storage import fra_storage_service
from ..services.fra_storage_service import fra_storage_service
from ..schemas import ProcessingResponse, FRARecord, FRARecordDetail
from ..models import Claim

router = APIRouter(prefix="/api/level4", tags=["Level 4 - Voice Assistant"])

# ============================================================
# GET QUESTIONS FOR FORM TYPE
# ============================================================
@router.get("/questions")
async def get_questions(form_type: str = "FORM_A"):
    """
    Get questions for a specific form type
    
    Supported form types:
    - FORM_A: Individual Forest Rights (16 questions)
    - FORM_B: Community Rights (14 questions)  
    - FORM_C: Community Forest Resource (9 questions)
    """
    try:
        questions = level4_questions_service.get_questions_by_form_type(form_type)
        return {
            "success": True,
            "form_type": form_type,
            "questions": questions,
            "total": len(questions)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load questions: {str(e)}")

# ============================================================
# TEXT TO SPEECH
# ============================================================
@router.post("/text-to-speech")
async def text_to_speech(
    text: str = Form(...),
    language: str = Form(default="hindi")
):
    """
    Convert text to speech for voice-based form filling
    
    Args:
        text: Text to convert to speech
        language: Language code (hindi, marathi, english)
    
    Returns:
        Audio file (MP3 format)
    """
    if not voice_service:
        raise HTTPException(status_code=503, detail="Voice service not available")
    
    try:
        audio_bytes = await voice_service.generate_speech(text, language)
        
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3",
                "Cache-Control": "no-cache"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")

# ============================================================
# SPEECH TO TEXT
# ============================================================
@router.post("/speech-to-text")
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = Form(default="hi")
):
    """
    Convert speech to text (transcription)
    
    Args:
        audio: Audio file (webm, mp3, wav, etc.)
        language: Language code
            - 'hi' for Hindi
            - 'en' for English
            - 'mr' for Marathi
    
    Returns:
        Transcribed text
    """
    if not voice_service:
        raise HTTPException(status_code=503, detail="Voice service not available")
    
    try:
        audio_bytes = await audio.read()
        
        if not audio_bytes or len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        transcript = await voice_service.transcribe_audio(audio_bytes, language)
        
        return {
            "success": True,
            "text": transcript,
            "language": language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

# ============================================================
# SUBMIT FORM
# ============================================================
@router.post("/submit-form", response_model=ProcessingResponse)
async def submit_form(
    form_type: str = Form(...),
    responses: str = Form(...),  # JSON string of responses
    language: str = Form(default="english"),
    db: Session = Depends(get_db)
):
    """
    Submit completed voice-based form
    
    Args:
        form_type: FORM_A, FORM_B, or FORM_C
        responses: JSON object with question_id: answer pairs
        language: Language used for the form (english, hindi, marathi)
    
    Returns:
        ProcessingResponse with claim_id and extracted fields
    """
    try:
        # Parse responses
        try:
            responses_dict = json.loads(responses)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid responses JSON format")
        
        # Validate form type
        if form_type.upper() not in ["FORM_A", "FORM_B", "FORM_C"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid form type: {form_type}. Must be FORM_A, FORM_B, or FORM_C"
            )
        
        # Get questions to map responses to fields
        questions = level4_questions_service.get_questions_by_form_type(form_type)
        
        # Build extracted_fields based on form type
        extracted_fields = {}
        
        for question in questions:
            field_id = question["id"]
            field_type = question["field_type"]
            
            if field_id in responses_dict:
                response_text = responses_dict[field_id]
                parsed_value = level4_questions_service.parse_response(
                    field_id, field_type, response_text
                )
                extracted_fields[field_id] = parsed_value
        
        # Store in database
        claim_id = fra_storage_service.create_claim_record(
            db=db,
            form_type=form_type.upper(),
            extracted_fields=extracted_fields,
            file_path=f"voice_form_{form_type.lower()}",
            raw_text=json.dumps(responses_dict, ensure_ascii=False),
            language=language,
            processing_level="level4"
        )
        
        return ProcessingResponse(
            success=True,
            message=f"Form {form_type} submitted successfully via voice",
            record_id=str(claim_id),
            data={
                "form_type": form_type,
                "extracted_fields": extracted_fields,
                "claim_id": str(claim_id),
                "language": language
            }
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid responses JSON")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit form: {str(e)}")

# ============================================================
# VALIDATE RESPONSE
# ============================================================
@router.post("/validate-response")
async def validate_response(
    field_id: str = Form(...),
    field_type: str = Form(...),
    response_text: str = Form(...)
):
    """
    Validate a single response before moving to next question
    
    Args:
        field_id: Question/field ID
        field_type: Field type (text, boolean, number, array)
        response_text: User's response text
    
    Returns:
        Validation result with parsed value
    """
    try:
        parsed_value = level4_questions_service.parse_response(
            field_id, field_type, response_text
        )
        
        is_valid = parsed_value is not None
        
        return {
            "success": True,
            "is_valid": is_valid,
            "parsed_value": parsed_value,
            "original_text": response_text
        }
    except Exception as e:
        return {
            "success": False,
            "is_valid": False,
            "error": str(e),
            "original_text": response_text
        }

# ============================================================
# GET RECORDS
# ============================================================
@router.get("/records", response_model=list[FRARecord])
async def get_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all Level 4 voice-based form records
    """
    try:
        records = db.query(Claim)\
            .filter(Claim.processing_level == "level4")\
            .order_by(Claim.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        return [
            FRARecord(
                claim_id=str(record.claim_id),
                form_type=record.claim_type,
                claimant_name=record.claimant_name,
                village=record.village,
                district=record.district,
                state=record.state,
                status=record.status,
                duplicate_flag=record.duplicate_flag,
                created_at=record.created_at.isoformat() if record.created_at else None
            )
            for record in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch records: {str(e)}")

# ============================================================
# GET RECORD BY ID
# ============================================================
@router.get("/records/{claim_id}", response_model=FRARecordDetail)
async def get_record_by_id(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific Level 4 record by claim ID
    """
    try:
        record = db.query(Claim).filter(
            Claim.claim_id == claim_id,
            Claim.processing_level == "level4"
        ).first()
        
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # Get form-specific data
        form_specific_data = {}
        
        if record.claim_type == "FORM_A" and record.ifr:
            form_specific_data = {
                "spouse_name": record.ifr.spouse_name,
                "father_mother_name": record.ifr.father_mother_name,
                "is_scheduled_tribe": record.ifr.is_scheduled_tribe,
                "is_otfd": record.ifr.is_otfd,
                "habitation_area": float(record.ifr.habitation_area) if record.ifr.habitation_area else None,
                "cultivation_area": float(record.ifr.cultivation_area) if record.ifr.cultivation_area else None,
                "khasra_numbers": record.ifr.khasra_numbers,
                "geo_boundary_text": record.ifr.geo_boundary_text
            }
        elif record.claim_type == "FORM_B" and record.cr:
            form_specific_data = {
                "community_name": record.cr.community_name,
                "is_st": record.cr.is_st,
                "is_otfd": record.cr.is_otfd,
                "nistar_rights": record.cr.nistar_rights,
                "minor_forest_produce": record.cr.minor_forest_produce,
                "grazing": record.cr.grazing,
                "khasra_numbers": record.cr.khasra_numbers
            }
        elif record.claim_type == "FORM_C" and record.cfr:
            form_specific_data = {
                "cfr_map_present": record.cfr.cfr_map_present,
                "boundary_description": record.cfr.boundary_description,
                "khasra_count": len(record.cfr.khasra_entries) if record.cfr.khasra_entries else 0,
                "neighbors_count": len(record.cfr.neighbors) if record.cfr.neighbors else 0
            }
        
        return FRARecordDetail(
            claim_id=str(record.claim_id),
            form_type=record.claim_type,
            claimant_name=record.claimant_name,
            village=record.village,
            gram_panchayat=record.gram_panchayat,
            tehsil=record.tehsil,
            district=record.district,
            state=record.state,
            status=record.status,
            duplicate_flag=record.duplicate_flag,
            language=record.language,
            created_at=record.created_at.isoformat() if record.created_at else None,
            form_specific_data=form_specific_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch record: {str(e)}")

# ============================================================
# DELETE RECORD
# ============================================================
@router.delete("/records/{claim_id}")
async def delete_record(
    claim_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a Level 4 record
    """
    try:
        record = db.query(Claim).filter(
            Claim.claim_id == claim_id,
            Claim.processing_level == "level4"
        ).first()
        
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        db.delete(record)
        db.commit()
        
        return {
            "success": True,
            "message": "Record deleted successfully",
            "claim_id": claim_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete record: {str(e)}")

# ============================================================
# GET STATISTICS
# ============================================================
@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get Level 4 statistics
    """
    try:
        total = db.query(Claim).filter(Claim.processing_level == "level4").count()
        
        form_a = db.query(Claim).filter(
            Claim.processing_level == "level4",
            Claim.claim_type == "FORM_A"
        ).count()
        
        form_b = db.query(Claim).filter(
            Claim.processing_level == "level4",
            Claim.claim_type == "FORM_B"
        ).count()
        
        form_c = db.query(Claim).filter(
            Claim.processing_level == "level4",
            Claim.claim_type == "FORM_C"
        ).count()
        
        duplicates = db.query(Claim).filter(
            Claim.processing_level == "level4",
            Claim.duplicate_flag == True
        ).count()
        
        return {
            "success": True,
            "total_records": total,
            "by_form_type": {
                "FORM_A": form_a,
                "FORM_B": form_b,
                "FORM_C": form_c
            },
            "duplicates_flagged": duplicates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {str(e)}")