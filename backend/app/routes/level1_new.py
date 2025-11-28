from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Claim
from ..schemas import ProcessingResponse, FRARecord as FRARecordResponse
from ..services.gemini_service import gemini_service
from ..services.storage_service import storage_service
from ..services.fra_ner_service import fra_ner_service
from ..services.duplicate_detection_service import duplicate_detection_service
from ..services.fra_storage_service import fra_storage_service

router = APIRouter(prefix="/api/level1", tags=["Level 1 - English Processing"])


@router.post("/process", response_model=ProcessingResponse)
async def process_english_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Process English FRA document with form-specific NER
    
    Flow:
    1. Upload & OCR
    2. Detect form type (A, B, C, II, III, IV, V)
    3. Extract form-specific fields
    4. Check for duplicates
    5. Store in appropriate tables
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
            "level1"
        )
        
        # Step 3: Extract text (OCR)
        print(f"📄 Extracting text from {file.filename}...")
        if file_ext == '.pdf':
            extracted_text = await gemini_service.extract_text_from_pdf(file_path)
        else:
            extracted_text = await gemini_service.extract_text_from_image(file_content)
        
        # Step 4: Perform form-specific NER
        print("🔍 Performing NER and form detection...")
        ner_result = await fra_ner_service.perform_ner(extracted_text)
        
        form_type = ner_result.get("form_type", "UNKNOWN")
        extracted_fields = ner_result.get("extracted_fields", {})
        
        if form_type == "UNKNOWN":
            raise HTTPException(400, "Could not identify FRA form type")
        
        print(f"✅ Detected form type: {form_type}")
        
        # Step 5: Check for duplicates
        print("🔎 Checking for duplicates...")
        is_duplicate, duplicate_records, warning = duplicate_detection_service.check_duplicate(
            db, form_type, extracted_fields
        )
        
        if is_duplicate:
            print(f"⚠️ WARNING: Found {len(duplicate_records)} potential duplicate(s)")
        
        # Step 6: Store in database
        print("💾 Storing in database...")
        claim_id = fra_storage_service.create_claim_record(
            db=db,
            form_type=form_type,
            extracted_fields=extracted_fields,
            file_path=file_path,
            raw_text=extracted_text,
            language="english",
            processing_level="level1"
        )
        
        # Mark as duplicate if found
        if is_duplicate:
            fra_storage_service.mark_as_duplicate(db, claim_id)
        
        print(f"✅ Successfully stored with claim_id: {claim_id}")
        
        # Step 7: Return response
        return ProcessingResponse(
            success=True,
            message=f"Document processed successfully as {form_type}. {warning}",
            record_id=str(claim_id),
            data={
                "form_type": form_type,
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


@router.get("/records", response_model=List[dict])
async def get_level1_records(
    skip: int = 0,
    limit: int = 100,
    form_type: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all Level 1 processed records with optional form type filter
    """
    query = db.query(Claim).filter(Claim.processing_level == "level1")
    
    if form_type:
        query = query.filter(Claim.claim_type == form_type)
    
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
    """Get specific record by claim_id with full details"""
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
    # Add more form types as needed...
    
    return {
        "claim_id": str(claim.claim_id),
        "form_type": claim.claim_type,
        "claimant_name": claim.claimant_name,
        "village": claim.village,
        "gram_panchayat": claim.gram_panchayat,
        "tehsil": claim.tehsil,
        "district": claim.district,
        "state": claim.state,
        "status": claim.status,
        "duplicate_flag": claim.duplicate_flag,
        "language": claim.language,
        "created_at": claim.created_at.isoformat() if claim.created_at else None,
        "form_specific_data": form_data
    }


@router.put("/records/{claim_id}/status")
async def update_claim_status(
    claim_id: str,
    status: str,
    changed_by: str = "system",
    remarks: str = None,
    db: Session = Depends(get_db)
):
    """Update claim status"""
    from uuid import UUID
    
    try:
        claim_uuid = UUID(claim_id)
    except ValueError:
        raise HTTPException(400, "Invalid claim_id format")
    
    valid_statuses = ["pending", "accepted", "rejected", "under_review"]
    if status not in valid_statuses:
        raise HTTPException(400, f"Invalid status. Must be one of: {valid_statuses}")
    
    fra_storage_service.update_claim_status(
        db, claim_uuid, status, changed_by, remarks
    )
    
    return {"success": True, "message": f"Status updated to {status}"}


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
    """Get statistics for Level 1 processing"""
    from sqlalchemy import func
    
    stats = db.query(
        Claim.claim_type,
        func.count(Claim.claim_id).label('count')
    ).filter(
        Claim.processing_level == "level1"
    ).group_by(Claim.claim_type).all()
    
    duplicates_count = db.query(func.count(Claim.claim_id)).filter(
        Claim.processing_level == "level1",
        Claim.duplicate_flag == True
    ).scalar()
    
    return {
        "total_records": sum([s.count for s in stats]),
        "by_form_type": {s.claim_type: s.count for s in stats},
        "duplicates_flagged": duplicates_count
    }
