# app/services/level4_questions.py

from typing import List, Dict

class Level4QuestionsService:
    """
    Service to provide form-specific questions for voice-based form filling
    Only for Form A, B, C (not annexures)
    """
    
    @staticmethod
    def get_form_a_questions() -> List[Dict]:
        """Questions for Individual Forest Rights (Form A)"""
        return [
            {
                "id": "claimant_name",
                "question_en": "What is your full name?",
                "question_hi": "आपका पूरा नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "spouse_name",
                "question_en": "What is your spouse's name?",
                "question_hi": "आपके पति या पत्नी का नाम क्या है?",
                "field_type": "text",
                "required": False
            },
            {
                "id": "father_mother_name",
                "question_en": "What is your father's or mother's name?",
                "question_hi": "आपके पिता या माता का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "address",
                "question_en": "What is your complete address?",
                "question_hi": "आपका पूरा पता क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "village",
                "question_en": "Which village do you live in?",
                "question_hi": "आप किस गाँव में रहते हैं?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "gram_panchayat",
                "question_en": "What is your Gram Panchayat name?",
                "question_hi": "आपकी ग्राम पंचायत का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "tehsil",
                "question_en": "What is your Tehsil or Block name?",
                "question_hi": "आपकी तहसील या ब्लॉक का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "district",
                "question_en": "What is your District name?",
                "question_hi": "आपके जिले का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "state",
                "question_en": "What is your State name?",
                "question_hi": "आपके राज्य का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "is_scheduled_tribe",
                "question_en": "Do you belong to a Scheduled Tribe? Please say yes or no.",
                "question_hi": "क्या आप अनुसूचित जनजाति से संबंधित हैं? कृपया हाँ या नहीं बोलें।",
                "field_type": "boolean",
                "required": True
            },
            {
                "id": "is_otfd",
                "question_en": "Are you an Other Traditional Forest Dweller? Please say yes or no.",
                "question_hi": "क्या आप अन्य पारंपरिक वन निवासी हैं? कृपया हाँ या नहीं बोलें।",
                "field_type": "boolean",
                "required": True
            },
            {
                "id": "habitation_area",
                "question_en": "What is the area of land you are living on, in hectares?",
                "question_hi": "आप जिस भूमि पर रह रहे हैं उसका क्षेत्रफल हेक्टेयर में क्या है?",
                "field_type": "number",
                "required": False
            },
            {
                "id": "cultivation_area",
                "question_en": "What is the area of land you are cultivating, in hectares?",
                "question_hi": "आप जिस भूमि पर खेती कर रहे हैं उसका क्षेत्रफल हेक्टेयर में क्या है?",
                "field_type": "number",
                "required": False
            },
            {
                "id": "khasra_numbers",
                "question_en": "What are the survey numbers or khasra numbers of your land? You can say multiple numbers separated by comma.",
                "question_hi": "आपकी भूमि के सर्वे नंबर या खसरा नंबर क्या हैं? आप अल्पविराम से अलग किए गए कई नंबर बोल सकते हैं।",
                "field_type": "array",
                "required": False
            },
            {
                "id": "geo_boundary_text",
                "question_en": "Please describe the boundaries of your land. For example, north side, south side, east side, and west side.",
                "question_hi": "कृपया अपनी भूमि की सीमाओं का वर्णन करें। उदाहरण के लिए, उत्तर दिशा, दक्षिण दिशा, पूर्व दिशा और पश्चिम दिशा।",
                "field_type": "text",
                "required": False
            },
            {
                "id": "other_traditional_rights",
                "question_en": "Do you claim any other traditional rights? Please describe them.",
                "question_hi": "क्या आप कोई अन्य पारंपरिक अधिकारों का दावा करते हैं? कृपया उनका वर्णन करें।",
                "field_type": "text",
                "required": False
            }
        ]
    
    @staticmethod
    def get_form_b_questions() -> List[Dict]:
        """Questions for Community Rights (Form B)"""
        return [
            {
                "id": "community_name",
                "question_en": "What is the name of your community or Gram Sabha?",
                "question_hi": "आपके समुदाय या ग्राम सभा का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "village",
                "question_en": "Which village is this community located in?",
                "question_hi": "यह समुदाय किस गाँव में स्थित है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "gram_panchayat",
                "question_en": "What is the Gram Panchayat name?",
                "question_hi": "ग्राम पंचायत का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "tehsil",
                "question_en": "What is the Tehsil or Block name?",
                "question_hi": "तहसील या ब्लॉक का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "district",
                "question_en": "What is the District name?",
                "question_hi": "जिले का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "state",
                "question_en": "What is the State name?",
                "question_hi": "राज्य का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "is_fdst",
                "question_en": "Does the community consist of Forest Dwelling Scheduled Tribes? Please say yes or no.",
                "question_hi": "क्या समुदाय वन निवासी अनुसूचित जनजातियों से मिलकर बना है? कृपया हाँ या नहीं बोलें।",
                "field_type": "boolean",
                "required": True
            },
            {
                "id": "is_otfd",
                "question_en": "Does the community include Other Traditional Forest Dwellers? Please say yes or no.",
                "question_hi": "क्या समुदाय में अन्य पारंपरिक वन निवासी शामिल हैं? कृपया हाँ या नहीं बोलें।",
                "field_type": "boolean",
                "required": True
            },
            {
                "id": "nistar_rights",
                "question_en": "What nistar rights does your community claim? For example, collection of forest produce.",
                "question_hi": "आपका समुदाय किन निस्तार अधिकारों का दावा करता है? उदाहरण के लिए, वन उपज का संग्रह।",
                "field_type": "text",
                "required": False
            },
            {
                "id": "minor_forest_produce",
                "question_en": "What minor forest produce does your community collect?",
                "question_hi": "आपका समुदाय कौन सी लघु वन उपज एकत्र करता है?",
                "field_type": "text",
                "required": False
            },
            {
                "id": "grazing",
                "question_en": "Does your community use forest land for grazing? Please describe.",
                "question_hi": "क्या आपका समुदाय चराई के लिए वन भूमि का उपयोग करता है? कृपया वर्णन करें।",
                "field_type": "text",
                "required": False
            },
            {
                "id": "community_uses",
                "question_en": "What other community uses of forest do you claim?",
                "question_hi": "आप वन के किन अन्य सामुदायिक उपयोगों का दावा करते हैं?",
                "field_type": "text",
                "required": False
            },
            {
                "id": "khasra_numbers",
                "question_en": "What are the survey numbers or khasra numbers of the community forest land? You can say multiple numbers separated by comma.",
                "question_hi": "सामुदायिक वन भूमि के सर्वे नंबर या खसरा नंबर क्या हैं? आप अल्पविराम से अलग किए गए कई नंबर बोल सकते हैं।",
                "field_type": "array",
                "required": False
            },
            {
                "id": "boundary_description",
                "question_en": "Please describe the boundaries of the community forest area.",
                "question_hi": "कृपया सामुदायिक वन क्षेत्र की सीमाओं का वर्णन करें।",
                "field_type": "text",
                "required": False
            }
        ]
    
    @staticmethod
    def get_form_c_questions() -> List[Dict]:
        """Questions for Community Forest Resource Rights (Form C)"""
        return [
            {
                "id": "village",
                "question_en": "Which village is claiming Community Forest Resource rights?",
                "question_hi": "कौन सा गाँव सामुदायिक वन संसाधन अधिकारों का दावा कर रहा है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "gram_panchayat",
                "question_en": "What is the Gram Panchayat name?",
                "question_hi": "ग्राम पंचायत का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "tehsil",
                "question_en": "What is the Tehsil or Block name?",
                "question_hi": "तहसील या ब्लॉक का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "district",
                "question_en": "What is the District name?",
                "question_hi": "जिले का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "state",
                "question_en": "What is the State name?",
                "question_hi": "राज्य का नाम क्या है?",
                "field_type": "text",
                "required": True
            },
            {
                "id": "cfr_map_attached",
                "question_en": "Do you have a map of the Community Forest Resource area? Please say yes or no.",
                "question_hi": "क्या आपके पास सामुदायिक वन संसाधन क्षेत्र का नक्शा है? कृपया हाँ या नहीं बोलें।",
                "field_type": "boolean",
                "required": False
            },
            {
                "id": "khasra_numbers",
                "question_en": "What are the survey numbers or khasra numbers of the CFR area? You can say multiple numbers separated by comma.",
                "question_hi": "सीएफआर क्षेत्र के सर्वे नंबर या खसरा नंबर क्या हैं? आप अल्पविराम से अलग किए गए कई नंबर बोल सकते हैं।",
                "field_type": "array",
                "required": False
            },
            {
                "id": "bordering_villages",
                "question_en": "Which villages border this Community Forest Resource area? You can say multiple village names separated by comma.",
                "question_hi": "कौन से गाँव इस सामुदायिक वन संसाधन क्षेत्र की सीमा बनाते हैं? आप अल्पविराम से अलग किए गए कई गाँव के नाम बोल सकते हैं।",
                "field_type": "array",
                "required": False
            },
            {
                "id": "boundary_description",
                "question_en": "Please describe the boundaries of the Community Forest Resource area in detail.",
                "question_hi": "कृपया सामुदायिक वन संसाधन क्षेत्र की सीमाओं का विस्तार से वर्णन करें।",
                "field_type": "text",
                "required": False
            }
        ]
    
    @staticmethod
    def get_questions_by_form_type(form_type: str) -> List[Dict]:
        """Get questions based on form type"""
        if form_type.upper() == "FORM_A":
            return Level4QuestionsService.get_form_a_questions()
        elif form_type.upper() == "FORM_B":
            return Level4QuestionsService.get_form_b_questions()
        elif form_type.upper() == "FORM_C":
            return Level4QuestionsService.get_form_c_questions()
        else:
            raise ValueError(f"Unsupported form type for Level 4: {form_type}")
    
    @staticmethod
    def parse_response(field_id: str, field_type: str, response_text: str):
        """Parse user response based on field type"""
        response_text = response_text.strip()
        
        if field_type == "boolean":
            # Handle yes/no responses in multiple languages
            yes_words = ["yes", "yeah", "yep", "हाँ", "हां", "जी", "true"]
            no_words = ["no", "nope", "नहीं", "ना", "false"]
            
            response_lower = response_text.lower()
            if any(word in response_lower for word in yes_words):
                return True
            elif any(word in response_lower for word in no_words):
                return False
            else:
                return None
        
        elif field_type == "number":
            # Extract number from text
            import re
            numbers = re.findall(r'\d+\.?\d*', response_text)
            if numbers:
                return float(numbers[0])
            return None
        
        elif field_type == "array":
            # Split by comma, semicolon, or "and"
            import re
            items = re.split(r'[,;]|\sand\s', response_text)
            return [item.strip() for item in items if item.strip()]
        
        else:  # text
            return response_text if response_text else None

level4_questions_service = Level4QuestionsService()