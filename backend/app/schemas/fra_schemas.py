from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime
from uuid import UUID


# ============================================================
# BASE SCHEMAS
# ============================================================

class ProcessingResponse(BaseModel):
    success: bool
    message: str
    record_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


# ============================================================
# FAMILY/DEPENDENT SCHEMAS
# ============================================================

class FamilyMemberBase(BaseModel):
    name: str
    age: Optional[int] = None
    relation: Optional[str] = None


class DependentBase(BaseModel):
    name: str
    age: Optional[int] = None
    relation: Optional[str] = None


class GramSabhaMemberBase(BaseModel):
    name: str
    category: Optional[str] = None  # 'ST', 'OTFD'


# ============================================================
# FORM A (IFR) SCHEMAS
# ============================================================

class FormAExtractedFields(BaseModel):
    claimant_name: Optional[str] = None
    spouse_name: Optional[str] = None
    father_mother_name: Optional[str] = None
    address: Optional[str] = None
    village: Optional[str] = None
    gram_panchayat: Optional[str] = None
    tehsil: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    is_scheduled_tribe: Optional[bool] = None
    is_otfd: Optional[bool] = None
    family_members: List[FamilyMemberBase] = []
    habitation_area: Optional[float] = None
    cultivation_area: Optional[float] = None
    disputed_lands: Optional[str] = None
    pattas_or_leases: Optional[str] = None
    rehabilitation_land: Optional[str] = None
    displacement_details: Optional[str] = None
    forest_village_extent: Optional[str] = None
    other_traditional_rights: Optional[str] = None
    evidence_list: List[str] = []
    khasra_numbers: List[str] = []
    geo_boundary_text: Optional[str] = None


# ============================================================
# FORM B (CR) SCHEMAS
# ============================================================

class FormBExtractedFields(BaseModel):
    community_name: Optional[str] = None
    village: Optional[str] = None
    gram_panchayat: Optional[str] = None
    tehsil: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    is_fdst: Optional[bool] = None
    is_otfd: Optional[bool] = None
    nistar_rights: Optional[str] = None
    minor_forest_produce: Optional[str] = None
    community_uses: Optional[str] = None
    grazing: Optional[str] = None
    pastoral_access: Optional[str] = None
    habitat_rights: Optional[str] = None
    biodiversity_access: Optional[str] = None
    other_traditional_rights: Optional[str] = None
    evidence_list: List[str] = []
    khasra_numbers: List[str] = []
    boundary_description: Optional[str] = None


# ============================================================
# FORM C (CFR) SCHEMAS
# ============================================================

class FormCExtractedFields(BaseModel):
    village: Optional[str] = None
    gram_panchayat: Optional[str] = None
    tehsil: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    gram_sabha_member_list: List[GramSabhaMemberBase] = []
    cfr_map_attached: Optional[bool] = None
    khasra_numbers: List[str] = []
    bordering_villages: List[str] = []
    boundary_description: Optional[str] = None
    evidence_list: List[str] = []
    geojson_extracted: Optional[Dict] = None


# ============================================================
# ANNEXURE II (IFR TITLE) SCHEMAS
# ============================================================

class AnnexureIIExtractedFields(BaseModel):
    holder_name: Optional[str] = None
    spouse_name: Optional[str] = None
    father_mother_name: Optional[str] = None
    dependents: List[DependentBase] = []
    address: Optional[str] = None
    village: Optional[str] = None
    gram_panchayat: Optional[str] = None
    tehsil: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    is_st_or_otfd: Optional[str] = None
    area_hectares: Optional[float] = None
    boundary_description: Optional[str] = None
    khasra_numbers: List[str] = []
    signed_by: List[str] = []


# ============================================================
# ANNEXURE III (CR TITLE) SCHEMAS
# ============================================================

class AnnexureIIIExtractedFields(BaseModel):
    holders_list: Optional[str] = None
    village: Optional[str] = None
    gram_panchayat: Optional[str] = None
    tehsil: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    community_type: Optional[str] = None
    nature_of_rights: Optional[str] = None
    conditions: Optional[str] = None
    boundary_description: Optional[str] = None
    khasra_numbers: List[str] = []
    signed_by: List[str] = []


# ============================================================
# ANNEXURE IV (CFR TITLE) SCHEMAS
# ============================================================

class AnnexureIVExtractedFields(BaseModel):
    village: Optional[str] = None
    gram_panchayat: Optional[str] = None
    tehsil: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    community_type: Optional[str] = None
    boundary_description: Optional[str] = None
    forest_area_hectares: Optional[float] = None
    khasra_numbers: List[str] = []
    signed_by: List[str] = []


# ============================================================
# ANNEXURE V (QUARTERLY REPORT) SCHEMAS
# ============================================================

class AnnexureVExtractedFields(BaseModel):
    state: Optional[str] = None
    report_period: Optional[str] = None
    individual_filed: Optional[int] = None
    individual_accepted: Optional[int] = None
    individual_rejected: Optional[int] = None
    individual_pending: Optional[int] = None
    individual_area_ha: Optional[float] = None
    rejection_reasons_individual: Optional[str] = None
    community_filed: Optional[int] = None
    community_accepted: Optional[int] = None
    community_rejected: Optional[int] = None
    community_pending: Optional[int] = None
    community_area_ha: Optional[float] = None
    rejection_reasons_community: Optional[str] = None
    corrective_measures: Optional[str] = None
    observations: Optional[str] = None
    good_practices: Optional[str] = None
    cfr_management_details: Optional[str] = None
    area_diverted_sec3_2: Optional[float] = None


# ============================================================
# RESPONSE SCHEMAS
# ============================================================

class ClaimRecordResponse(BaseModel):
    claim_id: str
    form_type: str
    claimant_name: Optional[str]
    village: Optional[str]
    district: Optional[str]
    state: Optional[str]
    status: str
    duplicate_flag: bool
    created_at: Optional[str]
    
    class Config:
        from_attributes = True


class ClaimDetailResponse(BaseModel):
    claim_id: str
    form_type: str
    claimant_name: Optional[str]
    village: Optional[str]
    gram_panchayat: Optional[str]
    tehsil: Optional[str]
    district: Optional[str]
    state: Optional[str]
    status: str
    duplicate_flag: bool
    language: str
    created_at: Optional[str]
    form_specific_data: Dict[str, Any]
    
    class Config:
        from_attributes = True


class DuplicateWarning(BaseModel):
    claim_id: str
    claimant_name: Optional[str]
    village: Optional[str]
    similarity_score: float
    reasons: List[str]


class NERResult(BaseModel):
    form_type: str
    extracted_fields: Dict[str, Any]
    extracted_text: str
    is_duplicate: bool
    duplicate_records: List[DuplicateWarning] = []


class StatsResponse(BaseModel):
    total_records: int
    by_form_type: Dict[str, int]
    duplicates_flagged: int