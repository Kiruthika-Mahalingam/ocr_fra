-- ============================================================
-- FRA DIGITIZATION DATABASE SCHEMA
-- Version 1.0 - Complete Implementation
-- ============================================================

-- Create database
CREATE DATABASE fra_db;
\c fra_db;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- MASTER TABLE (Core Claims Table)
-- ============================================================

CREATE TABLE claims (
    claim_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_type VARCHAR(50) NOT NULL, -- 'FORM_A', 'FORM_B', 'FORM_C', 'ANNEXURE_II', 'ANNEXURE_III', 'ANNEXURE_IV', 'ANNEXURE_V'
    claimant_name TEXT,
    village TEXT,
    gram_panchayat TEXT,
    tehsil TEXT,
    district TEXT,
    state TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'accepted', 'rejected', 'under_review'
    summary JSONB, -- Quick summary of claim for fast queries
    original_pdf_path TEXT,
    source_file_minio_path TEXT,
    duplicate_flag BOOLEAN DEFAULT FALSE,
    processing_level VARCHAR(20) DEFAULT 'level1', -- 'level1', 'level2', 'level3', 'level4'
    language VARCHAR(50) DEFAULT 'english',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for master table
CREATE INDEX idx_claims_type ON claims(claim_type);
CREATE INDEX idx_claims_village ON claims(village);
CREATE INDEX idx_claims_district ON claims(district);
CREATE INDEX idx_claims_state ON claims(state);
CREATE INDEX idx_claims_status ON claims(status);
CREATE INDEX idx_claims_duplicate ON claims(duplicate_flag);
CREATE INDEX idx_claims_created_at ON claims(created_at);

-- ============================================================
-- OCR STORAGE
-- ============================================================

CREATE TABLE ocr_raw (
    ocr_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(claim_id) ON DELETE CASCADE,
    source_minio_path TEXT,
    raw_text TEXT,
    extracted_fields JSONB,
    confidences JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ocr_claim_id ON ocr_raw(claim_id);

-- ============================================================
-- FORM A (Individual Forest Rights - IFR)
-- ============================================================

CREATE TABLE claim_ifr (
    claim_id UUID PRIMARY KEY REFERENCES claims(claim_id) ON DELETE CASCADE,
    spouse_name TEXT,
    father_mother_name TEXT,
    is_scheduled_tribe BOOLEAN,
    is_otfd BOOLEAN,
    address TEXT,
    habitation_area NUMERIC,
    cultivation_area NUMERIC,
    disputed_lands TEXT,
    pattas_or_leases TEXT,
    rehabilitation_land TEXT,
    displacement_details TEXT,
    forest_village_extent TEXT,
    other_traditional_rights TEXT,
    evidence_list JSONB,
    khasra_numbers TEXT[],
    geo_boundary_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE claim_ifr_family (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claim_ifr(claim_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    age INTEGER,
    relation TEXT
);

CREATE INDEX idx_ifr_claim_id ON claim_ifr(claim_id);
CREATE INDEX idx_ifr_family_claim_id ON claim_ifr_family(claim_id);

-- ============================================================
-- FORM B (Community Rights - CR)
-- ============================================================

CREATE TABLE claim_cr (
    claim_id UUID PRIMARY KEY REFERENCES claims(claim_id) ON DELETE CASCADE,
    community_name TEXT,
    village TEXT,
    gram_panchayat TEXT,
    tehsil TEXT,
    district TEXT,
    is_st BOOLEAN,
    is_otfd BOOLEAN,
    nistar_rights TEXT,
    minor_forest_produce TEXT,
    community_uses TEXT,
    grazing TEXT,
    pastoral_access TEXT,
    habitat_rights TEXT,
    biodiversity_access TEXT,
    other_traditional_rights TEXT,
    evidence_list JSONB,
    khasra_numbers TEXT[],
    boundary_description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cr_claim_id ON claim_cr(claim_id);
CREATE INDEX idx_cr_community_name ON claim_cr(community_name);

-- ============================================================
-- FORM C (Community Forest Resource - CFR)
-- ============================================================

CREATE TABLE claim_cfr (
    claim_id UUID PRIMARY KEY REFERENCES claims(claim_id) ON DELETE CASCADE,
    village TEXT,
    gram_panchayat TEXT,
    tehsil TEXT,
    district TEXT,
    cfr_map_present BOOLEAN,
    boundary_description TEXT,
    evidence_list JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE claim_cfr_khasra (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claim_cfr(claim_id) ON DELETE CASCADE,
    khasra_no TEXT
);

CREATE TABLE claim_cfr_neighbors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claim_cfr(claim_id) ON DELETE CASCADE,
    neighboring_village TEXT
);

CREATE TABLE claim_cfr_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claim_cfr(claim_id) ON DELETE CASCADE,
    name TEXT,
    category TEXT -- 'ST', 'OTFD'
);

CREATE TABLE cfr_boundaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claim_cfr(claim_id) ON DELETE CASCADE,
    boundary_minio_path TEXT
);

CREATE INDEX idx_cfr_claim_id ON claim_cfr(claim_id);
CREATE INDEX idx_cfr_khasra_claim_id ON claim_cfr_khasra(claim_id);
CREATE INDEX idx_cfr_neighbors_claim_id ON claim_cfr_neighbors(claim_id);

-- ============================================================
-- ANNEXURE II (IFR Title Issued)
-- ============================================================

CREATE TABLE annexure_ii (
    claim_id UUID PRIMARY KEY REFERENCES claims(claim_id) ON DELETE CASCADE,
    holder_name TEXT,
    father_mother_name TEXT,
    address TEXT,
    village TEXT,
    gram_panchayat TEXT,
    tehsil TEXT,
    district TEXT,
    is_st_or_otfd TEXT,
    area NUMERIC,
    boundary_description TEXT,
    khasra_numbers TEXT[],
    signed_by JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE annexure_ii_dependents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES annexure_ii(claim_id) ON DELETE CASCADE,
    name TEXT,
    age INTEGER,
    relation TEXT
);

CREATE INDEX idx_annexure_ii_claim_id ON annexure_ii(claim_id);
CREATE INDEX idx_annexure_ii_dependents_claim_id ON annexure_ii_dependents(claim_id);

-- ============================================================
-- ANNEXURE III (Community Title)
-- ============================================================

CREATE TABLE annexure_iii (
    claim_id UUID PRIMARY KEY REFERENCES claims(claim_id) ON DELETE CASCADE,
    holders TEXT,
    village TEXT,
    gram_panchayat TEXT,
    tehsil TEXT,
    district TEXT,
    community_type TEXT,
    nature_of_rights TEXT,
    conditions TEXT,
    boundary_description TEXT,
    khasra_numbers TEXT[],
    signed_by JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_annexure_iii_claim_id ON annexure_iii(claim_id);

-- ============================================================
-- ANNEXURE IV (CFR Title)
-- ============================================================

CREATE TABLE annexure_iv (
    claim_id UUID PRIMARY KEY REFERENCES claims(claim_id) ON DELETE CASCADE,
    village TEXT,
    gram_panchayat TEXT,
    tehsil TEXT,
    district TEXT,
    community_type TEXT,
    boundary_description TEXT,
    forest_area_hectares NUMERIC,
    khasra_numbers TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE annexure_iv_signatories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES annexure_iv(claim_id) ON DELETE CASCADE,
    signed_by TEXT
);

CREATE INDEX idx_annexure_iv_claim_id ON annexure_iv(claim_id);
CREATE INDEX idx_annexure_iv_signatories_claim_id ON annexure_iv_signatories(claim_id);

-- ============================================================
-- ANNEXURE V (Quarterly Report)
-- ============================================================

CREATE TABLE quarterly_report (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state TEXT,
    period_start DATE,
    period_end DATE,
    
    individual_filed INTEGER,
    individual_accepted INTEGER,
    individual_rejected INTEGER,
    individual_pending INTEGER,
    individual_area_ha NUMERIC,
    rejection_reasons_individual TEXT,
    
    community_filed INTEGER,
    community_accepted INTEGER,
    community_rejected INTEGER,
    community_pending INTEGER,
    community_area_ha NUMERIC,
    rejection_reasons_community TEXT,
    
    observations TEXT,
    corrective_measures TEXT,
    good_practices TEXT,
    cfr_management_details TEXT,
    area_diverted_sec3_2 NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quarterly_report_state ON quarterly_report(state);

-- ============================================================
-- EVIDENCE STORAGE
-- ============================================================

CREATE TABLE claim_evidence (
    evidence_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(claim_id) ON DELETE CASCADE,
    evidence_type VARCHAR(50),
    minio_path TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_evidence_claim_id ON claim_evidence(claim_id);

-- ============================================================
-- CLAIM HISTORY (Audit Trail)
-- ============================================================

CREATE TABLE claim_history (
    history_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(claim_id) ON DELETE CASCADE,
    previous_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_by TEXT,
    changed_at TIMESTAMP DEFAULT NOW(),
    remarks TEXT
);

CREATE INDEX idx_history_claim_id ON claim_history(claim_id);

-- ============================================================
-- GEO SHAPES
-- ============================================================

CREATE TABLE geo_cfr_shapes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claim_cfr(claim_id) ON DELETE CASCADE,
    geojson JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE geo_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(claim_id) ON DELETE CASCADE,
    asset_type VARCHAR(50),
    geometry JSONB,
    confidence NUMERIC
);

CREATE INDEX idx_geo_cfr_claim_id ON geo_cfr_shapes(claim_id);
CREATE INDEX idx_geo_assets_claim_id ON geo_assets(claim_id);

-- ============================================================
-- DUPLICATE DETECTION HELPER VIEW
-- ============================================================

CREATE VIEW duplicate_detection_view AS
SELECT 
    c.claim_id,
    c.claim_type,
    c.claimant_name,
    c.village,
    c.district,
    COALESCE(ifr.khasra_numbers, cr.khasra_numbers, cfr_k.khasra_array) as khasra_numbers,
    COALESCE(ifr.habitation_area + ifr.cultivation_area, 0) as total_area
FROM claims c
LEFT JOIN claim_ifr ifr ON c.claim_id = ifr.claim_id
LEFT JOIN claim_cr cr ON c.claim_id = cr.claim_id
LEFT JOIN (
    SELECT claim_id, ARRAY_AGG(khasra_no) as khasra_array
    FROM claim_cfr_khasra
    GROUP BY claim_id
) cfr_k ON c.claim_id = cfr_k.claim_id;

-- ============================================================
-- TRIGGER: Update timestamp on UPDATE
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_claims_updated_at BEFORE UPDATE ON claims
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- SAMPLE QUERIES FOR DUPLICATE DETECTION
-- ============================================================

-- Find duplicate IFR claims by name + village + khasra
-- SELECT * FROM claims c1
-- WHERE EXISTS (
--     SELECT 1 FROM claims c2
--     WHERE c1.claim_id != c2.claim_id
--     AND c1.claimant_name = c2.claimant_name
--     AND c1.village = c2.village
-- );

COMMENT ON TABLE claims IS 'Master table for all FRA claims';
COMMENT ON TABLE claim_ifr IS 'Form A - Individual Forest Rights claims';
COMMENT ON TABLE claim_cr IS 'Form B - Community Rights claims';
COMMENT ON TABLE claim_cfr IS 'Form C - Community Forest Resource claims';
COMMENT ON TABLE annexure_ii IS 'IFR Title issued documents';
COMMENT ON TABLE annexure_iii IS 'Community Rights Title';
COMMENT ON TABLE annexure_iv IS 'CFR Title';
COMMENT ON TABLE quarterly_report IS 'Annexure V - State-level monitoring reports';