from .fra_schemas import (
    ProcessingResponse,
    FamilyMemberBase,
    DependentBase,
    GramSabhaMemberBase,
    FormAExtractedFields,
    FormBExtractedFields,
    FormCExtractedFields,
    AnnexureIIExtractedFields,
    AnnexureIIIExtractedFields,
    AnnexureIVExtractedFields,
    AnnexureVExtractedFields,
    ClaimRecordResponse,
    ClaimDetailResponse,
    DuplicateWarning,
    NERResult,
    StatsResponse
)

# Create aliases for compatibility
FRARecord = ClaimRecordResponse
FRARecordDetail = ClaimDetailResponse

__all__ = [
    'ProcessingResponse',
    'FRARecord',
    'FRARecordDetail',
    'FamilyMemberBase',
    'DependentBase',
    'GramSabhaMemberBase',
    'FormAExtractedFields',
    'FormBExtractedFields',
    'FormCExtractedFields',
    'AnnexureIIExtractedFields',
    'AnnexureIIIExtractedFields',
    'AnnexureIVExtractedFields',
    'AnnexureVExtractedFields',
    'ClaimRecordResponse',
    'ClaimDetailResponse',
    'DuplicateWarning',
    'NERResult',
    'StatsResponse'
]