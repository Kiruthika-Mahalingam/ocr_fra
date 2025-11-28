# app/api/endpoints/level4.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, List
import json

from ...database import get_db
from ...services.voice_service import voice_service
from ...services.level4_questions import level4_questions_service
from ...services.fra_storage import fra_storage_service
from ...schemas import ProcessingResponse

router = APIRouter()

@router.get("/questions")
async def get_questions(form_type: str = "FORM_A"):
    """
    Get questions for a specific form type
    Supported: FORM_A, FORM_B, FORM_C
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

@router.post("/text-to-speech")
async def text_to_speech(
    text: str = Form(...),
    language: str = Form(default="hindi")
):
    """
    Convert text to speech for voice-based form filling
    """
    if not voice_service:
        raise HTTPException(status_code=503, detail="Voice service not available")
    
    try:
        audio_bytes = await voice_service.generate_speech(text, language)
        
        from fastapi.responses import Response
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")

@router.post("/speech-to-text")
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = Form(default="hi")
):
    """
    Convert speech to text (transcription)
    language: 'hi' for Hindi, 'en' for English, 'mr' for Marathi
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

@router.post("/submit-form")
async def submit_form(
    form_type: str = Form(...),
    responses: str = Form(...),  # JSON string of responses
    language: str = Form(default="english"),
    db: Session = Depends(get_db)
):
    """
    Submit completed voice-based form
    
    form_type: FORM_A, FORM_B, or FORM_C
    responses: JSON object with question_id: answer pairs
    """
    try:
        # Parse responses
        responses_dict = json.loads(responses)
        
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
            form_type=form_type,
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
                "claim_id": str(claim_id)
            }
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid responses JSON")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit form: {str(e)}")

@router.post("/validate-response")
async def validate_response(
    field_id: str = Form(...),
    field_type: str = Form(...),
    response_text: str = Form(...)
):
    """
    Validate a single response before moving to next question
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
            "error": str(e)
        }