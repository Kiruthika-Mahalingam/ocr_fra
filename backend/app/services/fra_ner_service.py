import google.generativeai as genai
import json
import time
from typing import Dict, Optional
from ..config import settings


class FRANERService:
    """
    Form-specific NER service for FRA documents.
    Detects form type and extracts fields accordingly.
    """
    
    def __init__(self):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("models/gemini-2.5-flash")
            self.last_request_time = 0
            self.min_request_interval = 1.0
            print("✓ FRA NER service initialized")
        except Exception as e:
            print(f"WARNING: FRA NER initialization failed: {e}")
            self.model = None

    def _rate_limit(self):
        """Ensure minimum time between API requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

    async def detect_form_type(self, extracted_text: str) -> str:
        """Detect which FRA form this document is"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        self._rate_limit()
        
        try:
            prompt = f"""
            Analyze this FRA document and identify which form type it is.
            
            TEXT:
            {extracted_text[:2000]}  # First 2000 chars for form detection
            
            Return ONLY a JSON object in this exact format:
            {{
                "form_type": "FORM_A" or "FORM_B" or "FORM_C" or "ANNEXURE_II" or "ANNEXURE_III" or "ANNEXURE_IV" or "ANNEXURE_V",
                "confidence": 0.0-1.0,
                "reasoning": "brief explanation"
            }}
            
            FORM IDENTIFICATION RULES:
            - FORM_A: Individual Forest Rights claim form, mentions claimant name, spouse, father/mother, habitation area, cultivation area
            - FORM_B: Community Rights form, mentions community/gram sabha, nistar rights, minor forest produce, grazing
            - FORM_C: Community Forest Resource claim, mentions gram sabha members list, CFR boundaries, khasra numbers
            - ANNEXURE_II: Title for individual forest land, has "holder(s) of forest rights", area in hectares, boundary description
            - ANNEXURE_III: Title for community forest rights, mentions "community forest right", nature of rights
            - ANNEXURE_IV: Title for CFR, mentions "community forest resources", protection/regeneration/conservation rights
            - ANNEXURE_V: Quarterly monitoring report, has statistics like filed/accepted/rejected claims, state-level data
            
            Return ONLY valid JSON, no explanations.
            """
            
            response = await self.model.generate_content_async(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            result = json.loads(raw)
            
            return result.get("form_type", "UNKNOWN")
            
        except Exception as e:
            print(f"Form detection error: {e}")
            return "UNKNOWN"

    # ============================================================
    # FORM A - Individual Forest Rights (IFR)
    # ============================================================
    
    async def extract_form_a(self, extracted_text: str) -> Dict:
        """Extract NER fields from FORM-A"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        self._rate_limit()
        
        try:
            prompt = f"""
            Extract structured information from this FORM-A (Individual Forest Rights) document.
            
            TEXT:
            {extracted_text}
            
            Return ONLY a valid JSON object with this exact structure:
            {{
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
                "family_members": [
                    {{"name": "", "age": 0, "relation": ""}}
                ],
                "habitation_area": 0.0,
                "cultivation_area": 0.0,
                "disputed_lands": "",
                "pattas_or_leases": "",
                "rehabilitation_land": "",
                "displacement_details": "",
                "forest_village_extent": "",
                "other_traditional_rights": "",
                "evidence_list": [],
                "khasra_numbers": [],
                "geo_boundary_text": ""
            }}
            
            IMPORTANT:
            - Extract exact values from the document
            - For boolean fields, use true/false/null
            - For numeric fields, extract as numbers (not strings)
            - If a field is missing, use empty string, empty array, or null
            - Return ONLY JSON, no markdown, no explanations
            """
            
            response = await self.model.generate_content_async(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(raw)
            
        except Exception as e:
            print(f"FORM-A extraction error: {e}")
            return {}

    # ============================================================
    # FORM B - Community Rights (CR)
    # ============================================================
    
    async def extract_form_b(self, extracted_text: str) -> Dict:
        """Extract NER fields from FORM-B"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        self._rate_limit()
        
        try:
            prompt = f"""
            Extract structured information from this FORM-B (Community Rights) document.
            
            TEXT:
            {extracted_text}
            
            Return ONLY a valid JSON object:
            {{
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
                "pastoral_access": "",
                "habitat_rights": "",
                "biodiversity_access": "",
                "other_traditional_rights": "",
                "evidence_list": [],
                "khasra_numbers": [],
                "boundary_description": ""
            }}
            
            Return ONLY JSON, no explanations.
            """
            
            response = await self.model.generate_content_async(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(raw)
            
        except Exception as e:
            print(f"FORM-B extraction error: {e}")
            return {}

    # ============================================================
    # FORM C - Community Forest Resource (CFR)
    # ============================================================
    
    async def extract_form_c(self, extracted_text: str) -> Dict:
        """Extract NER fields from FORM-C"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        self._rate_limit()
        
        try:
            prompt = f"""
            Extract structured information from this FORM-C (Community Forest Resource) document.
            
            TEXT:
            {extracted_text}
            
            Return ONLY a valid JSON object:
            {{
                "village": "",
                "gram_panchayat": "",
                "tehsil": "",
                "district": "",
                "state": "",
                "gram_sabha_member_list": [
                    {{"name": "", "category": "ST"}}
                ],
                "cfr_map_attached": true/false/null,
                "khasra_numbers": [],
                "bordering_villages": [],
                "boundary_description": "",
                "evidence_list": [],
                "geojson_extracted": null
            }}
            
            Return ONLY JSON, no explanations.
            """
            
            response = await self.model.generate_content_async(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(raw)
            
        except Exception as e:
            print(f"FORM-C extraction error: {e}")
            return {}

    # ============================================================
    # ANNEXURE II - IFR Title
    # ============================================================
    
    async def extract_annexure_ii(self, extracted_text: str) -> Dict:
        """Extract NER fields from ANNEXURE-II"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        self._rate_limit()
        
        try:
            prompt = f"""
            Extract structured information from this ANNEXURE-II (IFR Title) document.
            
            TEXT:
            {extracted_text}
            
            Return ONLY a valid JSON object:
            {{
                "holder_name": "",
                "spouse_name": "",
                "father_mother_name": "",
                "dependents": [
                    {{"name": "", "age": 0, "relation": ""}}
                ],
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
            }}
            
            Return ONLY JSON, no explanations.
            """
            
            response = await self.model.generate_content_async(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(raw)
            
        except Exception as e:
            print(f"ANNEXURE-II extraction error: {e}")
            return {}

    # ============================================================
    # ANNEXURE III - CR Title
    # ============================================================
    
    async def extract_annexure_iii(self, extracted_text: str) -> Dict:
        """Extract NER fields from ANNEXURE-III"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        self._rate_limit()
        
        try:
            prompt = f"""
            Extract structured information from this ANNEXURE-III (Community Rights Title) document.
            
            TEXT:
            {extracted_text}
            
            Return ONLY a valid JSON object:
            {{
                "holders_list": "",
                "village": "",
                "gram_panchayat": "",
                "tehsil": "",
                "district": "",
                "state": "",
                "community_type": "",
                "nature_of_rights": "",
                "conditions": "",
                "boundary_description": "",
                "khasra_numbers": [],
                "signed_by": []
            }}
            
            Return ONLY JSON, no explanations.
            """
            
            response = await self.model.generate_content_async(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(raw)
            
        except Exception as e:
            print(f"ANNEXURE-III extraction error: {e}")
            return {}

    # ============================================================
    # ANNEXURE IV - CFR Title
    # ============================================================
    
    async def extract_annexure_iv(self, extracted_text: str) -> Dict:
        """Extract NER fields from ANNEXURE-IV"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        self._rate_limit()
        
        try:
            prompt = f"""
            Extract structured information from this ANNEXURE-IV (CFR Title) document.
            
            TEXT:
            {extracted_text}
            
            Return ONLY a valid JSON object:
            {{
                "village": "",
                "gram_panchayat": "",
                "tehsil": "",
                "district": "",
                "state": "",
                "community_type": "",
                "boundary_description": "",
                "forest_area_hectares": 0.0,
                "khasra_numbers": [],
                "signed_by": []
            }}
            
            Return ONLY JSON, no explanations.
            """
            
            response = await self.model.generate_content_async(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(raw)
            
        except Exception as e:
            print(f"ANNEXURE-IV extraction error: {e}")
            return {}

    # ============================================================
    # ANNEXURE V - Quarterly Report
    # ============================================================
    
    async def extract_annexure_v(self, extracted_text: str) -> Dict:
        """Extract NER fields from ANNEXURE-V"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        self._rate_limit()
        
        try:
            prompt = f"""
            Extract structured information from this ANNEXURE-V (Quarterly Monitoring Report) document.
            
            TEXT:
            {extracted_text}
            
            Return ONLY a valid JSON object:
            {{
                "state": "",
                "report_period": "",
                "individual_filed": 0,
                "individual_accepted": 0,
                "individual_rejected": 0,
                "individual_pending": 0,
                "individual_area_ha": 0.0,
                "rejection_reasons_individual": "",
                "community_filed": 0,
                "community_accepted": 0,
                "community_rejected": 0,
                "community_pending": 0,
                "community_area_ha": 0.0,
                "rejection_reasons_community": "",
                "corrective_measures": "",
                "observations": "",
                "good_practices": "",
                "cfr_management_details": "",
                "area_diverted_sec3_2": 0.0
            }}
            
            Return ONLY JSON, no explanations.
            """
            
            response = await self.model.generate_content_async(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(raw)
            
        except Exception as e:
            print(f"ANNEXURE-V extraction error: {e}")
            return {}

    # ============================================================
    # MASTER NER FUNCTION
    # ============================================================
    
    async def perform_ner(self, extracted_text: str) -> Dict:
        """
        Main NER function - detects form type and extracts fields accordingly
        """
        try:
            # Step 1: Detect form type
            form_type = await self.detect_form_type(extracted_text)
            
            print(f"Detected form type: {form_type}")
            
            # Step 2: Extract fields based on form type
            if form_type == "FORM_A":
                extracted_fields = await self.extract_form_a(extracted_text)
            elif form_type == "FORM_B":
                extracted_fields = await self.extract_form_b(extracted_text)
            elif form_type == "FORM_C":
                extracted_fields = await self.extract_form_c(extracted_text)
            elif form_type == "ANNEXURE_II":
                extracted_fields = await self.extract_annexure_ii(extracted_text)
            elif form_type == "ANNEXURE_III":
                extracted_fields = await self.extract_annexure_iii(extracted_text)
            elif form_type == "ANNEXURE_IV":
                extracted_fields = await self.extract_annexure_iv(extracted_text)
            elif form_type == "ANNEXURE_V":
                extracted_fields = await self.extract_annexure_v(extracted_text)
            else:
                extracted_fields = {}
            
            return {
                "form_type": form_type,
                "extracted_fields": extracted_fields
            }
            
        except Exception as e:
            print(f"NER error: {e}")
            return {
                "form_type": "UNKNOWN",
                "extracted_fields": {}
            }


# Create service instance
try:
    fra_ner_service = FRANERService()
except Exception as e:
    print(f"Failed to initialize FRA NER service: {e}")
    fra_ner_service = None