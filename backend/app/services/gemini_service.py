# # # # # # # # import google.generativeai as genai
# # # # # # # # from PIL import Image
# # # # # # # # import io
# # # # # # # # from typing import Dict, Optional
# # # # # # # # from ..config import settings

# # # # # # # # class GeminiService:
# # # # # # # #     def __init__(self):
# # # # # # # #         genai.configure(api_key=settings.GEMINI_API_KEY)
# # # # # # # #         self.model = genai.GenerativeModel('gemini-1.5-flash')
    
# # # # # # # #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# # # # # # # #         """Extract text from image using Gemini Vision"""
# # # # # # # #         try:
# # # # # # # #             image = Image.open(io.BytesIO(image_bytes))
            
# # # # # # # #             prompt = """
# # # # # # # #             Extract all text from this document image. 
# # # # # # # #             Maintain the original structure and formatting.
# # # # # # # #             Return only the extracted text without any additional commentary.
# # # # # # # #             """
            
# # # # # # # #             response = self.model.generate_content([prompt, image])
# # # # # # # #             return response.text
# # # # # # # #         except Exception as e:
# # # # # # # #             raise Exception(f"Error extracting text: {str(e)}")
    
# # # # # # # #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# # # # # # # #         """Extract text from PDF using Gemini"""
# # # # # # # #         try:
# # # # # # # #             # For PDFs, we'll need to convert to images first
# # # # # # # #             from pdf2image import convert_from_path
            
# # # # # # # #             images = convert_from_path(pdf_path)
# # # # # # # #             full_text = []
            
# # # # # # # #             for i, image in enumerate(images):
# # # # # # # #                 img_byte_arr = io.BytesIO()
# # # # # # # #                 image.save(img_byte_arr, format='PNG')
# # # # # # # #                 img_byte_arr = img_byte_arr.getvalue()
                
# # # # # # # #                 text = await self.extract_text_from_image(img_byte_arr)
# # # # # # # #                 full_text.append(f"--- Page {i+1} ---\n{text}")
            
# # # # # # # #             return "\n\n".join(full_text)
# # # # # # # #         except Exception as e:
# # # # # # # #             raise Exception(f"Error processing PDF: {str(e)}")
    
# # # # # # # #     async def perform_ner(self, text: str) -> Dict:
# # # # # # # #         """Perform Named Entity Recognition using Gemini"""
# # # # # # # #         try:
# # # # # # # #             prompt = f"""
# # # # # # # #             Analyze the following FRA (Forest Rights Act) document text and extract named entities.
            
# # # # # # # #             Text: {text}
            
# # # # # # # #             Extract and return a JSON object with the following entities:
# # # # # # # #             - PERSON: Names of patta holders, claimants
# # # # # # # #             - LOCATION: Village names, districts, blocks, states
# # # # # # # #             - CLAIM_NUMBER: Any claim or reference numbers
# # # # # # # #             - CLAIM_TYPE: Type of claim (IFR, CR, CFR)
# # # # # # # #             - SURVEY_NUMBER: Land survey numbers
# # # # # # # #             - AREA: Land area in hectares
# # # # # # # #             - COORDINATES: GPS coordinates if present
# # # # # # # #             - DATE: Any dates mentioned
# # # # # # # #             - STATUS: Claim status (approved, pending, rejected)
            
# # # # # # # #             Return ONLY a valid JSON object in this format:
# # # # # # # #             {{
# # # # # # # #                 "entities": [
# # # # # # # #                     {{"text": "entity text", "label": "ENTITY_TYPE", "start": 0, "end": 10}}
# # # # # # # #                 ],
# # # # # # # #                 "extracted_fields": {{
# # # # # # # #                     "patta_holder_name": "name",
# # # # # # # #                     "village_name": "village",
# # # # # # # #                     "district": "district",
# # # # # # # #                     "state": "state",
# # # # # # # #                     "claim_number": "number",
# # # # # # # #                     "claim_type": "type",
# # # # # # # #                     "survey_number": "survey",
# # # # # # # #                     "area_in_hectares": "area",
# # # # # # # #                     "coordinates": "coords",
# # # # # # # #                     "claim_status": "status"
# # # # # # # #                 }}
# # # # # # # #             }}
# # # # # # # #             """
            
# # # # # # # #             response = self.model.generate_content(prompt)
# # # # # # # #             result_text = response.text.strip()
            
# # # # # # # #             # Remove markdown code blocks if present
# # # # # # # #             if result_text.startswith("```json"):
# # # # # # # #                 result_text = result_text[7:]
# # # # # # # #             if result_text.startswith("```"):
# # # # # # # #                 result_text = result_text[3:]
# # # # # # # #             if result_text.endswith("```"):
# # # # # # # #                 result_text = result_text[:-3]
            
# # # # # # # #             import json
# # # # # # # #             return json.loads(result_text.strip())
# # # # # # # #         except Exception as e:
# # # # # # # #             raise Exception(f"Error performing NER: {str(e)}")

# # # # # # # # gemini_service = GeminiService()


# # # # # # # # import google.generativeai as genai
# # # # # # # # from PIL import Image
# # # # # # # # import io
# # # # # # # # from typing import Dict, Optional
# # # # # # # # from ..config import settings

# # # # # # # # class GeminiService:
# # # # # # # #     def __init__(self):
# # # # # # # #         genai.configure(api_key=settings.GEMINI_API_KEY)

# # # # # # # #         # FIX: Use latest supported model
# # # # # # # #         # self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
# # # # # # # #         self.model = genai.GenerativeModel("gemini-2.5-flash")

    
# # # # # # # #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# # # # # # # #         """Extract text from image using Gemini Vision"""
# # # # # # # #         try:
# # # # # # # #             image = Image.open(io.BytesIO(image_bytes))

# # # # # # # #             prompt = """
# # # # # # # #             Extract all text from this document image.
# # # # # # # #             Maintain the original structure and formatting.
# # # # # # # #             Return only the extracted text without any additional commentary.
# # # # # # # #             """

# # # # # # # #             # FIX: Proper call format for image input
# # # # # # # #             response = self.model.generate_content(
# # # # # # # #                 [prompt, image],
# # # # # # # #             )

# # # # # # # #             return response.text
        
# # # # # # # #         except Exception as e:
# # # # # # # #             raise Exception(f"Error extracting text: {str(e)}")
    
# # # # # # # #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# # # # # # # #         """Extract text from PDF using Gemini"""
# # # # # # # #         try:
# # # # # # # #             from pdf2image import convert_from_path

# # # # # # # #             images = convert_from_path(pdf_path)
# # # # # # # #             full_text = []

# # # # # # # #             for i, image in enumerate(images):
# # # # # # # #                 img_byte_arr = io.BytesIO()
# # # # # # # #                 image.save(img_byte_arr, format='PNG')
# # # # # # # #                 img_bytes = img_byte_arr.getvalue()

# # # # # # # #                 text = await self.extract_text_from_image(img_bytes)
# # # # # # # #                 full_text.append(f"--- Page {i+1} ---\n{text}")

# # # # # # # #             return "\n\n".join(full_text)
        
# # # # # # # #         except Exception as e:
# # # # # # # #             raise Exception(f"Error processing PDF: {str(e)}")
    
# # # # # # # #     async def perform_ner(self, text: str) -> Dict:
# # # # # # # #         """Perform Named Entity Recognition using Gemini"""
# # # # # # # #         try:
# # # # # # # #             prompt = f"""
# # # # # # # #             Analyze the following FRA (Forest Rights Act) document text and extract named entities.

# # # # # # # #             Text: {text}

# # # # # # # #             Extract and return a JSON object with the following entities:
# # # # # # # #             - PERSON: Names of patta holders, claimants
# # # # # # # #             - LOCATION: Village names, districts, blocks, states
# # # # # # # #             - CLAIM_NUMBER: Any claim or reference numbers
# # # # # # # #             - CLAIM_TYPE: Type of claim (IFR, CR, CFR)
# # # # # # # #             - SURVEY_NUMBER: Land survey numbers
# # # # # # # #             - AREA: Land area in hectares
# # # # # # # #             - COORDINATES: GPS coordinates if present
# # # # # # # #             - DATE: Any dates mentioned
# # # # # # # #             - STATUS: Claim status (approved, pending, rejected)

# # # # # # # #             Return ONLY a valid JSON object in this format:
# # # # # # # #             {{
# # # # # # # #                 "entities": [
# # # # # # # #                     {{"text": "entity text", "label": "ENTITY_TYPE", "start": 0, "end": 10}}
# # # # # # # #                 ],
# # # # # # # #                 "extracted_fields": {{
# # # # # # # #                     "patta_holder_name": "name",
# # # # # # # #                     "village_name": "village",
# # # # # # # #                     "district": "district",
# # # # # # # #                     "state": "state",
# # # # # # # #                     "claim_number": "number",
# # # # # # # #                     "claim_type": "type",
# # # # # # # #                     "survey_number": "survey",
# # # # # # # #                     "area_in_hectares": "area",
# # # # # # # #                     "coordinates": "coords",
# # # # # # # #                     "claim_status": "status"
# # # # # # # #                 }}
# # # # # # # #             }}
# # # # # # # #             """

# # # # # # # #             response = self.model.generate_content(prompt)
# # # # # # # #             result_text = response.text.strip()

# # # # # # # #             # Clean markdown wrappers
# # # # # # # #             if result_text.startswith("```json"):
# # # # # # # #                 result_text = result_text[7:]
# # # # # # # #             if result_text.startswith("```"):
# # # # # # # #                 result_text = result_text[3:]
# # # # # # # #             if result_text.endswith("```"):
# # # # # # # #                 result_text = result_text[:-3]

# # # # # # # #             import json
# # # # # # # #             return json.loads(result_text.strip())

# # # # # # # #         except Exception as e:
# # # # # # # #             raise Exception(f"Error performing NER: {str(e)}")

# # # # # # # # gemini_service = GeminiService()



# # # # # # # import google.generativeai as genai
# # # # # # # from PIL import Image
# # # # # # # import io
# # # # # # # from typing import Dict
# # # # # # # from ..config import settings


# # # # # # # class GeminiService:
# # # # # # #     def __init__(self):
# # # # # # #         # Configure API Key
# # # # # # #         genai.configure(api_key=settings.GEMINI_API_KEY)

# # # # # # #         # BEST MODEL FOR OCR + NER
# # # # # # #         self.model = genai.GenerativeModel("models/gemini-2.5-flash-image")

# # # # # # #     # --------------------------------------------------------------------
# # # # # # #     # LEVEL 1 / 2: OCR FROM IMAGE (English / Hindi / Marathi)
# # # # # # #     # --------------------------------------------------------------------
# # # # # # #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# # # # # # #         """Extract text from image using Gemini Vision."""
# # # # # # #         try:
# # # # # # #             image = Image.open(io.BytesIO(image_bytes))

# # # # # # #             prompt = """
# # # # # # #             Extract all text from this document image.
# # # # # # #             - Preserve original formatting
# # # # # # #             - Return ONLY the plain extracted text
# # # # # # #             - No explanation, no metadata
# # # # # # #             """

# # # # # # #             response = self.model.generate_content(
# # # # # # #                 contents=[
# # # # # # #                     prompt,
# # # # # # #                     image
# # # # # # #                 ]
# # # # # # #             )

# # # # # # #             return response.text.strip()

# # # # # # #         except Exception as e:
# # # # # # #             raise Exception(f"Error extracting text: {str(e)}")

# # # # # # #     # --------------------------------------------------------------------
# # # # # # #     # PDF OCR (MULTI-PAGE)
# # # # # # #     # --------------------------------------------------------------------
# # # # # # #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# # # # # # #         """Extract text from PDF by converting pages to images."""
# # # # # # #         try:
# # # # # # #             from pdf2image import convert_from_path

# # # # # # #             images = convert_from_path(pdf_path)
# # # # # # #             full_text = []

# # # # # # #             for i, image in enumerate(images):
# # # # # # #                 img_bytes = io.BytesIO()
# # # # # # #                 image.save(img_bytes, format="PNG")
# # # # # # #                 img_bytes = img_bytes.getvalue()

# # # # # # #                 text = await self.extract_text_from_image(img_bytes)
# # # # # # #                 full_text.append(f"--- PAGE {i+1} ---\n{text}")

# # # # # # #             return "\n\n".join(full_text)

# # # # # # #         except Exception as e:
# # # # # # #             raise Exception(f"Error processing PDF: {str(e)}")

# # # # # # #     # --------------------------------------------------------------------
# # # # # # #     # LEVEL 1/2/3: NER EXTRACTION
# # # # # # #     # --------------------------------------------------------------------
# # # # # # #     async def perform_ner(self, text: str) -> Dict:
# # # # # # #         """Run Gemini NER for FRA fields (English or translated English)."""
# # # # # # #         try:
# # # # # # #             prompt = f"""
# # # # # # #             Perform Named Entity Recognition (NER) on the following FRA document text
# # # # # # #             and extract FRA-related information.

# # # # # # #             TEXT:
# # # # # # #             {text}

# # # # # # #             Return STRICTLY a valid JSON object with:

# # # # # # #             {{
# # # # # # #                 "entities": [
# # # # # # #                     {{
# # # # # # #                         "text": "entity text",
# # # # # # #                         "label": "ENTITY_TYPE",
# # # # # # #                         "start": 0,
# # # # # # #                         "end": 10
# # # # # # #                     }}
# # # # # # #                 ],
# # # # # # #                 "extracted_fields": {{
# # # # # # #                     "patta_holder_name": "",
# # # # # # #                     "village_name": "",
# # # # # # #                     "district": "",
# # # # # # #                     "state": "",
# # # # # # #                     "claim_number": "",
# # # # # # #                     "claim_type": "",
# # # # # # #                     "survey_number": "",
# # # # # # #                     "area_in_hectares": "",
# # # # # # #                     "coordinates": "",
# # # # # # #                     "claim_status": ""
# # # # # # #                 }}
# # # # # # #             }}

# # # # # # #             RULES:
# # # # # # #             - Return ONLY valid JSON
# # # # # # #             - No explanations
# # # # # # #             - No markdown
# # # # # # #             - No comments
# # # # # # #             """

# # # # # # #             response = self.model.generate_content(prompt)
# # # # # # #             result_text = response.text.strip()

# # # # # # #             # CLEAN POSSIBLE MARKDOWN
# # # # # # #             if result_text.startswith("```json"):
# # # # # # #                 result_text = result_text[7:]
# # # # # # #             if result_text.startswith("```"):
# # # # # # #                 result_text = result_text[3:]
# # # # # # #             if result_text.endswith("```"):
# # # # # # #                 result_text = result_text[:-3]

# # # # # # #             import json
# # # # # # #             return json.loads(result_text)

# # # # # # #         except Exception as e:
# # # # # # #             raise Exception(f"Error performing NER: {str(e)}")


# # # # # # # # Export service instance
# # # # # # # gemini_service = GeminiService()



# # # # # # import google.generativeai as genai
# # # # # # from PIL import Image
# # # # # # import io
# # # # # # from typing import Dict, Optional
# # # # # # from ..config import settings

# # # # # # class GeminiService:
# # # # # #     def __init__(self):
# # # # # #         genai.configure(api_key=settings.GEMINI_API_KEY)

# # # # # #         self.model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
# # # # # #         # self.model = genai.GenerativeModel("models/gemini-2.5-flash-image")
# # # # # #         # self.model = genai.GenerativeModel("gemini-1.5-flash")

    
# # # # # #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# # # # # #         """Extract text from image using Gemini Vision"""
# # # # # #         try:
# # # # # #             image = Image.open(io.BytesIO(image_bytes))

# # # # # #             prompt = """
# # # # # #             Extract all text from this document image.
# # # # # #             Maintain the original structure and formatting.
# # # # # #             Return only the extracted text without any additional commentary.
# # # # # #             """

# # # # # #             response = self.model.generate_content(
# # # # # #                 [prompt, image],
# # # # # #             )

# # # # # #             return response.text
        
# # # # # #         except Exception as e:
# # # # # #             raise Exception(f"Error extracting text: {str(e)}")
    
# # # # # #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# # # # # #         """Extract text from PDF using Gemini"""
# # # # # #         try:
# # # # # #             from pdf2image import convert_from_path

# # # # # #             images = convert_from_path(pdf_path)
# # # # # #             full_text = []

# # # # # #             for i, image in enumerate(images):
# # # # # #                 img_byte_arr = io.BytesIO()
# # # # # #                 image.save(img_byte_arr, format='PNG')
# # # # # #                 img_bytes = img_byte_arr.getvalue()

# # # # # #                 text = await self.extract_text_from_image(img_bytes)
# # # # # #                 full_text.append(f"--- Page {i+1} ---\n{text}")

# # # # # #             return "\n\n".join(full_text)
        
# # # # # #         except Exception as e:
# # # # # #             raise Exception(f"Error processing PDF: {str(e)}")
    
# # # # # #     async def perform_ner(self, text: str) -> Dict:
# # # # # #         """Perform Named Entity Recognition using Gemini"""
# # # # # #         try:
# # # # # #             prompt = f"""
# # # # # #             Analyze the following FRA (Forest Rights Act) document text and extract named entities.

# # # # # #             Text: {text}

# # # # # #             Extract and return a JSON object with the following entities:
# # # # # #             - PERSON
# # # # # #             - LOCATION
# # # # # #             - CLAIM_NUMBER
# # # # # #             - CLAIM_TYPE
# # # # # #             - SURVEY_NUMBER
# # # # # #             - AREA
# # # # # #             - COORDINATES
# # # # # #             - DATE
# # # # # #             - STATUS

# # # # # #             Return ONLY valid JSON.
# # # # # #             """

# # # # # #             response = self.model.generate_content(prompt)
# # # # # #             result_text = response.text.strip()

# # # # # #             if result_text.startswith("```json"):
# # # # # #                 result_text = result_text.replace("```json", "").replace("```", "").strip()
# # # # # #             elif result_text.startswith("```"):
# # # # # #                 result_text = result_text.replace("```", "").strip()

# # # # # #             import json
# # # # # #             return json.loads(result_text)

# # # # # #         except Exception as e:
# # # # # #             raise Exception(f"Error performing NER: {str(e)}")

# # # # # # gemini_service = GeminiService()


# # # # # # # level-1
# # # # # # import google.generativeai as genai
# # # # # # from PIL import Image
# # # # # # import io
# # # # # # import json
# # # # # # from typing import Dict
# # # # # # from ..config import settings


# # # # # # class GeminiService:
# # # # # #     def __init__(self):
# # # # # #         # Configure Gemini API
# # # # # #         genai.configure(api_key=settings.GEMINI_API_KEY)

# # # # # #         # Best stable model for OCR + NER
# # # # # #         self.model = genai.GenerativeModel("models/gemini-2.0-flash")

# # # # # #     # -----------------------------
# # # # # #     # IMAGE OCR
# # # # # #     # -----------------------------
# # # # # #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# # # # # #         """Extract text from image using Gemini Vision OCR."""
# # # # # #         try:
# # # # # #             image = Image.open(io.BytesIO(image_bytes))

# # # # # #             prompt = """
# # # # # #             Extract all readable text from this document image.
# # # # # #             Maintain original structure. DO NOT add explanations.
# # # # # #             Return only the extracted text.
# # # # # #             """

# # # # # #             response = await self.model.generate_content_async(
# # # # # #                 [prompt, image]
# # # # # #             )

# # # # # #             return response.text.strip()

# # # # # #         except Exception as e:
# # # # # #             raise Exception(f"Error extracting text: {str(e)}")

# # # # # #     # -----------------------------
# # # # # #     # PDF OCR
# # # # # #     # -----------------------------
# # # # # #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# # # # # #         """Extract text from a PDF by converting pages to images."""
# # # # # #         try:
# # # # # #             from pdf2image import convert_from_path

# # # # # #             images = convert_from_path(pdf_path)
# # # # # #             full_text = []

# # # # # #             for i, image in enumerate(images):
# # # # # #                 img_byte_arr = io.BytesIO()
# # # # # #                 image.save(img_byte_arr, format="PNG")
# # # # # #                 img_bytes = img_byte_arr.getvalue()

# # # # # #                 text = await self.extract_text_from_image(img_bytes)
# # # # # #                 full_text.append(f"--- Page {i + 1} ---\n{text}")

# # # # # #             return "\n\n".join(full_text)

# # # # # #         except Exception as e:
# # # # # #             raise Exception(f"Error processing PDF: {str(e)}")

# # # # # #     # -----------------------------
# # # # # #     # NER PROCESSING
# # # # # #     # -----------------------------
# # # # # #     async def perform_ner(self, extracted_text: str) -> Dict:
# # # # # #         """Perform Named Entity Recognition and structured extraction."""
# # # # # #         try:
# # # # # #             prompt = f"""
# # # # # #             You are an expert system analyzing FRA (Forest Rights Act) documents.
# # # # # #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.

# # # # # #             TEXT TO ANALYZE:
# # # # # #             {extracted_text}

# # # # # #             Return ONLY a valid JSON object in this exact structure:

# # # # # #             {{
# # # # # #                 "entities": {{
# # # # # #                     "persons": [],
# # # # # #                     "dependents": [],
# # # # # #                     "village": "",
# # # # # #                     "district": "",
# # # # # #                     "state": "",
# # # # # #                     "block": "",
# # # # # #                     "tribe_status": "",
# # # # # #                     "land_area": "",
# # # # # #                     "khasra_numbers": [],
# # # # # #                     "boundaries": "",
# # # # # #                     "others": {{}}
# # # # # #                 }},
# # # # # #                 "extracted_fields": {{
# # # # # #                     "patta_holder_name": "",
# # # # # #                     "village_name": "",
# # # # # #                     "state": "",
# # # # # #                     "district": "",
# # # # # #                     "block": "",
# # # # # #                     "survey_number": "",
# # # # # #                     "area_in_hectares": "",
# # # # # #                     "coordinates": ""
# # # # # #                 }}
# # # # # #             }}

# # # # # #             IMPORTANT RULES:
# # # # # #             - Return ONLY JSON (no explanation, no markdown).
# # # # # #             - If a field is missing in the text, return an empty string.
# # # # # #             """

# # # # # #             response = await self.model.generate_content_async(prompt)

# # # # # #             raw = response.text.strip()

# # # # # #             # Remove markdown if present
# # # # # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # # # # #             return json.loads(raw)

# # # # # #         except Exception as e:
# # # # # #             print("NER ERROR:", e)
# # # # # #             return {
# # # # # #                 "entities": {},
# # # # # #                 "extracted_fields": {}
# # # # # #             }


# # # # # # # Create service instance
# # # # # # gemini_service = GeminiService()


# # # # # # level-2

# # # # # import google.generativeai as genai
# # # # # from PIL import Image
# # # # # import io
# # # # # import json
# # # # # from typing import Dict
# # # # # from ..config import settings


# # # # # class GeminiService:
# # # # #     def __init__(self):
# # # # #         # Configure Gemini API
# # # # #         genai.configure(api_key=settings.GEMINI_API_KEY)

# # # # #         # Best stable model for OCR + NER
# # # # #         self.model = genai.GenerativeModel("models/gemini-2.0-flash")

# # # # #     # -----------------------------
# # # # #     # IMAGE OCR
# # # # #     # -----------------------------
# # # # #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# # # # #         """Extract text from image using Gemini Vision OCR."""
# # # # #         try:
# # # # #             image = Image.open(io.BytesIO(image_bytes))

# # # # #             prompt = """
# # # # #             Extract all readable text from this document image.
# # # # #             Maintain original structure. DO NOT add explanations.
# # # # #             Return only the extracted text.
# # # # #             """

# # # # #             response = await self.model.generate_content_async(
# # # # #                 [prompt, image]
# # # # #             )

# # # # #             return response.text.strip()

# # # # #         except Exception as e:
# # # # #             raise Exception(f"Error extracting text: {str(e)}")

# # # # #     # -----------------------------
# # # # #     # PDF OCR
# # # # #     # -----------------------------
# # # # #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# # # # #         """Extract text from a PDF by converting pages to images."""
# # # # #         try:
# # # # #             from pdf2image import convert_from_path

# # # # #             images = convert_from_path(pdf_path)
# # # # #             full_text = []

# # # # #             for i, image in enumerate(images):
# # # # #                 img_byte_arr = io.BytesIO()
# # # # #                 image.save(img_byte_arr, format="PNG")
# # # # #                 img_bytes = img_byte_arr.getvalue()

# # # # #                 text = await self.extract_text_from_image(img_bytes)
# # # # #                 full_text.append(f"--- Page {i + 1} ---\n{text}")

# # # # #             return "\n\n".join(full_text)

# # # # #         except Exception as e:
# # # # #             raise Exception(f"Error processing PDF: {str(e)}")

# # # # #     # -----------------------------
# # # # #     # NER PROCESSING (English - Level 1)
# # # # #     # -----------------------------
# # # # #     async def perform_ner(self, extracted_text: str) -> Dict:
# # # # #         """Perform Named Entity Recognition and structured extraction."""
# # # # #         try:
# # # # #             prompt = f"""
# # # # #             You are an expert system analyzing FRA (Forest Rights Act) documents.
# # # # #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.

# # # # #             TEXT TO ANALYZE:
# # # # #             {extracted_text}

# # # # #             Return ONLY a valid JSON object in this exact structure:

# # # # #             {{
# # # # #                 "entities": {{
# # # # #                     "persons": [],
# # # # #                     "dependents": [],
# # # # #                     "village": "",
# # # # #                     "district": "",
# # # # #                     "state": "",
# # # # #                     "block": "",
# # # # #                     "tribe_status": "",
# # # # #                     "land_area": "",
# # # # #                     "khasra_numbers": [],
# # # # #                     "boundaries": "",
# # # # #                     "others": {{}}
# # # # #                 }},
# # # # #                 "extracted_fields": {{
# # # # #                     "patta_holder_name": "",
# # # # #                     "village_name": "",
# # # # #                     "state": "",
# # # # #                     "district": "",
# # # # #                     "block": "",
# # # # #                     "survey_number": "",
# # # # #                     "area_in_hectares": "",
# # # # #                     "coordinates": ""
# # # # #                 }}
# # # # #             }}

# # # # #             IMPORTANT RULES:
# # # # #             - Return ONLY JSON (no explanation, no markdown).
# # # # #             - If a field is missing in the text, return an empty string.
# # # # #             """

# # # # #             response = await self.model.generate_content_async(prompt)

# # # # #             raw = response.text.strip()

# # # # #             # Remove markdown if present
# # # # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # # # #             return json.loads(raw)

# # # # #         except Exception as e:
# # # # #             print("NER ERROR:", e)
# # # # #             return {
# # # # #                 "entities": {},
# # # # #                 "extracted_fields": {}
# # # # #             }

# # # # #     # -----------------------------
# # # # #     # NER PROCESSING (Hindi/Marathi - Level 2)
# # # # #     # -----------------------------
# # # # #     async def perform_ner_native_language(self, extracted_text: str, language: str) -> Dict:
# # # # #         """Perform NER on Hindi/Marathi text while keeping output in native language."""
# # # # #         try:
# # # # #             language_name = "Hindi" if language == "hindi" else "Marathi"
            
# # # # #             prompt = f"""
# # # # #             You are an expert system analyzing FRA (Forest Rights Act) documents written in {language_name}.
# # # # #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.
# # # # #             KEEP ALL EXTRACTED VALUES IN THE ORIGINAL {language_name.upper()} LANGUAGE.

# # # # #             TEXT TO ANALYZE ({language_name}):
# # # # #             {extracted_text}

# # # # #             Return ONLY a valid JSON object in this exact structure:

# # # # #             {{
# # # # #                 "entities": {{
# # # # #                     "persons": [],
# # # # #                     "dependents": [],
# # # # #                     "village": "",
# # # # #                     "district": "",
# # # # #                     "state": "",
# # # # #                     "block": "",
# # # # #                     "tribe_status": "",
# # # # #                     "land_area": "",
# # # # #                     "khasra_numbers": [],
# # # # #                     "boundaries": "",
# # # # #                     "others": {{}}
# # # # #                 }},
# # # # #                 "extracted_fields": {{
# # # # #                     "patta_holder_name": "",
# # # # #                     "village_name": "",
# # # # #                     "state": "",
# # # # #                     "district": "",
# # # # #                     "block": "",
# # # # #                     "survey_number": "",
# # # # #                     "area_in_hectares": "",
# # # # #                     "coordinates": ""
# # # # #                 }}
# # # # #             }}

# # # # #             IMPORTANT RULES:
# # # # #             - Return ONLY JSON (no explanation, no markdown).
# # # # #             - Keep all values in original {language_name} script.
# # # # #             - If a field is missing in the text, return an empty string.
# # # # #             """

# # # # #             response = await self.model.generate_content_async(prompt)

# # # # #             raw = response.text.strip()

# # # # #             # Remove markdown if present
# # # # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # # # #             return json.loads(raw)

# # # # #         except Exception as e:
# # # # #             print(f"NER ERROR ({language}):", e)
# # # # #             return {
# # # # #                 "entities": {},
# # # # #                 "extracted_fields": {}
# # # # #             }

# # # # #     # -----------------------------
# # # # #     # TRANSLATION + NER (Level 3)
# # # # #     # -----------------------------
# # # # #     async def translate_and_ner(self, extracted_text: str, source_language: str) -> Dict:
# # # # #         """Translate Hindi/Marathi to English and perform NER."""
# # # # #         try:
# # # # #             language_name = "Hindi" if source_language == "hindi" else "Marathi"
            
# # # # #             prompt = f"""
# # # # #             You are an expert system analyzing FRA (Forest Rights Act) documents.
            
# # # # #             TASK:
# # # # #             1. Translate the {language_name} text to English
# # # # #             2. Extract structured FRA information
            
# # # # #             ORIGINAL TEXT ({language_name}):
# # # # #             {extracted_text}

# # # # #             Return ONLY a valid JSON object in this exact structure:

# # # # #             {{
# # # # #                 "translated_text": "Full English translation here...",
# # # # #                 "entities": {{
# # # # #                     "persons": [],
# # # # #                     "dependents": [],
# # # # #                     "village": "",
# # # # #                     "district": "",
# # # # #                     "state": "",
# # # # #                     "block": "",
# # # # #                     "tribe_status": "",
# # # # #                     "land_area": "",
# # # # #                     "khasra_numbers": [],
# # # # #                     "boundaries": "",
# # # # #                     "others": {{}}
# # # # #                 }},
# # # # #                 "extracted_fields": {{
# # # # #                     "patta_holder_name": "",
# # # # #                     "village_name": "",
# # # # #                     "state": "",
# # # # #                     "district": "",
# # # # #                     "block": "",
# # # # #                     "survey_number": "",
# # # # #                     "area_in_hectares": "",
# # # # #                     "coordinates": ""
# # # # #                 }}
# # # # #             }}

# # # # #             IMPORTANT RULES:
# # # # #             - Return ONLY JSON (no explanation, no markdown).
# # # # #             - Translate accurately to English.
# # # # #             - Extract all fields in English.
# # # # #             """

# # # # #             response = await self.model.generate_content_async(prompt)

# # # # #             raw = response.text.strip()

# # # # #             # Remove markdown if present
# # # # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # # # #             return json.loads(raw)

# # # # #         except Exception as e:
# # # # #             print(f"Translation + NER ERROR ({source_language}):", e)
# # # # #             return {
# # # # #                 "translated_text": "",
# # # # #                 "entities": {},
# # # # #                 "extracted_fields": {}
# # # # #             }


# # # # # # Create service instance
# # # # # gemini_service = GeminiService()


# # # # # voice
# # # # import google.generativeai as genai
# # # # from PIL import Image
# # # # import io
# # # # import json
# # # # from typing import Dict
# # # # from ..config import settings


# # # # class GeminiService:
# # # #     def __init__(self):
# # # #         # Configure Gemini API
# # # #         genai.configure(api_key=settings.GEMINI_API_KEY)

# # # #         # Best stable model for OCR + NER
# # # #         self.model = genai.GenerativeModel("models/gemini-2.0-flash")

# # # #     # -----------------------------
# # # #     # IMAGE OCR
# # # #     # -----------------------------
# # # #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# # # #         """Extract text from image using Gemini Vision OCR."""
# # # #         try:
# # # #             image = Image.open(io.BytesIO(image_bytes))

# # # #             prompt = """
# # # #             Extract all readable text from this document image.
# # # #             Maintain original structure. DO NOT add explanations.
# # # #             Return only the extracted text.
# # # #             """

# # # #             response = await self.model.generate_content_async(
# # # #                 [prompt, image]
# # # #             )

# # # #             return response.text.strip()

# # # #         except Exception as e:
# # # #             raise Exception(f"Error extracting text: {str(e)}")

# # # #     # -----------------------------
# # # #     # PDF OCR
# # # #     # -----------------------------
# # # #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# # # #         """Extract text from a PDF by converting pages to images."""
# # # #         try:
# # # #             from pdf2image import convert_from_path

# # # #             images = convert_from_path(pdf_path)
# # # #             full_text = []

# # # #             for i, image in enumerate(images):
# # # #                 img_byte_arr = io.BytesIO()
# # # #                 image.save(img_byte_arr, format="PNG")
# # # #                 img_bytes = img_byte_arr.getvalue()

# # # #                 text = await self.extract_text_from_image(img_bytes)
# # # #                 full_text.append(f"--- Page {i + 1} ---\n{text}")

# # # #             return "\n\n".join(full_text)

# # # #         except Exception as e:
# # # #             raise Exception(f"Error processing PDF: {str(e)}")

# # # #     # -----------------------------
# # # #     # NER PROCESSING (English - Level 1)
# # # #     # -----------------------------
# # # #     async def perform_ner(self, extracted_text: str) -> Dict:
# # # #         """Perform Named Entity Recognition and structured extraction."""
# # # #         try:
# # # #             prompt = f"""
# # # #             You are an expert system analyzing FRA (Forest Rights Act) documents.
# # # #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.

# # # #             TEXT TO ANALYZE:
# # # #             {extracted_text}

# # # #             Return ONLY a valid JSON object in this exact structure:

# # # #             {{
# # # #                 "entities": {{
# # # #                     "persons": [],
# # # #                     "dependents": [],
# # # #                     "village": "",
# # # #                     "district": "",
# # # #                     "state": "",
# # # #                     "block": "",
# # # #                     "tribe_status": "",
# # # #                     "land_area": "",
# # # #                     "khasra_numbers": [],
# # # #                     "boundaries": "",
# # # #                     "others": {{}}
# # # #                 }},
# # # #                 "extracted_fields": {{
# # # #                     "patta_holder_name": "",
# # # #                     "village_name": "",
# # # #                     "state": "",
# # # #                     "district": "",
# # # #                     "block": "",
# # # #                     "survey_number": "",
# # # #                     "area_in_hectares": "",
# # # #                     "coordinates": ""
# # # #                 }}
# # # #             }}

# # # #             IMPORTANT RULES:
# # # #             - Return ONLY JSON (no explanation, no markdown).
# # # #             - If a field is missing in the text, return an empty string.
# # # #             """

# # # #             response = await self.model.generate_content_async(prompt)

# # # #             raw = response.text.strip()

# # # #             # Remove markdown if present
# # # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # # #             return json.loads(raw)

# # # #         except Exception as e:
# # # #             print("NER ERROR:", e)
# # # #             return {
# # # #                 "entities": {},
# # # #                 "extracted_fields": {}
# # # #             }

# # # #     # -----------------------------
# # # #     # NER PROCESSING (Hindi/Marathi - Level 2)
# # # #     # -----------------------------
# # # #     async def perform_ner_native_language(self, extracted_text: str, language: str) -> Dict:
# # # #         """Perform NER on Hindi/Marathi text while keeping output in native language."""
# # # #         try:
# # # #             language_name = "Hindi" if language == "hindi" else "Marathi"
            
# # # #             prompt = f"""
# # # #             You are an expert system analyzing FRA (Forest Rights Act) documents written in {language_name}.
# # # #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.
# # # #             KEEP ALL EXTRACTED VALUES IN THE ORIGINAL {language_name.upper()} LANGUAGE.

# # # #             TEXT TO ANALYZE ({language_name}):
# # # #             {extracted_text}

# # # #             Return ONLY a valid JSON object in this exact structure:

# # # #             {{
# # # #                 "entities": {{
# # # #                     "persons": [],
# # # #                     "dependents": [],
# # # #                     "village": "",
# # # #                     "district": "",
# # # #                     "state": "",
# # # #                     "block": "",
# # # #                     "tribe_status": "",
# # # #                     "land_area": "",
# # # #                     "khasra_numbers": [],
# # # #                     "boundaries": "",
# # # #                     "others": {{}}
# # # #                 }},
# # # #                 "extracted_fields": {{
# # # #                     "patta_holder_name": "",
# # # #                     "village_name": "",
# # # #                     "state": "",
# # # #                     "district": "",
# # # #                     "block": "",
# # # #                     "survey_number": "",
# # # #                     "area_in_hectares": "",
# # # #                     "coordinates": ""
# # # #                 }}
# # # #             }}

# # # #             IMPORTANT RULES:
# # # #             - Return ONLY JSON (no explanation, no markdown).
# # # #             - Keep all values in original {language_name} script.
# # # #             - If a field is missing in the text, return an empty string.
# # # #             """

# # # #             response = await self.model.generate_content_async(prompt)

# # # #             raw = response.text.strip()

# # # #             # Remove markdown if present
# # # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # # #             return json.loads(raw)

# # # #         except Exception as e:
# # # #             print(f"NER ERROR ({language}):", e)
# # # #             return {
# # # #                 "entities": {},
# # # #                 "extracted_fields": {}
# # # #             }

# # # #     # -----------------------------
# # # #     # TRANSLATION + NER (Level 3)
# # # #     # -----------------------------
# # # #     async def translate_and_ner(self, extracted_text: str, source_language: str) -> Dict:
# # # #         """Translate Hindi/Marathi to English and perform NER."""
# # # #         try:
# # # #             language_name = "Hindi" if source_language == "hindi" else "Marathi"
            
# # # #             prompt = f"""
# # # #             You are an expert system analyzing FRA (Forest Rights Act) documents.
            
# # # #             TASK:
# # # #             1. Translate the {language_name} text to English
# # # #             2. Extract structured FRA information
            
# # # #             ORIGINAL TEXT ({language_name}):
# # # #             {extracted_text}

# # # #             Return ONLY a valid JSON object in this exact structure:

# # # #             {{
# # # #                 "translated_text": "Full English translation here...",
# # # #                 "entities": {{
# # # #                     "persons": [],
# # # #                     "dependents": [],
# # # #                     "village": "",
# # # #                     "district": "",
# # # #                     "state": "",
# # # #                     "block": "",
# # # #                     "tribe_status": "",
# # # #                     "land_area": "",
# # # #                     "khasra_numbers": [],
# # # #                     "boundaries": "",
# # # #                     "others": {{}}
# # # #                 }},
# # # #                 "extracted_fields": {{
# # # #                     "patta_holder_name": "",
# # # #                     "village_name": "",
# # # #                     "state": "",
# # # #                     "district": "",
# # # #                     "block": "",
# # # #                     "survey_number": "",
# # # #                     "area_in_hectares": "",
# # # #                     "coordinates": ""
# # # #                 }}
# # # #             }}

# # # #             IMPORTANT RULES:
# # # #             - Return ONLY JSON (no explanation, no markdown).
# # # #             - Translate accurately to English.
# # # #             - Extract all fields in English.
# # # #             """

# # # #             response = await self.model.generate_content_async(prompt)

# # # #             raw = response.text.strip()

# # # #             # Remove markdown if present
# # # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # # #             return json.loads(raw)

# # # #         except Exception as e:
# # # #             print(f"Translation + NER ERROR ({source_language}):", e)
# # # #             return {
# # # #                 "translated_text": "",
# # # #                 "entities": {},
# # # #                 "extracted_fields": {}
# # # #             }

# # # #     # -----------------------------
# # # #     # TEXT-TO-SPEECH (Level 4)
# # # #     # -----------------------------
# # # #     async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
# # # #         """
# # # #         Generate speech from text using Gemini TTS.
# # # #         Note: Gemini doesn't have native TTS. This is a placeholder.
# # # #         Use Google Text-to-Speech API or gTTS library instead.
# # # #         """
# # # #         try:
# # # #             # For actual TTS, use gTTS or Google Cloud TTS
# # # #             from gtts import gTTS
            
# # # #             lang_code = "hi" if language == "hindi" else "mr" if language == "marathi" else "en"
            
# # # #             tts = gTTS(text=text, lang=lang_code, slow=False)
            
# # # #             audio_bytes = io.BytesIO()
# # # #             tts.write_to_fp(audio_bytes)
# # # #             audio_bytes.seek(0)
            
# # # #             return audio_bytes.read()
            
# # # #         except Exception as e:
# # # #             raise Exception(f"Error generating speech: {str(e)}")


# # # # # Create service instance
# # # # gemini_service = GeminiService()

# # # import google.generativeai as genai
# # # from PIL import Image
# # # import io
# # # import json
# # # from typing import Dict
# # # from ..config import settings


# # # class GeminiService:
# # #     def __init__(self):
# # #         try:
# # #             # Configure Gemini API
# # #             genai.configure(api_key=settings.GEMINI_API_KEY)

# # #             # Best stable model for OCR + NER
# # #             self.model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
# # #         except Exception as e:
# # #             print(f"WARNING: Gemini initialization failed: {e}")
# # #             print("Make sure GEMINI_API_KEY is set in .env file")
# # #             self.model = None

# # #     # -----------------------------
# # #     # IMAGE OCR
# # #     # -----------------------------
# # #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# # #         """Extract text from image using Gemini Vision OCR."""
# # #         if not self.model:
# # #             raise Exception("Gemini model not initialized. Check API key.")
            
# # #         try:
# # #             image = Image.open(io.BytesIO(image_bytes))

# # #             prompt = """
# # #             Extract all readable text from this document image.
# # #             Maintain original structure. DO NOT add explanations.
# # #             Return only the extracted text.
# # #             """

# # #             response = await self.model.generate_content_async(
# # #                 [prompt, image]
# # #             )

# # #             return response.text.strip()

# # #         except Exception as e:
# # #             raise Exception(f"Error extracting text: {str(e)}")

# # #     # -----------------------------
# # #     # PDF OCR
# # #     # -----------------------------
# # #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# # #         """Extract text from a PDF by converting pages to images."""
# # #         if not self.model:
# # #             raise Exception("Gemini model not initialized. Check API key.")
            
# # #         try:
# # #             from pdf2image import convert_from_path

# # #             images = convert_from_path(pdf_path)
# # #             full_text = []

# # #             for i, image in enumerate(images):
# # #                 img_byte_arr = io.BytesIO()
# # #                 image.save(img_byte_arr, format="PNG")
# # #                 img_bytes = img_byte_arr.getvalue()

# # #                 text = await self.extract_text_from_image(img_bytes)
# # #                 full_text.append(f"--- Page {i + 1} ---\n{text}")

# # #             return "\n\n".join(full_text)

# # #         except ImportError:
# # #             raise Exception("pdf2image not installed. Run: pip install pdf2image")
# # #         except Exception as e:
# # #             raise Exception(f"Error processing PDF: {str(e)}")

# # #     # -----------------------------
# # #     # NER PROCESSING (English - Level 1)
# # #     # -----------------------------
# # #     async def perform_ner(self, extracted_text: str) -> Dict:
# # #         """Perform Named Entity Recognition and structured extraction."""
# # #         if not self.model:
# # #             raise Exception("Gemini model not initialized. Check API key.")
            
# # #         try:
# # #             prompt = f"""
# # #             You are an expert system analyzing FRA (Forest Rights Act) documents.
# # #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.

# # #             TEXT TO ANALYZE:
# # #             {extracted_text}

# # #             Return ONLY a valid JSON object in this exact structure:

# # #             {{
# # #                 "entities": {{
# # #                     "persons": [],
# # #                     "dependents": [],
# # #                     "village": "",
# # #                     "district": "",
# # #                     "state": "",
# # #                     "block": "",
# # #                     "tribe_status": "",
# # #                     "land_area": "",
# # #                     "khasra_numbers": [],
# # #                     "boundaries": "",
# # #                     "others": {{}}
# # #                 }},
# # #                 "extracted_fields": {{
# # #                     "patta_holder_name": "",
# # #                     "village_name": "",
# # #                     "state": "",
# # #                     "district": "",
# # #                     "block": "",
# # #                     "survey_number": "",
# # #                     "area_in_hectares": "",
# # #                     "coordinates": ""
# # #                 }}
# # #             }}

# # #             IMPORTANT RULES:
# # #             - Return ONLY JSON (no explanation, no markdown).
# # #             - If a field is missing in the text, return an empty string.
# # #             """

# # #             response = await self.model.generate_content_async(prompt)

# # #             raw = response.text.strip()

# # #             # Remove markdown if present
# # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # #             return json.loads(raw)

# # #         except json.JSONDecodeError as e:
# # #             print(f"NER JSON Parse Error: {e}")
# # #             print(f"Raw response: {raw}")
# # #             return {
# # #                 "entities": {},
# # #                 "extracted_fields": {}
# # #             }
# # #         except Exception as e:
# # #             print("NER ERROR:", e)
# # #             return {
# # #                 "entities": {},
# # #                 "extracted_fields": {}
# # #             }

# # #     # -----------------------------
# # #     # NER PROCESSING (Hindi/Marathi - Level 2)
# # #     # -----------------------------
# # #     async def perform_ner_native_language(self, extracted_text: str, language: str) -> Dict:
# # #         """Perform NER on Hindi/Marathi text while keeping output in native language."""
# # #         if not self.model:
# # #             raise Exception("Gemini model not initialized. Check API key.")
            
# # #         try:
# # #             language_name = "Hindi" if language == "hindi" else "Marathi"
            
# # #             prompt = f"""
# # #             You are an expert system analyzing FRA (Forest Rights Act) documents written in {language_name}.
# # #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.
# # #             KEEP ALL EXTRACTED VALUES IN THE ORIGINAL {language_name.upper()} LANGUAGE.

# # #             TEXT TO ANALYZE ({language_name}):
# # #             {extracted_text}

# # #             Return ONLY a valid JSON object in this exact structure:

# # #             {{
# # #                 "entities": {{
# # #                     "persons": [],
# # #                     "dependents": [],
# # #                     "village": "",
# # #                     "district": "",
# # #                     "state": "",
# # #                     "block": "",
# # #                     "tribe_status": "",
# # #                     "land_area": "",
# # #                     "khasra_numbers": [],
# # #                     "boundaries": "",
# # #                     "others": {{}}
# # #                 }},
# # #                 "extracted_fields": {{
# # #                     "patta_holder_name": "",
# # #                     "village_name": "",
# # #                     "state": "",
# # #                     "district": "",
# # #                     "block": "",
# # #                     "survey_number": "",
# # #                     "area_in_hectares": "",
# # #                     "coordinates": ""
# # #                 }}
# # #             }}

# # #             IMPORTANT RULES:
# # #             - Return ONLY JSON (no explanation, no markdown).
# # #             - Keep all values in original {language_name} script.
# # #             - If a field is missing in the text, return an empty string.
# # #             """

# # #             response = await self.model.generate_content_async(prompt)

# # #             raw = response.text.strip()

# # #             # Remove markdown if present
# # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # #             return json.loads(raw)

# # #         except Exception as e:
# # #             print(f"NER ERROR ({language}):", e)
# # #             return {
# # #                 "entities": {},
# # #                 "extracted_fields": {}
# # #             }

# # #     # -----------------------------
# # #     # TRANSLATION + NER (Level 3)
# # #     # -----------------------------
# # #     async def translate_and_ner(self, extracted_text: str, source_language: str) -> Dict:
# # #         """Translate Hindi/Marathi to English and perform NER."""
# # #         if not self.model:
# # #             raise Exception("Gemini model not initialized. Check API key.")
            
# # #         try:
# # #             language_name = "Hindi" if source_language == "hindi" else "Marathi"
            
# # #             prompt = f"""
# # #             You are an expert system analyzing FRA (Forest Rights Act) documents.
            
# # #             TASK:
# # #             1. Translate the {language_name} text to English
# # #             2. Extract structured FRA information
            
# # #             ORIGINAL TEXT ({language_name}):
# # #             {extracted_text}

# # #             Return ONLY a valid JSON object in this exact structure:

# # #             {{
# # #                 "translated_text": "Full English translation here...",
# # #                 "entities": {{
# # #                     "persons": [],
# # #                     "dependents": [],
# # #                     "village": "",
# # #                     "district": "",
# # #                     "state": "",
# # #                     "block": "",
# # #                     "tribe_status": "",
# # #                     "land_area": "",
# # #                     "khasra_numbers": [],
# # #                     "boundaries": "",
# # #                     "others": {{}}
# # #                 }},
# # #                 "extracted_fields": {{
# # #                     "patta_holder_name": "",
# # #                     "village_name": "",
# # #                     "state": "",
# # #                     "district": "",
# # #                     "block": "",
# # #                     "survey_number": "",
# # #                     "area_in_hectares": "",
# # #                     "coordinates": ""
# # #                 }}
# # #             }}

# # #             IMPORTANT RULES:
# # #             - Return ONLY JSON (no explanation, no markdown).
# # #             - Translate accurately to English.
# # #             - Extract all fields in English.
# # #             """

# # #             response = await self.model.generate_content_async(prompt)

# # #             raw = response.text.strip()

# # #             # Remove markdown if present
# # #             raw = raw.replace("```json", "").replace("```", "").strip()

# # #             return json.loads(raw)

# # #         except Exception as e:
# # #             print(f"Translation + NER ERROR ({source_language}):", e)
# # #             return {
# # #                 "translated_text": "",
# # #                 "entities": {},
# # #                 "extracted_fields": {}
# # #             }

# # #     # -----------------------------
# # #     # TEXT-TO-SPEECH (Level 4)
# # #     # -----------------------------
# # #     async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
# # #         """
# # #         Generate speech from text using gTTS.
# # #         """
# # #         try:
# # #             from gtts import gTTS
            
# # #             lang_code = "hi" if language == "hindi" else "mr" if language == "marathi" else "en"
            
# # #             tts = gTTS(text=text, lang=lang_code, slow=False)
            
# # #             audio_bytes = io.BytesIO()
# # #             tts.write_to_fp(audio_bytes)
# # #             audio_bytes.seek(0)
            
# # #             return audio_bytes.read()
            
# # #         except ImportError:
# # #             raise Exception("gTTS not installed. Run: pip install gtts")
# # #         except Exception as e:
# # #             raise Exception(f"Error generating speech: {str(e)}")


# # # # Create service instance
# # # try:
# # #     gemini_service = GeminiService()
# # # except Exception as e:
# # #     print(f"Failed to initialize Gemini service: {e}")
# # #     gemini_service = None


# # # changing model
# # import google.generativeai as genai
# # from PIL import Image
# # import io
# # import json
# # from typing import Dict
# # import time
# # from ..config import settings


# # class GeminiService:
# #     def __init__(self):
# #         try:
# #             # Configure Gemini API
# #             genai.configure(api_key=settings.GEMINI_API_KEY)

# #             # Use stable model with better rate limits
# #             # Changed from gemini-2.0-flash-exp to gemini-1.5-flash
# #             self.model = genai.GenerativeModel("gemini-1.5-flash")
            
# #             # Rate limiting
# #             self.last_request_time = 0
# #             self.min_request_interval = 1.0  # 1 second between requests
            
# #             print("✓ Gemini service initialized with gemini-1.5-flash")
# #         except Exception as e:
# #             print(f"WARNING: Gemini initialization failed: {e}")
# #             print("Make sure GEMINI_API_KEY is set in .env file")
# #             self.model = None

# #     def _rate_limit(self):
# #         """Ensure minimum time between API requests"""
# #         current_time = time.time()
# #         time_since_last_request = current_time - self.last_request_time
        
# #         if time_since_last_request < self.min_request_interval:
# #             sleep_time = self.min_request_interval - time_since_last_request
# #             print(f"Rate limiting: waiting {sleep_time:.2f}s")
# #             time.sleep(sleep_time)
        
# #         self.last_request_time = time.time()

# #     # -----------------------------
# #     # IMAGE OCR
# #     # -----------------------------
# #     async def extract_text_from_image(self, image_bytes: bytes) -> str:
# #         """Extract text from image using Gemini Vision OCR."""
# #         if not self.model:
# #             raise Exception("Gemini model not initialized. Check API key.")
        
# #         self._rate_limit()  # Apply rate limiting
            
# #         try:
# #             image = Image.open(io.BytesIO(image_bytes))

# #             prompt = """
# #             Extract all readable text from this document image.
# #             Maintain original structure. DO NOT add explanations.
# #             Return only the extracted text.
# #             """

# #             response = await self.model.generate_content_async(
# #                 [prompt, image]
# #             )

# #             return response.text.strip()

# #         except Exception as e:
# #             if "429" in str(e) or "quota" in str(e).lower():
# #                 raise Exception("Rate limit exceeded. Please wait a moment and try again.")
# #             raise Exception(f"Error extracting text: {str(e)}")

# #     # -----------------------------
# #     # PDF OCR
# #     # -----------------------------
# #     async def extract_text_from_pdf(self, pdf_path: str) -> str:
# #         """Extract text from a PDF by converting pages to images."""
# #         if not self.model:
# #             raise Exception("Gemini model not initialized. Check API key.")
            
# #         try:
# #             from pdf2image import convert_from_path

# #             images = convert_from_path(pdf_path)
# #             full_text = []

# #             for i, image in enumerate(images):
# #                 img_byte_arr = io.BytesIO()
# #                 image.save(img_byte_arr, format="PNG")
# #                 img_bytes = img_byte_arr.getvalue()

# #                 text = await self.extract_text_from_image(img_bytes)
# #                 full_text.append(f"--- Page {i + 1} ---\n{text}")

# #             return "\n\n".join(full_text)

# #         except ImportError:
# #             raise Exception("pdf2image not installed. Run: pip install pdf2image")
# #         except Exception as e:
# #             raise Exception(f"Error processing PDF: {str(e)}")

# #     # -----------------------------
# #     # NER PROCESSING (English - Level 1)
# #     # -----------------------------
# #     async def perform_ner(self, extracted_text: str) -> Dict:
# #         """Perform Named Entity Recognition and structured extraction."""
# #         if not self.model:
# #             raise Exception("Gemini model not initialized. Check API key.")
        
# #         self._rate_limit()  # Apply rate limiting
            
# #         try:
# #             prompt = f"""
# #             You are an expert system analyzing FRA (Forest Rights Act) documents.
# #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.

# #             TEXT TO ANALYZE:
# #             {extracted_text}

# #             Return ONLY a valid JSON object in this exact structure:

# #             {{
# #                 "entities": {{
# #                     "persons": [],
# #                     "dependents": [],
# #                     "village": "",
# #                     "district": "",
# #                     "state": "",
# #                     "block": "",
# #                     "tribe_status": "",
# #                     "land_area": "",
# #                     "khasra_numbers": [],
# #                     "boundaries": "",
# #                     "others": {{}}
# #                 }},
# #                 "extracted_fields": {{
# #                     "patta_holder_name": "",
# #                     "village_name": "",
# #                     "state": "",
# #                     "district": "",
# #                     "block": "",
# #                     "survey_number": "",
# #                     "area_in_hectares": "",
# #                     "coordinates": ""
# #                 }}
# #             }}

# #             IMPORTANT RULES:
# #             - Return ONLY JSON (no explanation, no markdown).
# #             - If a field is missing in the text, return an empty string.
# #             """

# #             response = await self.model.generate_content_async(prompt)

# #             raw = response.text.strip()

# #             # Remove markdown if present
# #             raw = raw.replace("```json", "").replace("```", "").strip()

# #             return json.loads(raw)

# #         except json.JSONDecodeError as e:
# #             print(f"NER JSON Parse Error: {e}")
# #             print(f"Raw response: {raw}")
# #             return {
# #                 "entities": {},
# #                 "extracted_fields": {}
# #             }
# #         except Exception as e:
# #             if "429" in str(e) or "quota" in str(e).lower():
# #                 raise Exception("Rate limit exceeded. Please wait a moment and try again.")
# #             print("NER ERROR:", e)
# #             return {
# #                 "entities": {},
# #                 "extracted_fields": {}
# #             }

# #     # -----------------------------
# #     # NER PROCESSING (Hindi/Marathi - Level 2)
# #     # -----------------------------
# #     async def perform_ner_native_language(self, extracted_text: str, language: str) -> Dict:
# #         """Perform NER on Hindi/Marathi text while keeping output in native language."""
# #         if not self.model:
# #             raise Exception("Gemini model not initialized. Check API key.")
        
# #         self._rate_limit()  # Apply rate limiting
            
# #         try:
# #             language_name = "Hindi" if language == "hindi" else "Marathi"
            
# #             prompt = f"""
# #             You are an expert system analyzing FRA (Forest Rights Act) documents written in {language_name}.
# #             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.
# #             KEEP ALL EXTRACTED VALUES IN THE ORIGINAL {language_name.upper()} LANGUAGE.

# #             TEXT TO ANALYZE ({language_name}):
# #             {extracted_text}

# #             Return ONLY a valid JSON object in this exact structure:

# #             {{
# #                 "entities": {{
# #                     "persons": [],
# #                     "dependents": [],
# #                     "village": "",
# #                     "district": "",
# #                     "state": "",
# #                     "block": "",
# #                     "tribe_status": "",
# #                     "land_area": "",
# #                     "khasra_numbers": [],
# #                     "boundaries": "",
# #                     "others": {{}}
# #                 }},
# #                 "extracted_fields": {{
# #                     "patta_holder_name": "",
# #                     "village_name": "",
# #                     "state": "",
# #                     "district": "",
# #                     "block": "",
# #                     "survey_number": "",
# #                     "area_in_hectares": "",
# #                     "coordinates": ""
# #                 }}
# #             }}

# #             IMPORTANT RULES:
# #             - Return ONLY JSON (no explanation, no markdown).
# #             - Keep all values in original {language_name} script.
# #             - If a field is missing in the text, return an empty string.
# #             """

# #             response = await self.model.generate_content_async(prompt)

# #             raw = response.text.strip()

# #             # Remove markdown if present
# #             raw = raw.replace("```json", "").replace("```", "").strip()

# #             return json.loads(raw)

# #         except Exception as e:
# #             if "429" in str(e) or "quota" in str(e).lower():
# #                 raise Exception("Rate limit exceeded. Please wait a moment and try again.")
# #             print(f"NER ERROR ({language}):", e)
# #             return {
# #                 "entities": {},
# #                 "extracted_fields": {}
# #             }

# #     # -----------------------------
# #     # TRANSLATION + NER (Level 3)
# #     # -----------------------------
# #     async def translate_and_ner(self, extracted_text: str, source_language: str) -> Dict:
# #         """Translate Hindi/Marathi to English and perform NER."""
# #         if not self.model:
# #             raise Exception("Gemini model not initialized. Check API key.")
        
# #         self._rate_limit()  # Apply rate limiting
            
# #         try:
# #             language_name = "Hindi" if source_language == "hindi" else "Marathi"
            
# #             prompt = f"""
# #             You are an expert system analyzing FRA (Forest Rights Act) documents.
            
# #             TASK:
# #             1. Translate the {language_name} text to English
# #             2. Extract structured FRA information
            
# #             ORIGINAL TEXT ({language_name}):
# #             {extracted_text}

# #             Return ONLY a valid JSON object in this exact structure:

# #             {{
# #                 "translated_text": "Full English translation here...",
# #                 "entities": {{
# #                     "persons": [],
# #                     "dependents": [],
# #                     "village": "",
# #                     "district": "",
# #                     "state": "",
# #                     "block": "",
# #                     "tribe_status": "",
# #                     "land_area": "",
# #                     "khasra_numbers": [],
# #                     "boundaries": "",
# #                     "others": {{}}
# #                 }},
# #                 "extracted_fields": {{
# #                     "patta_holder_name": "",
# #                     "village_name": "",
# #                     "state": "",
# #                     "district": "",
# #                     "block": "",
# #                     "survey_number": "",
# #                     "area_in_hectares": "",
# #                     "coordinates": ""
# #                 }}
# #             }}

# #             IMPORTANT RULES:
# #             - Return ONLY JSON (no explanation, no markdown).
# #             - Translate accurately to English.
# #             - Extract all fields in English.
# #             """

# #             response = await self.model.generate_content_async(prompt)

# #             raw = response.text.strip()

# #             # Remove markdown if present
# #             raw = raw.replace("```json", "").replace("```", "").strip()

# #             return json.loads(raw)

# #         except Exception as e:
# #             if "429" in str(e) or "quota" in str(e).lower():
# #                 raise Exception("Rate limit exceeded. Please wait a moment and try again.")
# #             print(f"Translation + NER ERROR ({source_language}):", e)
# #             return {
# #                 "translated_text": "",
# #                 "entities": {},
# #                 "extracted_fields": {}
# #             }

# #     # -----------------------------
# #     # TEXT-TO-SPEECH (Level 4)
# #     # -----------------------------
# #     async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
# #         """
# #         Generate speech from text using gTTS.
# #         """
# #         try:
# #             from gtts import gTTS
            
# #             lang_code = "hi" if language == "hindi" else "mr" if language == "marathi" else "en"
            
# #             tts = gTTS(text=text, lang=lang_code, slow=False)
            
# #             audio_bytes = io.BytesIO()
# #             tts.write_to_fp(audio_bytes)
# #             audio_bytes.seek(0)
            
# #             return audio_bytes.read()
            
# #         except ImportError:
# #             raise Exception("gTTS not installed. Run: pip install gtts")
# #         except Exception as e:
# #             raise Exception(f"Error generating speech: {str(e)}")


# # # Create service instance
# # try:
# #     gemini_service = GeminiService()
# # except Exception as e:
# #     print(f"Failed to initialize Gemini service: {e}")
# #     gemini_service = None



# # all language

# import google.generativeai as genai
# from PIL import Image
# import io
# import json
# from typing import Dict
# import time
# from ..config import settings


# class GeminiService:
#     def __init__(self):
#         try:
#             # Configure Gemini API
#             genai.configure(api_key=settings.GEMINI_API_KEY)

#             # Use stable model with better rate limits
#             # self.model = genai.GenerativeModel("gemini-1.5-flash")
#             self.model = genai.GenerativeModel("gemini-1.5-flash-latest")

            
#             # Rate limiting
#             self.last_request_time = 0
#             self.min_request_interval = 1.0  # 1 second between requests
            
#             print("✓ Gemini service initialized with gemini-1.5-flash")
#         except Exception as e:
#             print(f"WARNING: Gemini initialization failed: {e}")
#             print("Make sure GEMINI_API_KEY is set in .env file")
#             self.model = None

#     def _rate_limit(self):
#         """Ensure minimum time between API requests"""
#         current_time = time.time()
#         time_since_last_request = current_time - self.last_request_time
        
#         if time_since_last_request < self.min_request_interval:
#             sleep_time = self.min_request_interval - time_since_last_request
#             print(f"Rate limiting: waiting {sleep_time:.2f}s")
#             time.sleep(sleep_time)
        
#         self.last_request_time = time.time()

#     # -----------------------------
#     # IMAGE OCR
#     # -----------------------------
#     async def extract_text_from_image(self, image_bytes: bytes) -> str:
#         """Extract text from image using Gemini Vision OCR."""
#         if not self.model:
#             raise Exception("Gemini model not initialized. Check API key.")
        
#         self._rate_limit()
            
#         try:
#             image = Image.open(io.BytesIO(image_bytes))

#             prompt = """
#             Extract all readable text from this document image.
#             Maintain original structure. DO NOT add explanations.
#             Return only the extracted text.
#             Support all Indian languages including Hindi, Marathi, Bengali, Telugu, Tamil, Odia, Urdu, Kokborok.
#             """

#             response = await self.model.generate_content_async(
#                 [prompt, image]
#             )

#             return response.text.strip()

#         except Exception as e:
#             if "429" in str(e) or "quota" in str(e).lower():
#                 raise Exception("Rate limit exceeded. Please wait a moment and try again.")
#             raise Exception(f"Error extracting text: {str(e)}")

#     # -----------------------------
#     # PDF OCR
#     # -----------------------------
#     async def extract_text_from_pdf(self, pdf_path: str) -> str:
#         """Extract text from a PDF by converting pages to images."""
#         if not self.model:
#             raise Exception("Gemini model not initialized. Check API key.")
            
#         try:
#             from pdf2image import convert_from_path

#             images = convert_from_path(pdf_path)
#             full_text = []

#             for i, image in enumerate(images):
#                 img_byte_arr = io.BytesIO()
#                 image.save(img_byte_arr, format="PNG")
#                 img_bytes = img_byte_arr.getvalue()

#                 text = await self.extract_text_from_image(img_bytes)
#                 full_text.append(f"--- Page {i + 1} ---\n{text}")

#             return "\n\n".join(full_text)

#         except ImportError:
#             raise Exception("pdf2image not installed. Run: pip install pdf2image")
#         except Exception as e:
#             raise Exception(f"Error processing PDF: {str(e)}")

#     # -----------------------------
#     # NER PROCESSING (English - Level 1)
#     # -----------------------------
#     async def perform_ner(self, extracted_text: str) -> Dict:
#         """Perform Named Entity Recognition and structured extraction."""
#         if not self.model:
#             raise Exception("Gemini model not initialized. Check API key.")
        
#         self._rate_limit()
            
#         try:
#             prompt = f"""
#             You are an expert system analyzing FRA (Forest Rights Act) documents.
#             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.

#             TEXT TO ANALYZE:
#             {extracted_text}

#             Return ONLY a valid JSON object in this exact structure:

#             {{
#                 "entities": {{
#                     "persons": [],
#                     "dependents": [],
#                     "village": "",
#                     "district": "",
#                     "state": "",
#                     "block": "",
#                     "tribe_status": "",
#                     "land_area": "",
#                     "khasra_numbers": [],
#                     "boundaries": "",
#                     "others": {{}}
#                 }},
#                 "extracted_fields": {{
#                     "patta_holder_name": "",
#                     "village_name": "",
#                     "state": "",
#                     "district": "",
#                     "block": "",
#                     "survey_number": "",
#                     "area_in_hectares": "",
#                     "coordinates": ""
#                 }}
#             }}

#             IMPORTANT RULES:
#             - Return ONLY JSON (no explanation, no markdown).
#             - If a field is missing in the text, return an empty string.
#             """

#             response = await self.model.generate_content_async(prompt)

#             raw = response.text.strip()
#             raw = raw.replace("```json", "").replace("```", "").strip()

#             return json.loads(raw)

#         except json.JSONDecodeError as e:
#             print(f"NER JSON Parse Error: {e}")
#             return {"entities": {}, "extracted_fields": {}}
#         except Exception as e:
#             if "429" in str(e) or "quota" in str(e).lower():
#                 raise Exception("Rate limit exceeded. Please wait a moment and try again.")
#             print("NER ERROR:", e)
#             return {"entities": {}, "extracted_fields": {}}

#     # -----------------------------
#     # NER PROCESSING (Indian Languages - Level 2)
#     # -----------------------------
#     async def perform_ner_native_language(self, extracted_text: str, language: str) -> Dict:
#         """Perform NER on Indian language text while keeping output in native language."""
#         if not self.model:
#             raise Exception("Gemini model not initialized. Check API key.")
        
#         self._rate_limit()
        
#         # Language mapping
#         language_map = {
#             "hindi": "Hindi",
#             "marathi": "Marathi",
#             "bengali": "Bengali",
#             "telugu": "Telugu",
#             "tamil": "Tamil",
#             "odia": "Odia",
#             "urdu": "Urdu",
#             "kokborok": "Kokborok (Tripuri)"
#         }
        
#         language_name = language_map.get(language, language.title())
            
#         try:
#             prompt = f"""
#             You are an expert system analyzing FRA (Forest Rights Act) documents written in {language_name}.
#             Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.
#             KEEP ALL EXTRACTED VALUES IN THE ORIGINAL {language_name.upper()} LANGUAGE.

#             TEXT TO ANALYZE ({language_name}):
#             {extracted_text}

#             Return ONLY a valid JSON object in this exact structure:

#             {{
#                 "entities": {{
#                     "persons": [],
#                     "dependents": [],
#                     "village": "",
#                     "district": "",
#                     "state": "",
#                     "block": "",
#                     "tribe_status": "",
#                     "land_area": "",
#                     "khasra_numbers": [],
#                     "boundaries": "",
#                     "others": {{}}
#                 }},
#                 "extracted_fields": {{
#                     "patta_holder_name": "",
#                     "village_name": "",
#                     "state": "",
#                     "district": "",
#                     "block": "",
#                     "survey_number": "",
#                     "area_in_hectares": "",
#                     "coordinates": ""
#                 }}
#             }}

#             IMPORTANT RULES:
#             - Return ONLY JSON (no explanation, no markdown).
#             - Keep all values in original {language_name} script.
#             - If a field is missing in the text, return an empty string.
#             """

#             response = await self.model.generate_content_async(prompt)

#             raw = response.text.strip()
#             raw = raw.replace("```json", "").replace("```", "").strip()

#             return json.loads(raw)

#         except Exception as e:
#             if "429" in str(e) or "quota" in str(e).lower():
#                 raise Exception("Rate limit exceeded. Please wait a moment and try again.")
#             print(f"NER ERROR ({language}):", e)
#             return {"entities": {}, "extracted_fields": {}}

#     # -----------------------------
#     # TRANSLATION + NER (Level 3)
#     # -----------------------------
#     async def translate_and_ner(self, extracted_text: str, source_language: str) -> Dict:
#         """Translate any Indian language to English and perform NER."""
#         if not self.model:
#             raise Exception("Gemini model not initialized. Check API key.")
        
#         self._rate_limit()
        
#         # Language mapping
#         language_map = {
#             "hindi": "Hindi",
#             "marathi": "Marathi",
#             "bengali": "Bengali",
#             "telugu": "Telugu",
#             "tamil": "Tamil",
#             "odia": "Odia",
#             "urdu": "Urdu",
#             "kokborok": "Kokborok (Tripuri)"
#         }
        
#         language_name = language_map.get(source_language, source_language.title())
            
#         try:
#             prompt = f"""
#             You are an expert system analyzing FRA (Forest Rights Act) documents.
            
#             TASK:
#             1. Translate the {language_name} text to English
#             2. Extract structured FRA information
            
#             ORIGINAL TEXT ({language_name}):
#             {extracted_text}

#             Return ONLY a valid JSON object in this exact structure:

#             {{
#                 "translated_text": "Full English translation here...",
#                 "entities": {{
#                     "persons": [],
#                     "dependents": [],
#                     "village": "",
#                     "district": "",
#                     "state": "",
#                     "block": "",
#                     "tribe_status": "",
#                     "land_area": "",
#                     "khasra_numbers": [],
#                     "boundaries": "",
#                     "others": {{}}
#                 }},
#                 "extracted_fields": {{
#                     "patta_holder_name": "",
#                     "village_name": "",
#                     "state": "",
#                     "district": "",
#                     "block": "",
#                     "survey_number": "",
#                     "area_in_hectares": "",
#                     "coordinates": ""
#                 }}
#             }}

#             IMPORTANT RULES:
#             - Return ONLY JSON (no explanation, no markdown).
#             - Translate accurately to English.
#             - Extract all fields in English.
#             """

#             response = await self.model.generate_content_async(prompt)

#             raw = response.text.strip()
#             raw = raw.replace("```json", "").replace("```", "").strip()

#             return json.loads(raw)

#         except Exception as e:
#             if "429" in str(e) or "quota" in str(e).lower():
#                 raise Exception("Rate limit exceeded. Please wait a moment and try again.")
#             print(f"Translation + NER ERROR ({source_language}):", e)
#             return {"translated_text": "", "entities": {}, "extracted_fields": {}}

#     # -----------------------------
#     # TEXT-TO-SPEECH (Level 4)
#     # -----------------------------
#     async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
#         """Generate speech from text using gTTS."""
#         try:
#             from gtts import gTTS
            
#             # Language code mapping for gTTS
#             lang_code_map = {
#                 "hindi": "hi",
#                 "marathi": "mr",
#                 "bengali": "bn",
#                 "telugu": "te",
#                 "tamil": "ta",
#                 "odia": "or",
#                 "urdu": "ur",
#                 "kokborok": "hi",  # Fallback to Hindi (gTTS doesn't support Kokborok)
#                 "english": "en"
#             }
            
#             lang_code = lang_code_map.get(language, "en")
            
#             tts = gTTS(text=text, lang=lang_code, slow=False)
            
#             audio_bytes = io.BytesIO()
#             tts.write_to_fp(audio_bytes)
#             audio_bytes.seek(0)
            
#             return audio_bytes.read()
            
#         except ImportError:
#             raise Exception("gTTS not installed. Run: pip install gtts")
#         except Exception as e:
#             raise Exception(f"Error generating speech: {str(e)}")


# # Create service instance
# try:
#     gemini_service = GeminiService()
# except Exception as e:
#     print(f"Failed to initialize Gemini service: {e}")
#     gemini_service = None


import google.generativeai as genai
from PIL import Image
import io
import json
from typing import Dict
import time
from ..config import settings


class GeminiService:
    def __init__(self):
        try:
            # Configure Gemini API
            genai.configure(api_key=settings.GEMINI_API_KEY)

            # Use Gemini 2.5 Flash - stable, fast, and within free tier
            # Alternative: "models/gemini-flash-latest" for always-current version
            self.model = genai.GenerativeModel("models/gemini-2.5-flash")
            
            # Rate limiting
            self.last_request_time = 0
            self.min_request_interval = 1.0  # 1 second between requests
            
            print("✓ Gemini service initialized with gemini-2.5-flash")
        except Exception as e:
            print(f"WARNING: Gemini initialization failed: {e}")
            print("Make sure GEMINI_API_KEY is set in .env file")
            self.model = None

    def _rate_limit(self):
        """Ensure minimum time between API requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            print(f"Rate limiting: waiting {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

    # -----------------------------
    # IMAGE OCR
    # -----------------------------
    async def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Extract text from image using Gemini Vision OCR."""
        if not self.model:
            raise Exception("Gemini model not initialized. Check API key.")
        
        self._rate_limit()
            
        try:
            image = Image.open(io.BytesIO(image_bytes))

            prompt = """
            Extract all readable text from this document image.
            Maintain original structure. DO NOT add explanations.
            Return only the extracted text.
            Support all Indian languages including Hindi, Marathi, Bengali, Telugu, Tamil, Odia, Urdu, Kokborok.
            """

            response = await self.model.generate_content_async(
                [prompt, image]
            )

            return response.text.strip()

        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                raise Exception("Rate limit exceeded. Please wait a moment and try again.")
            raise Exception(f"Error extracting text: {str(e)}")

    # -----------------------------
    # PDF OCR
    # -----------------------------
    async def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF by converting pages to images."""
        if not self.model:
            raise Exception("Gemini model not initialized. Check API key.")
            
        try:
            from pdf2image import convert_from_path

            images = convert_from_path(pdf_path)
            full_text = []

            for i, image in enumerate(images):
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format="PNG")
                img_bytes = img_byte_arr.getvalue()

                text = await self.extract_text_from_image(img_bytes)
                full_text.append(f"--- Page {i + 1} ---\n{text}")

            return "\n\n".join(full_text)

        except ImportError:
            raise Exception("pdf2image not installed. Run: pip install pdf2image")
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    # -----------------------------
    # NER PROCESSING (English - Level 1)
    # -----------------------------
    async def perform_ner(self, extracted_text: str) -> Dict:
        """Perform Named Entity Recognition and structured extraction."""
        if not self.model:
            raise Exception("Gemini model not initialized. Check API key.")
        
        self._rate_limit()
            
        try:
            prompt = f"""
            You are an expert system analyzing FRA (Forest Rights Act) documents.
            Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.

            TEXT TO ANALYZE:
            {extracted_text}

            Return ONLY a valid JSON object in this exact structure:

            {{
                "entities": {{
                    "persons": [],
                    "dependents": [],
                    "village": "",
                    "district": "",
                    "state": "",
                    "block": "",
                    "tribe_status": "",
                    "land_area": "",
                    "khasra_numbers": [],
                    "boundaries": "",
                    "others": {{}}
                }},
                "extracted_fields": {{
                    "patta_holder_name": "",
                    "village_name": "",
                    "state": "",
                    "district": "",
                    "block": "",
                    "survey_number": "",
                    "area_in_hectares": "",
                    "coordinates": ""
                }}
            }}

            IMPORTANT RULES:
            - Return ONLY JSON (no explanation, no markdown).
            - If a field is missing in the text, return an empty string.
            """

            response = await self.model.generate_content_async(prompt)

            raw = response.text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()

            return json.loads(raw)

        except json.JSONDecodeError as e:
            print(f"NER JSON Parse Error: {e}")
            return {"entities": {}, "extracted_fields": {}}
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                raise Exception("Rate limit exceeded. Please wait a moment and try again.")
            print("NER ERROR:", e)
            return {"entities": {}, "extracted_fields": {}}

    # -----------------------------
    # NER PROCESSING (Indian Languages - Level 2)
    # -----------------------------
    async def perform_ner_native_language(self, extracted_text: str, language: str) -> Dict:
        """Perform NER on Indian language text while keeping output in native language."""
        if not self.model:
            raise Exception("Gemini model not initialized. Check API key.")
        
        self._rate_limit()
        
        # Language mapping
        language_map = {
            "hindi": "Hindi",
            "marathi": "Marathi",
            "bengali": "Bengali",
            "telugu": "Telugu",
            "tamil": "Tamil",
            "odia": "Odia",
            "urdu": "Urdu",
            "kokborok": "Kokborok (Tripuri)"
        }
        
        language_name = language_map.get(language, language.title())
            
        try:
            prompt = f"""
            You are an expert system analyzing FRA (Forest Rights Act) documents written in {language_name}.
            Perform high-accuracy Named Entity Recognition (NER) and extract structured fields.
            KEEP ALL EXTRACTED VALUES IN THE ORIGINAL {language_name.upper()} LANGUAGE.

            TEXT TO ANALYZE ({language_name}):
            {extracted_text}

            Return ONLY a valid JSON object in this exact structure:

            {{
                "entities": {{
                    "persons": [],
                    "dependents": [],
                    "village": "",
                    "district": "",
                    "state": "",
                    "block": "",
                    "tribe_status": "",
                    "land_area": "",
                    "khasra_numbers": [],
                    "boundaries": "",
                    "others": {{}}
                }},
                "extracted_fields": {{
                    "patta_holder_name": "",
                    "village_name": "",
                    "state": "",
                    "district": "",
                    "block": "",
                    "survey_number": "",
                    "area_in_hectares": "",
                    "coordinates": ""
                }}
            }}

            IMPORTANT RULES:
            - Return ONLY JSON (no explanation, no markdown).
            - Keep all values in original {language_name} script.
            - If a field is missing in the text, return an empty string.
            """

            response = await self.model.generate_content_async(prompt)

            raw = response.text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()

            return json.loads(raw)

        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                raise Exception("Rate limit exceeded. Please wait a moment and try again.")
            print(f"NER ERROR ({language}):", e)
            return {"entities": {}, "extracted_fields": {}}

    # -----------------------------
    # TRANSLATION + NER (Level 3)
    # -----------------------------
    async def translate_and_ner(self, extracted_text: str, source_language: str) -> Dict:
        """Translate any Indian language to English and perform NER."""
        if not self.model:
            raise Exception("Gemini model not initialized. Check API key.")
        
        self._rate_limit()
        
        # Language mapping
        language_map = {
            "hindi": "Hindi",
            "marathi": "Marathi",
            "bengali": "Bengali",
            "telugu": "Telugu",
            "tamil": "Tamil",
            "odia": "Odia",
            "urdu": "Urdu",
            "kokborok": "Kokborok (Tripuri)"
        }
        
        language_name = language_map.get(source_language, source_language.title())
            
        try:
            prompt = f"""
            You are an expert system analyzing FRA (Forest Rights Act) documents.
            
            TASK:
            1. Translate the {language_name} text to English
            2. Extract structured FRA information
            
            ORIGINAL TEXT ({language_name}):
            {extracted_text}

            Return ONLY a valid JSON object in this exact structure:

            {{
                "translated_text": "Full English translation here...",
                "entities": {{
                    "persons": [],
                    "dependents": [],
                    "village": "",
                    "district": "",
                    "state": "",
                    "block": "",
                    "tribe_status": "",
                    "land_area": "",
                    "khasra_numbers": [],
                    "boundaries": "",
                    "others": {{}}
                }},
                "extracted_fields": {{
                    "patta_holder_name": "",
                    "village_name": "",
                    "state": "",
                    "district": "",
                    "block": "",
                    "survey_number": "",
                    "area_in_hectares": "",
                    "coordinates": ""
                }}
            }}

            IMPORTANT RULES:
            - Return ONLY JSON (no explanation, no markdown).
            - Translate accurately to English.
            - Extract all fields in English.
            """

            response = await self.model.generate_content_async(prompt)

            raw = response.text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()

            return json.loads(raw)

        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                raise Exception("Rate limit exceeded. Please wait a moment and try again.")
            print(f"Translation + NER ERROR ({source_language}):", e)
            return {"translated_text": "", "entities": {}, "extracted_fields": {}}

    # -----------------------------
    # TEXT-TO-SPEECH (Level 4)
    # -----------------------------
    async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
        """Generate speech from text using gTTS."""
        try:
            from gtts import gTTS
            
            # Language code mapping for gTTS
            lang_code_map = {
                "hindi": "hi",
                "marathi": "mr",
                "bengali": "bn",
                "telugu": "te",
                "tamil": "ta",
                "odia": "or",
                "urdu": "ur",
                "kokborok": "hi",  # Fallback to Hindi (gTTS doesn't support Kokborok)
                "english": "en"
            }
            
            lang_code = lang_code_map.get(language, "en")
            
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            return audio_bytes.read()
            
        except ImportError:
            raise Exception("gTTS not installed. Run: pip install gtts")
        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")


# Create service instance
try:
    gemini_service = GeminiService()
except Exception as e:
    print(f"Failed to initialize Gemini service: {e}")
    gemini_service = None