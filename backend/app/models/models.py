from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, Numeric, Integer, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base


# ============================================================
# MASTER TABLE
# ============================================================

class Claim(Base):
    __tablename__ = "claims"
    
    claim_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_type = Column(String(50), nullable=False, index=True)  # FORM_A, FORM_B, FORM_C, etc.
    claimant_name = Column(Text)
    village = Column(Text, index=True)
    gram_panchayat = Column(Text)
    tehsil = Column(Text)
    district = Column(Text, index=True)
    state = Column(Text, index=True)
    status = Column(String(50), default='pending', index=True)
    summary = Column(JSONB)
    original_pdf_path = Column(Text)
    source_file_minio_path = Column(Text)
    duplicate_flag = Column(Boolean, default=False, index=True)
    processing_level = Column(String(20), default='level1')
    language = Column(String(50), default='english')
    created_at = Column(TIMESTAMP, default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    
    # Relationships
    ocr_records = relationship("OCRRaw", back_populates="claim", cascade="all, delete-orphan")
    ifr = relationship("ClaimIFR", back_populates="claim", uselist=False, cascade="all, delete-orphan")
    cr = relationship("ClaimCR", back_populates="claim", uselist=False, cascade="all, delete-orphan")
    cfr = relationship("ClaimCFR", back_populates="claim", uselist=False, cascade="all, delete-orphan")
    annexure_ii = relationship("AnnexureII", back_populates="claim", uselist=False, cascade="all, delete-orphan")
    annexure_iii = relationship("AnnexureIII", back_populates="claim", uselist=False, cascade="all, delete-orphan")
    annexure_iv = relationship("AnnexureIV", back_populates="claim", uselist=False, cascade="all, delete-orphan")
    evidence = relationship("ClaimEvidence", back_populates="claim", cascade="all, delete-orphan")
    history = relationship("ClaimHistory", back_populates="claim", cascade="all, delete-orphan")


# ============================================================
# OCR STORAGE
# ============================================================

class OCRRaw(Base):
    __tablename__ = "ocr_raw"
    
    ocr_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'))
    source_minio_path = Column(Text)
    raw_text = Column(Text)
    extracted_fields = Column(JSONB)
    confidences = Column(JSONB)
    created_at = Column(TIMESTAMP, default=func.now())
    
    claim = relationship("Claim", back_populates="ocr_records")


# ============================================================
# FORM A (Individual Forest Rights - IFR)
# ============================================================

class ClaimIFR(Base):
    __tablename__ = "claim_ifr"
    
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'), primary_key=True)
    spouse_name = Column(Text)
    father_mother_name = Column(Text)
    is_scheduled_tribe = Column(Boolean)
    is_otfd = Column(Boolean)
    address = Column(Text)
    habitation_area = Column(Numeric)
    cultivation_area = Column(Numeric)
    disputed_lands = Column(Text)
    pattas_or_leases = Column(Text)
    rehabilitation_land = Column(Text)
    displacement_details = Column(Text)
    forest_village_extent = Column(Text)
    other_traditional_rights = Column(Text)
    evidence_list = Column(JSONB)
    khasra_numbers = Column(ARRAY(Text))
    geo_boundary_text = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())
    
    claim = relationship("Claim", back_populates="ifr")
    family_members = relationship("ClaimIFRFamily", back_populates="ifr", cascade="all, delete-orphan")


class ClaimIFRFamily(Base):
    __tablename__ = "claim_ifr_family"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claim_ifr.claim_id', ondelete='CASCADE'))
    name = Column(Text, nullable=False)
    age = Column(Integer)
    relation = Column(Text)
    
    ifr = relationship("ClaimIFR", back_populates="family_members")


# ============================================================
# FORM B (Community Rights - CR)
# ============================================================

class ClaimCR(Base):
    __tablename__ = "claim_cr"
    
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'), primary_key=True)
    community_name = Column(Text, index=True)
    village = Column(Text)
    gram_panchayat = Column(Text)
    tehsil = Column(Text)
    district = Column(Text)
    is_st = Column(Boolean)
    is_otfd = Column(Boolean)
    nistar_rights = Column(Text)
    minor_forest_produce = Column(Text)
    community_uses = Column(Text)
    grazing = Column(Text)
    pastoral_access = Column(Text)
    habitat_rights = Column(Text)
    biodiversity_access = Column(Text)
    other_traditional_rights = Column(Text)
    evidence_list = Column(JSONB)
    khasra_numbers = Column(ARRAY(Text))
    boundary_description = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())
    
    claim = relationship("Claim", back_populates="cr")


# ============================================================
# FORM C (Community Forest Resource - CFR)
# ============================================================

class ClaimCFR(Base):
    __tablename__ = "claim_cfr"
    
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'), primary_key=True)
    village = Column(Text)
    gram_panchayat = Column(Text)
    tehsil = Column(Text)
    district = Column(Text)
    cfr_map_present = Column(Boolean)
    boundary_description = Column(Text)
    evidence_list = Column(JSONB)
    created_at = Column(TIMESTAMP, default=func.now())
    
    claim = relationship("Claim", back_populates="cfr")
    khasra_entries = relationship("ClaimCFRKhasra", back_populates="cfr", cascade="all, delete-orphan")
    neighbors = relationship("ClaimCFRNeighbors", back_populates="cfr", cascade="all, delete-orphan")
    members = relationship("ClaimCFRMembers", back_populates="cfr", cascade="all, delete-orphan")
    boundaries = relationship("CFRBoundaries", back_populates="cfr", cascade="all, delete-orphan")
    geo_shapes = relationship("GeoCFRShapes", back_populates="cfr", cascade="all, delete-orphan")


class ClaimCFRKhasra(Base):
    __tablename__ = "claim_cfr_khasra"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claim_cfr.claim_id', ondelete='CASCADE'))
    khasra_no = Column(Text)
    
    cfr = relationship("ClaimCFR", back_populates="khasra_entries")


class ClaimCFRNeighbors(Base):
    __tablename__ = "claim_cfr_neighbors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claim_cfr.claim_id', ondelete='CASCADE'))
    neighboring_village = Column(Text)
    
    cfr = relationship("ClaimCFR", back_populates="neighbors")


class ClaimCFRMembers(Base):
    __tablename__ = "claim_cfr_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claim_cfr.claim_id', ondelete='CASCADE'))
    name = Column(Text)
    category = Column(Text)  # 'ST', 'OTFD'
    
    cfr = relationship("ClaimCFR", back_populates="members")


class CFRBoundaries(Base):
    __tablename__ = "cfr_boundaries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claim_cfr.claim_id', ondelete='CASCADE'))
    boundary_minio_path = Column(Text)
    
    cfr = relationship("ClaimCFR", back_populates="boundaries")


# ============================================================
# ANNEXURE II (IFR Title)
# ============================================================

class AnnexureII(Base):
    __tablename__ = "annexure_ii"
    
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'), primary_key=True)
    holder_name = Column(Text)
    father_mother_name = Column(Text)
    address = Column(Text)
    village = Column(Text)
    gram_panchayat = Column(Text)
    tehsil = Column(Text)
    district = Column(Text)
    is_st_or_otfd = Column(Text)
    area = Column(Numeric)
    boundary_description = Column(Text)
    khasra_numbers = Column(ARRAY(Text))
    signed_by = Column(JSONB)
    created_at = Column(TIMESTAMP, default=func.now())
    
    claim = relationship("Claim", back_populates="annexure_ii")
    dependents = relationship("AnnexureIIDependents", back_populates="annexure", cascade="all, delete-orphan")


class AnnexureIIDependents(Base):
    __tablename__ = "annexure_ii_dependents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('annexure_ii.claim_id', ondelete='CASCADE'))
    name = Column(Text)
    age = Column(Integer)
    relation = Column(Text)
    
    annexure = relationship("AnnexureII", back_populates="dependents")


# ============================================================
# ANNEXURE III (CR Title)
# ============================================================

class AnnexureIII(Base):
    __tablename__ = "annexure_iii"
    
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'), primary_key=True)
    holders = Column(Text)
    village = Column(Text)
    gram_panchayat = Column(Text)
    tehsil = Column(Text)
    district = Column(Text)
    community_type = Column(Text)
    nature_of_rights = Column(Text)
    conditions = Column(Text)
    boundary_description = Column(Text)
    khasra_numbers = Column(ARRAY(Text))
    signed_by = Column(JSONB)
    created_at = Column(TIMESTAMP, default=func.now())
    
    claim = relationship("Claim", back_populates="annexure_iii")


# ============================================================
# ANNEXURE IV (CFR Title)
# ============================================================

class AnnexureIV(Base):
    __tablename__ = "annexure_iv"
    
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'), primary_key=True)
    village = Column(Text)
    gram_panchayat = Column(Text)
    tehsil = Column(Text)
    district = Column(Text)
    community_type = Column(Text)
    boundary_description = Column(Text)
    forest_area_hectares = Column(Numeric)
    khasra_numbers = Column(ARRAY(Text))
    created_at = Column(TIMESTAMP, default=func.now())
    
    claim = relationship("Claim", back_populates="annexure_iv")
    signatories = relationship("AnnexureIVSignatories", back_populates="annexure", cascade="all, delete-orphan")


class AnnexureIVSignatories(Base):
    __tablename__ = "annexure_iv_signatories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('annexure_iv.claim_id', ondelete='CASCADE'))
    signed_by = Column(Text)
    
    annexure = relationship("AnnexureIV", back_populates="signatories")


# ============================================================
# ANNEXURE V (Quarterly Report)
# ============================================================

class QuarterlyReport(Base):
    __tablename__ = "quarterly_report"
    
    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state = Column(Text, index=True)
    period_start = Column(TIMESTAMP)
    period_end = Column(TIMESTAMP)
    
    individual_filed = Column(Integer)
    individual_accepted = Column(Integer)
    individual_rejected = Column(Integer)
    individual_pending = Column(Integer)
    individual_area_ha = Column(Numeric)
    rejection_reasons_individual = Column(Text)
    
    community_filed = Column(Integer)
    community_accepted = Column(Integer)
    community_rejected = Column(Integer)
    community_pending = Column(Integer)
    community_area_ha = Column(Numeric)
    rejection_reasons_community = Column(Text)
    
    observations = Column(Text)
    corrective_measures = Column(Text)
    good_practices = Column(Text)
    cfr_management_details = Column(Text)
    area_diverted_sec3_2 = Column(Numeric)
    created_at = Column(TIMESTAMP, default=func.now())


# ============================================================
# EVIDENCE STORAGE
# ============================================================

class ClaimEvidence(Base):
    __tablename__ = "claim_evidence"
    
    evidence_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'))
    evidence_type = Column(String(50))
    minio_path = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())
    
    claim = relationship("Claim", back_populates="evidence")


# ============================================================
# CLAIM HISTORY (Audit Trail)
# ============================================================

class ClaimHistory(Base):
    __tablename__ = "claim_history"
    
    history_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'))
    previous_status = Column(String(50))
    new_status = Column(String(50))
    changed_by = Column(Text)
    changed_at = Column(TIMESTAMP, default=func.now())
    remarks = Column(Text)
    
    claim = relationship("Claim", back_populates="history")


# ============================================================
# GEO SHAPES
# ============================================================

class GeoCFRShapes(Base):
    __tablename__ = "geo_cfr_shapes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claim_cfr.claim_id', ondelete='CASCADE'))
    geojson = Column(JSONB)
    created_at = Column(TIMESTAMP, default=func.now())
    
    cfr = relationship("ClaimCFR", back_populates="geo_shapes")


class GeoAssets(Base):
    __tablename__ = "geo_assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey('claims.claim_id', ondelete='CASCADE'))
    asset_type = Column(String(50))
    geometry = Column(JSONB)
    confidence = Column(Numeric)
    
    # No direct relationship to keep it flexible