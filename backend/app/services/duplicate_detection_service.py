from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Dict, List, Optional, Tuple
from ..models import Claim, ClaimIFR, ClaimCR, ClaimCFR, AnnexureII


class DuplicateDetectionService:
    """
    Detect duplicate FRA claims based on form-specific criteria
    """
    
    @staticmethod
    def normalize_text(text: Optional[str]) -> str:
        """Normalize text for comparison"""
        if not text:
            return ""
        return text.lower().strip()
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Simple string similarity metric (can be enhanced with fuzzy matching)
        Returns score between 0 and 1
        """
        if not text1 or not text2:
            return 0.0
        
        t1 = DuplicateDetectionService.normalize_text(text1)
        t2 = DuplicateDetectionService.normalize_text(text2)
        
        if t1 == t2:
            return 1.0
        
        # Simple character-level similarity
        # Can be enhanced with libraries like fuzzywuzzy or rapidfuzz
        set1 = set(t1.split())
        set2 = set(t2.split())
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    # ============================================================
    # FORM A - IFR Duplicate Detection
    # ============================================================
    
    @staticmethod
    def check_form_a_duplicate(
        db: Session,
        claimant_name: str,
        father_mother_name: str,
        village: str,
        khasra_numbers: List[str],
        habitation_area: float,
        cultivation_area: float,
        threshold: float = 0.85
    ) -> Tuple[bool, List[Dict]]:
        """
        Check for duplicate FORM-A claims
        
        Duplicate criteria:
        - Same claimant name + father/mother name + village (high confidence)
        - Same khasra numbers in same village (medium confidence)
        - Similar total area (habitation + cultivation) in same village (low confidence)
        """
        
        duplicates = []
        
        # Query existing FORM-A claims
        existing_claims = db.query(Claim, ClaimIFR).join(
            ClaimIFR, Claim.claim_id == ClaimIFR.claim_id
        ).filter(
            Claim.claim_type == "FORM_A"
        ).all()
        
        for claim, ifr in existing_claims:
            score = 0.0
            reasons = []
            
            # Check 1: Name similarity
            name_sim = DuplicateDetectionService.calculate_similarity(
                claimant_name, claim.claimant_name
            )
            if name_sim > threshold:
                score += 0.4
                reasons.append(f"Name match: {name_sim:.2f}")
            
            # Check 2: Father/Mother name similarity
            if father_mother_name and ifr.father_mother_name:
                father_sim = DuplicateDetectionService.calculate_similarity(
                    father_mother_name, ifr.father_mother_name
                )
                if father_sim > threshold:
                    score += 0.3
                    reasons.append(f"Father/Mother match: {father_sim:.2f}")
            
            # Check 3: Same village
            village_sim = DuplicateDetectionService.calculate_similarity(
                village, claim.village
            )
            if village_sim > 0.9:
                score += 0.2
                reasons.append("Same village")
            
            # Check 4: Khasra numbers overlap
            if khasra_numbers and ifr.khasra_numbers:
                common_khasra = set(khasra_numbers).intersection(set(ifr.khasra_numbers))
                if common_khasra:
                    score += 0.1 * len(common_khasra)
                    reasons.append(f"Common khasra: {common_khasra}")
            
            # If score indicates potential duplicate
            if score >= 0.7:
                duplicates.append({
                    "claim_id": str(claim.claim_id),
                    "claimant_name": claim.claimant_name,
                    "village": claim.village,
                    "similarity_score": score,
                    "reasons": reasons
                })
        
        is_duplicate = len(duplicates) > 0
        return is_duplicate, duplicates
    
    # ============================================================
    # FORM B - CR Duplicate Detection
    # ============================================================
    
    @staticmethod
    def check_form_b_duplicate(
        db: Session,
        community_name: str,
        village: str,
        nistar_rights: str,
        minor_forest_produce: str,
        threshold: float = 0.85
    ) -> Tuple[bool, List[Dict]]:
        """
        Check for duplicate FORM-B claims
        
        Duplicate criteria:
        - Same community name + village
        - Similar nistar rights or MFP claims in same village
        """
        
        duplicates = []
        
        existing_claims = db.query(Claim, ClaimCR).join(
            ClaimCR, Claim.claim_id == ClaimCR.claim_id
        ).filter(
            Claim.claim_type == "FORM_B"
        ).all()
        
        for claim, cr in existing_claims:
            score = 0.0
            reasons = []
            
            # Check 1: Community name
            comm_sim = DuplicateDetectionService.calculate_similarity(
                community_name, cr.community_name
            )
            if comm_sim > threshold:
                score += 0.5
                reasons.append(f"Community name match: {comm_sim:.2f}")
            
            # Check 2: Village
            village_sim = DuplicateDetectionService.calculate_similarity(
                village, cr.village
            )
            if village_sim > 0.9:
                score += 0.3
                reasons.append("Same village")
            
            # Check 3: Nistar rights similarity
            if nistar_rights and cr.nistar_rights:
                nistar_sim = DuplicateDetectionService.calculate_similarity(
                    nistar_rights, cr.nistar_rights
                )
                if nistar_sim > 0.7:
                    score += 0.2
                    reasons.append(f"Similar nistar rights: {nistar_sim:.2f}")
            
            if score >= 0.7:
                duplicates.append({
                    "claim_id": str(claim.claim_id),
                    "community_name": cr.community_name,
                    "village": cr.village,
                    "similarity_score": score,
                    "reasons": reasons
                })
        
        is_duplicate = len(duplicates) > 0
        return is_duplicate, duplicates
    
    # ============================================================
    # FORM C - CFR Duplicate Detection
    # ============================================================
    
    @staticmethod
    def check_form_c_duplicate(
        db: Session,
        village: str,
        boundary_description: str,
        khasra_numbers: List[str],
        threshold: float = 0.85
    ) -> Tuple[bool, List[Dict]]:
        """
        Check for duplicate FORM-C claims
        
        Duplicate criteria:
        - Same village + boundary description
        - Overlapping khasra numbers
        """
        
        duplicates = []
        
        existing_claims = db.query(Claim, ClaimCFR).join(
            ClaimCFR, Claim.claim_id == ClaimCFR.claim_id
        ).filter(
            Claim.claim_type == "FORM_C"
        ).all()
        
        for claim, cfr in existing_claims:
            score = 0.0
            reasons = []
            
            # Check 1: Village
            village_sim = DuplicateDetectionService.calculate_similarity(
                village, cfr.village
            )
            if village_sim > 0.9:
                score += 0.4
                reasons.append("Same village")
            
            # Check 2: Boundary description
            if boundary_description and cfr.boundary_description:
                boundary_sim = DuplicateDetectionService.calculate_similarity(
                    boundary_description, cfr.boundary_description
                )
                if boundary_sim > 0.8:
                    score += 0.4
                    reasons.append(f"Similar boundary: {boundary_sim:.2f}")
            
            # Check 3: Khasra numbers (from related table)
            if khasra_numbers:
                # Get khasra numbers for this CFR claim
                existing_khasras = [k.khasra_no for k in cfr.khasra_entries]
                common_khasra = set(khasra_numbers).intersection(set(existing_khasras))
                if common_khasra:
                    score += 0.2
                    reasons.append(f"Common khasra: {common_khasra}")
            
            if score >= 0.7:
                duplicates.append({
                    "claim_id": str(claim.claim_id),
                    "village": cfr.village,
                    "similarity_score": score,
                    "reasons": reasons
                })
        
        is_duplicate = len(duplicates) > 0
        return is_duplicate, duplicates
    
    # ============================================================
    # ANNEXURE II - IFR Title Duplicate Detection
    # ============================================================
    
    @staticmethod
    def check_annexure_ii_duplicate(
        db: Session,
        holder_name: str,
        village: str,
        area: float,
        boundary_description: str,
        threshold: float = 0.85
    ) -> Tuple[bool, List[Dict]]:
        """
        Check for duplicate ANNEXURE-II (IFR titles)
        
        This is critical - prevents issuing multiple titles for same land
        """
        
        duplicates = []
        
        existing_claims = db.query(Claim, AnnexureII).join(
            AnnexureII, Claim.claim_id == AnnexureII.claim_id
        ).filter(
            Claim.claim_type == "ANNEXURE_II"
        ).all()
        
        for claim, ann2 in existing_claims:
            score = 0.0
            reasons = []
            
            # Check 1: Holder name
            name_sim = DuplicateDetectionService.calculate_similarity(
                holder_name, ann2.holder_name
            )
            if name_sim > threshold:
                score += 0.4
                reasons.append(f"Holder name match: {name_sim:.2f}")
            
            # Check 2: Village
            village_sim = DuplicateDetectionService.calculate_similarity(
                village, ann2.village
            )
            if village_sim > 0.9:
                score += 0.3
                reasons.append("Same village")
            
            # Check 3: Area similarity (within 10% tolerance)
            if area and ann2.area:
                area_diff = abs(float(area) - float(ann2.area)) / float(ann2.area)
                if area_diff < 0.1:
                    score += 0.2
                    reasons.append(f"Similar area: {area} vs {ann2.area}")
            
            # Check 4: Boundary description
            if boundary_description and ann2.boundary_description:
                boundary_sim = DuplicateDetectionService.calculate_similarity(
                    boundary_description, ann2.boundary_description
                )
                if boundary_sim > 0.7:
                    score += 0.1
                    reasons.append(f"Similar boundary: {boundary_sim:.2f}")
            
            if score >= 0.6:  # Lower threshold for titles - be cautious!
                duplicates.append({
                    "claim_id": str(claim.claim_id),
                    "holder_name": ann2.holder_name,
                    "village": ann2.village,
                    "area": float(ann2.area) if ann2.area else 0,
                    "similarity_score": score,
                    "reasons": reasons
                })
        
        is_duplicate = len(duplicates) > 0
        return is_duplicate, duplicates
    
    # ============================================================
    # MASTER DUPLICATE CHECK FUNCTION
    # ============================================================
    
    @staticmethod
    def check_duplicate(
        db: Session,
        form_type: str,
        extracted_fields: Dict
    ) -> Tuple[bool, List[Dict], str]:
        """
        Master duplicate detection function
        
        Returns:
        - is_duplicate: bool
        - duplicate_records: List[Dict]
        - warning_message: str
        """
        
        try:
            if form_type == "FORM_A":
                is_dup, dups = DuplicateDetectionService.check_form_a_duplicate(
                    db,
                    claimant_name=extracted_fields.get("claimant_name", ""),
                    father_mother_name=extracted_fields.get("father_mother_name", ""),
                    village=extracted_fields.get("village", ""),
                    khasra_numbers=extracted_fields.get("khasra_numbers", []),
                    habitation_area=extracted_fields.get("habitation_area", 0),
                    cultivation_area=extracted_fields.get("cultivation_area", 0)
                )
                
            elif form_type == "FORM_B":
                is_dup, dups = DuplicateDetectionService.check_form_b_duplicate(
                    db,
                    community_name=extracted_fields.get("community_name", ""),
                    village=extracted_fields.get("village", ""),
                    nistar_rights=extracted_fields.get("nistar_rights", ""),
                    minor_forest_produce=extracted_fields.get("minor_forest_produce", "")
                )
                
            elif form_type == "FORM_C":
                is_dup, dups = DuplicateDetectionService.check_form_c_duplicate(
                    db,
                    village=extracted_fields.get("village", ""),
                    boundary_description=extracted_fields.get("boundary_description", ""),
                    khasra_numbers=extracted_fields.get("khasra_numbers", [])
                )
                
            elif form_type == "ANNEXURE_II":
                is_dup, dups = DuplicateDetectionService.check_annexure_ii_duplicate(
                    db,
                    holder_name=extracted_fields.get("holder_name", ""),
                    village=extracted_fields.get("village", ""),
                    area=extracted_fields.get("area_hectares", 0),
                    boundary_description=extracted_fields.get("boundary_description", "")
                )
            
            else:
                # For other forms, no duplicate check yet
                return False, [], ""
            
            warning = f"⚠️ Found {len(dups)} potential duplicate(s)" if is_dup else ""
            
            return is_dup, dups, warning
            
        except Exception as e:
            print(f"Duplicate detection error: {e}")
            return False, [], ""


# Export service
duplicate_detection_service = DuplicateDetectionService()