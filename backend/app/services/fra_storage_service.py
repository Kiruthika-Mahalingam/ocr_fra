from sqlalchemy.orm import Session
from typing import Dict, Optional
import uuid
from ..models import (
    Claim, OCRRaw, ClaimIFR, ClaimIFRFamily,
    ClaimCR, ClaimCFR, ClaimCFRKhasra, ClaimCFRNeighbors, ClaimCFRMembers,
    AnnexureII, AnnexureIIDependents,
    AnnexureIII, AnnexureIV, AnnexureIVSignatories,
    QuarterlyReport, ClaimHistory
)


class FRAStorageService:
    """
    Service to store form-specific data into appropriate database tables
    """
    
    @staticmethod
    def create_claim_record(
        db: Session,
        form_type: str,
        extracted_fields: Dict,
        file_path: str,
        raw_text: str,
        language: str = "english",
        processing_level: str = "level1"
    ) -> uuid.UUID:
        """
        Create master claim record and form-specific records
        
        Returns: claim_id (UUID)
        """
        
        # Create master claim record
        claim = Claim(
            claim_type=form_type,
            claimant_name=extracted_fields.get("claimant_name") or extracted_fields.get("holder_name") or extracted_fields.get("community_name"),
            village=extracted_fields.get("village"),
            gram_panchayat=extracted_fields.get("gram_panchayat"),
            tehsil=extracted_fields.get("tehsil"),
            district=extracted_fields.get("district"),
            state=extracted_fields.get("state"),
            status="pending",
            summary={"form_type": form_type, "extracted": True},
            original_pdf_path=file_path,
            processing_level=processing_level,
            language=language
        )
        
        db.add(claim)
        db.flush()  # Get claim_id
        
        # Store OCR raw text
        ocr_record = OCRRaw(
            claim_id=claim.claim_id,
            raw_text=raw_text,
            extracted_fields=extracted_fields
        )
        db.add(ocr_record)
        
        # Store form-specific data
        if form_type == "FORM_A":
            FRAStorageService._store_form_a(db, claim.claim_id, extracted_fields)
        elif form_type == "FORM_B":
            FRAStorageService._store_form_b(db, claim.claim_id, extracted_fields)
        elif form_type == "FORM_C":
            FRAStorageService._store_form_c(db, claim.claim_id, extracted_fields)
        elif form_type == "ANNEXURE_II":
            FRAStorageService._store_annexure_ii(db, claim.claim_id, extracted_fields)
        elif form_type == "ANNEXURE_III":
            FRAStorageService._store_annexure_iii(db, claim.claim_id, extracted_fields)
        elif form_type == "ANNEXURE_IV":
            FRAStorageService._store_annexure_iv(db, claim.claim_id, extracted_fields)
        elif form_type == "ANNEXURE_V":
            FRAStorageService._store_annexure_v(db, extracted_fields)
        
        db.commit()
        
        return claim.claim_id
    
    # ============================================================
    # FORM A STORAGE
    # ============================================================
    
    @staticmethod
    def _store_form_a(db: Session, claim_id: uuid.UUID, fields: Dict):
        """Store FORM-A data"""
        
        ifr = ClaimIFR(
            claim_id=claim_id,
            spouse_name=fields.get("spouse_name"),
            father_mother_name=fields.get("father_mother_name"),
            is_scheduled_tribe=fields.get("is_scheduled_tribe"),
            is_otfd=fields.get("is_otfd"),
            address=fields.get("address"),
            habitation_area=fields.get("habitation_area"),
            cultivation_area=fields.get("cultivation_area"),
            disputed_lands=fields.get("disputed_lands"),
            pattas_or_leases=fields.get("pattas_or_leases"),
            rehabilitation_land=fields.get("rehabilitation_land"),
            displacement_details=fields.get("displacement_details"),
            forest_village_extent=fields.get("forest_village_extent"),
            other_traditional_rights=fields.get("other_traditional_rights"),
            evidence_list=fields.get("evidence_list"),
            khasra_numbers=fields.get("khasra_numbers"),
            geo_boundary_text=fields.get("geo_boundary_text")
        )
        db.add(ifr)
        
        # Store family members
        family_members = fields.get("family_members", [])
        for member in family_members:
            if member.get("name"):
                family = ClaimIFRFamily(
                    claim_id=claim_id,
                    name=member.get("name"),
                    age=member.get("age"),
                    relation=member.get("relation")
                )
                db.add(family)
    
    # ============================================================
    # FORM B STORAGE
    # ============================================================
    
    @staticmethod
    def _store_form_b(db: Session, claim_id: uuid.UUID, fields: Dict):
        """Store FORM-B data"""
        
        cr = ClaimCR(
            claim_id=claim_id,
            community_name=fields.get("community_name"),
            village=fields.get("village"),
            gram_panchayat=fields.get("gram_panchayat"),
            tehsil=fields.get("tehsil"),
            district=fields.get("district"),
            is_st=fields.get("is_fdst"),
            is_otfd=fields.get("is_otfd"),
            nistar_rights=fields.get("nistar_rights"),
            minor_forest_produce=fields.get("minor_forest_produce"),
            community_uses=fields.get("community_uses"),
            grazing=fields.get("grazing"),
            pastoral_access=fields.get("pastoral_access"),
            habitat_rights=fields.get("habitat_rights"),
            biodiversity_access=fields.get("biodiversity_access"),
            other_traditional_rights=fields.get("other_traditional_rights"),
            evidence_list=fields.get("evidence_list"),
            khasra_numbers=fields.get("khasra_numbers"),
            boundary_description=fields.get("boundary_description")
        )
        db.add(cr)
    
    # ============================================================
    # FORM C STORAGE
    # ============================================================
    
    @staticmethod
    def _store_form_c(db: Session, claim_id: uuid.UUID, fields: Dict):
        """Store FORM-C data"""
        
        cfr = ClaimCFR(
            claim_id=claim_id,
            village=fields.get("village"),
            gram_panchayat=fields.get("gram_panchayat"),
            tehsil=fields.get("tehsil"),
            district=fields.get("district"),
            cfr_map_present=fields.get("cfr_map_attached"),
            boundary_description=fields.get("boundary_description"),
            evidence_list=fields.get("evidence_list")
        )
        db.add(cfr)
        
        # Store khasra numbers
        khasra_numbers = fields.get("khasra_numbers", [])
        for khasra in khasra_numbers:
            if khasra:
                khasra_entry = ClaimCFRKhasra(
                    claim_id=claim_id,
                    khasra_no=khasra
                )
                db.add(khasra_entry)
        
        # Store bordering villages
        bordering_villages = fields.get("bordering_villages", [])
        for village in bordering_villages:
            if village:
                neighbor = ClaimCFRNeighbors(
                    claim_id=claim_id,
                    neighboring_village=village
                )
                db.add(neighbor)
        
        # Store gram sabha members
        members = fields.get("gram_sabha_member_list", [])
        for member in members:
            if member.get("name"):
                member_entry = ClaimCFRMembers(
                    claim_id=claim_id,
                    name=member.get("name"),
                    category=member.get("category")
                )
                db.add(member_entry)
    
    # ============================================================
    # ANNEXURE II STORAGE
    # ============================================================
    
    @staticmethod
    def _store_annexure_ii(db: Session, claim_id: uuid.UUID, fields: Dict):
        """Store ANNEXURE-II data"""
        
        ann2 = AnnexureII(
            claim_id=claim_id,
            holder_name=fields.get("holder_name"),
            father_mother_name=fields.get("father_mother_name"),
            address=fields.get("address"),
            village=fields.get("village"),
            gram_panchayat=fields.get("gram_panchayat"),
            tehsil=fields.get("tehsil"),
            district=fields.get("district"),
            is_st_or_otfd=fields.get("is_st_or_otfd"),
            area=fields.get("area_hectares"),
            boundary_description=fields.get("boundary_description"),
            khasra_numbers=fields.get("khasra_numbers"),
            signed_by=fields.get("signed_by")
        )
        db.add(ann2)
        
        # Store dependents
        dependents = fields.get("dependents", [])
        for dependent in dependents:
            if dependent.get("name"):
                dep_entry = AnnexureIIDependents(
                    claim_id=claim_id,
                    name=dependent.get("name"),
                    age=dependent.get("age"),
                    relation=dependent.get("relation")
                )
                db.add(dep_entry)
    
    # ============================================================
    # ANNEXURE III STORAGE
    # ============================================================
    
    @staticmethod
    def _store_annexure_iii(db: Session, claim_id: uuid.UUID, fields: Dict):
        """Store ANNEXURE-III data"""
        
        ann3 = AnnexureIII(
            claim_id=claim_id,
            holders=fields.get("holders_list"),
            village=fields.get("village"),
            gram_panchayat=fields.get("gram_panchayat"),
            tehsil=fields.get("tehsil"),
            district=fields.get("district"),
            community_type=fields.get("community_type"),
            nature_of_rights=fields.get("nature_of_rights"),
            conditions=fields.get("conditions"),
            boundary_description=fields.get("boundary_description"),
            khasra_numbers=fields.get("khasra_numbers"),
            signed_by=fields.get("signed_by")
        )
        db.add(ann3)
    
    # ============================================================
    # ANNEXURE IV STORAGE
    # ============================================================
    
    @staticmethod
    def _store_annexure_iv(db: Session, claim_id: uuid.UUID, fields: Dict):
        """Store ANNEXURE-IV data"""
        
        ann4 = AnnexureIV(
            claim_id=claim_id,
            village=fields.get("village"),
            gram_panchayat=fields.get("gram_panchayat"),
            tehsil=fields.get("tehsil"),
            district=fields.get("district"),
            community_type=fields.get("community_type"),
            boundary_description=fields.get("boundary_description"),
            forest_area_hectares=fields.get("forest_area_hectares"),
            khasra_numbers=fields.get("khasra_numbers")
        )
        db.add(ann4)
        
        # Store signatories
        signed_by_list = fields.get("signed_by", [])
        for signatory in signed_by_list:
            if signatory:
                sig_entry = AnnexureIVSignatories(
                    claim_id=claim_id,
                    signed_by=signatory
                )
                db.add(sig_entry)
    
    # ============================================================
    # ANNEXURE V STORAGE
    # ============================================================
    
    @staticmethod
    def _store_annexure_v(db: Session, fields: Dict):
        """Store ANNEXURE-V data (Quarterly Report - no claim_id needed)"""
        
        report = QuarterlyReport(
            state=fields.get("state"),
            period_start=fields.get("period_start"),
            period_end=fields.get("period_end"),
            individual_filed=fields.get("individual_filed"),
            individual_accepted=fields.get("individual_accepted"),
            individual_rejected=fields.get("individual_rejected"),
            individual_pending=fields.get("individual_pending"),
            individual_area_ha=fields.get("individual_area_ha"),
            rejection_reasons_individual=fields.get("rejection_reasons_individual"),
            community_filed=fields.get("community_filed"),
            community_accepted=fields.get("community_accepted"),
            community_rejected=fields.get("community_rejected"),
            community_pending=fields.get("community_pending"),
            community_area_ha=fields.get("community_area_ha"),
            rejection_reasons_community=fields.get("rejection_reasons_community"),
            observations=fields.get("observations"),
            corrective_measures=fields.get("corrective_measures"),
            good_practices=fields.get("good_practices"),
            cfr_management_details=fields.get("cfr_management_details"),
            area_diverted_sec3_2=fields.get("area_diverted_sec3_2")
        )
        db.add(report)
    
    # ============================================================
    # UPDATE FUNCTIONS (for CRUD)
    # ============================================================
    
    @staticmethod
    def update_claim_status(
        db: Session,
        claim_id: uuid.UUID,
        new_status: str,
        changed_by: str,
        remarks: Optional[str] = None
    ):
        """Update claim status with history tracking"""
        
        claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
        if not claim:
            raise ValueError(f"Claim {claim_id} not found")
        
        # Create history record
        history = ClaimHistory(
            claim_id=claim_id,
            previous_status=claim.status,
            new_status=new_status,
            changed_by=changed_by,
            remarks=remarks
        )
        db.add(history)
        
        # Update claim
        claim.status = new_status
        db.commit()
    
    @staticmethod
    def mark_as_duplicate(db: Session, claim_id: uuid.UUID):
        """Mark a claim as duplicate"""
        claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
        if claim:
            claim.duplicate_flag = True
            db.commit()


# Export service
fra_storage_service = FRAStorageService()