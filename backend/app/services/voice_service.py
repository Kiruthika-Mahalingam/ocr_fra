# # # # from groq import Groq
# # # # import openai
# # # # import tempfile
# # # # import os
# # # # from ..config import settings


# # # # class VoiceService:
# # # #     def __init__(self):
# # # #         # Initialize Groq for TTS
# # # #         try:
# # # #             self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
# # # #             print("✓ Groq service initialized (for TTS)")
# # # #         except Exception as e:
# # # #             print(f"WARNING: Groq initialization failed: {e}")
# # # #             self.groq_client = None
        
# # # #         # Initialize OpenAI for Whisper STT
# # # #         try:
# # # #             self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
# # # #             print("✓ OpenAI Whisper service initialized (for STT)")
# # # #         except Exception as e:
# # # #             print(f"WARNING: OpenAI initialization failed: {e}")
# # # #             self.openai_client = None
    
# # # #     # -------------------------
# # # #     # TEXT-TO-SPEECH using Groq
# # # #     # -------------------------
# # # #     async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
# # # #         """
# # # #         Generate speech from text using Groq TTS API.
        
# # # #         Args:
# # # #             text: Text to convert to speech
# # # #             language: Language code (hindi, marathi, english)
        
# # # #         Returns:
# # # #             Audio bytes (MP3 format)
# # # #         """
# # # #         if not self.groq_client:
# # # #             raise Exception("Groq client not initialized. Check GROQ_API_KEY.")
        
# # # #         try:
# # # #             # Groq TTS endpoint
# # # #             # Note: As of now, Groq doesn't have native TTS API
# # # #             # We'll use a workaround with gTTS for now
# # # #             # When Groq releases TTS, we can update this
            
# # # #             from gtts import gTTS
# # # #             import io
            
# # # #             # Map language to gTTS language code
# # # #             lang_code_map = {
# # # #                 "hindi": "hi",
# # # #                 "marathi": "mr",
# # # #                 "english": "en"
# # # #             }
# # # #             lang_code = lang_code_map.get(language, "en")
            
# # # #             # Generate speech using gTTS
# # # #             tts = gTTS(text=text, lang=lang_code, slow=False)
            
# # # #             audio_bytes = io.BytesIO()
# # # #             tts.write_to_fp(audio_bytes)
# # # #             audio_bytes.seek(0)
            
# # # #             return audio_bytes.read()
            
# # # #         except Exception as e:
# # # #             raise Exception(f"Error generating speech: {str(e)}")
    
# # # #     # -------------------------
# # # #     # SPEECH-TO-TEXT using OpenAI Whisper
# # # #     # -------------------------
# # # #     async def transcribe_audio(self, audio_bytes: bytes, language: str = "hi") -> str:
# # # #         """
# # # #         Transcribe audio to text using OpenAI Whisper API.
        
# # # #         Args:
# # # #             audio_bytes: Audio file bytes
# # # #             language: Language code (hi=Hindi, mr=Marathi, en=English)
        
# # # #         Returns:
# # # #             Transcribed text
# # # #         """
# # # #         if not self.openai_client:
# # # #             raise Exception("OpenAI client not initialized. Check OPENAI_API_KEY.")
        
# # # #         try:
# # # #             # Create temporary file for audio
# # # #             with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
# # # #                 temp_audio.write(audio_bytes)
# # # #                 temp_audio_path = temp_audio.name
            
# # # #             try:
# # # #                 # Open file and transcribe using OpenAI Whisper
# # # #                 with open(temp_audio_path, "rb") as audio_file:
# # # #                     transcript = self.openai_client.audio.transcriptions.create(
# # # #                         model="whisper-1",
# # # #                         file=audio_file,
# # # #                         language=language,
# # # #                         response_format="text"
# # # #                     )
                
# # # #                 return transcript.strip()
            
# # # #             finally:
# # # #                 # Clean up temp file
# # # #                 if os.path.exists(temp_audio_path):
# # # #                     os.remove(temp_audio_path)
        
# # # #         except Exception as e:
# # # #             raise Exception(f"Error transcribing audio with Whisper: {str(e)}")


# # # # # Create service instance
# # # # try:
# # # #     voice_service = VoiceService()
# # # # except Exception as e:
# # # #     print(f"Failed to initialize Voice service: {e}")
# # # #     voice_service = None


# # # import tempfile
# # # import os
# # # import io

# # # try:
# # #     from groq import Groq
# # #     GROQ_AVAILABLE = True
# # # except ImportError:
# # #     GROQ_AVAILABLE = False
# # #     print("WARNING: groq not installed. Run: pip install groq")

# # # try:
# # #     import openai
# # #     OPENAI_AVAILABLE = True
# # # except ImportError:
# # #     OPENAI_AVAILABLE = False
# # #     print("WARNING: openai not installed. Run: pip install openai")

# # # try:
# # #     from gtts import gTTS
# # #     GTTS_AVAILABLE = True
# # # except ImportError:
# # #     GTTS_AVAILABLE = False
# # #     print("WARNING: gtts not installed. Run: pip install gtts")

# # # from ..config import settings


# # # class VoiceService:
# # #     def __init__(self):
# # #         self.groq_client = None
# # #         self.openai_client = None
        
# # #         # Initialize Groq (for future TTS)
# # #         if GROQ_AVAILABLE:
# # #             try:
# # #                 if hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
# # #                     # Fix: Don't pass any extra arguments
# # #                     self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
# # #                     print("✓ Groq client initialized")
# # #                 else:
# # #                     print("⚠️  GROQ_API_KEY not set in .env")
# # #             except Exception as e:
# # #                 print(f"⚠️  Groq initialization failed: {e}")
# # #                 self.groq_client = None
        
# # #         # Initialize OpenAI Whisper (for STT)
# # #         if OPENAI_AVAILABLE:
# # #             try:
# # #                 if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
# # #                     # Fix: Use the correct initialization
# # #                     self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
# # #                     print("✓ OpenAI Whisper client initialized")
# # #                 else:
# # #                     print("⚠️  OPENAI_API_KEY not set in .env")
# # #             except Exception as e:
# # #                 print(f"⚠️  OpenAI initialization failed: {e}")
# # #                 self.openai_client = None
    
# # #     # -------------------------
# # #     # TEXT-TO-SPEECH using gTTS
# # #     # -------------------------
# # #     async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
# # #         """
# # #         Generate speech from text using gTTS.
# # #         Falls back to gTTS since Groq doesn't have native TTS yet.
        
# # #         Args:
# # #             text: Text to convert to speech
# # #             language: Language code (hindi, marathi, english)
        
# # #         Returns:
# # #             Audio bytes (MP3 format)
# # #         """
# # #         if not GTTS_AVAILABLE:
# # #             raise Exception("gTTS not installed. Run: pip install gtts")
        
# # #         try:
# # #             # Map language to gTTS language code
# # #             lang_code_map = {
# # #                 "hindi": "hi",
# # #                 "marathi": "mr",
# # #                 "english": "en"
# # #             }
# # #             lang_code = lang_code_map.get(language, "en")
            
# # #             print(f"Generating TTS: text='{text[:50]}...', lang={lang_code}")
            
# # #             # Generate speech using gTTS
# # #             tts = gTTS(text=text, lang=lang_code, slow=False)
            
# # #             audio_bytes = io.BytesIO()
# # #             tts.write_to_fp(audio_bytes)
# # #             audio_bytes.seek(0)
            
# # #             result = audio_bytes.read()
# # #             print(f"✓ TTS generated: {len(result)} bytes")
            
# # #             return result
            
# # #         except Exception as e:
# # #             print(f"✗ TTS Error: {e}")
# # #             raise Exception(f"Error generating speech: {str(e)}")
    
# # #     # -------------------------
# # #     # SPEECH-TO-TEXT using OpenAI Whisper
# # #     # -------------------------
# # #     async def transcribe_audio(self, audio_bytes: bytes, language: str = "hi") -> str:
# # #         """
# # #         Transcribe audio to text using OpenAI Whisper API.
        
# # #         Args:
# # #             audio_bytes: Audio file bytes
# # #             language: Language code (hi=Hindi, mr=Marathi, en=English)
        
# # #         Returns:
# # #             Transcribed text
# # #         """
# # #         if not self.openai_client:
# # #             raise Exception("OpenAI Whisper not initialized. Check OPENAI_API_KEY in .env file")
        
# # #         if not audio_bytes or len(audio_bytes) == 0:
# # #             raise Exception("Empty audio file received")
        
# # #         try:
# # #             print(f"Transcribing audio: {len(audio_bytes)} bytes, lang={language}")
            
# # #             # Create temporary file for audio
# # #             with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
# # #                 temp_audio.write(audio_bytes)
# # #                 temp_audio_path = temp_audio.name
            
# # #             try:
# # #                 # Open file and transcribe using OpenAI Whisper
# # #                 with open(temp_audio_path, "rb") as audio_file:
# # #                     transcript = self.openai_client.audio.transcriptions.create(
# # #                         model="whisper-1",
# # #                         file=audio_file,
# # #                         language=language,
# # #                         response_format="text"
# # #                     )
                
# # #                 result = transcript.strip()
# # #                 print(f"✓ Transcription: '{result}'")
                
# # #                 return result
            
# # #             finally:
# # #                 # Clean up temp file
# # #                 try:
# # #                     if os.path.exists(temp_audio_path):
# # #                         os.remove(temp_audio_path)
# # #                 except Exception as e:
# # #                     print(f"Warning: Could not delete temp file: {e}")
        
# # #         except Exception as e:
# # #             print(f"✗ STT Error: {e}")
# # #             raise Exception(f"Error transcribing audio: {str(e)}")


# # # # Create service instance
# # # try:
# # #     voice_service = VoiceService()
# # #     print("✓ Voice service created")
# # # except Exception as e:
# # #     print(f"✗ Failed to create voice service: {e}")
# # #     voice_service = None


# # import tempfile
# # import os
# # import io

# # try:
# #     import openai
# #     OPENAI_AVAILABLE = True
# # except ImportError:
# #     OPENAI_AVAILABLE = False
# #     print("WARNING: openai not installed. Run: pip install openai")

# # try:
# #     from gtts import gTTS
# #     GTTS_AVAILABLE = True
# # except ImportError:
# #     GTTS_AVAILABLE = False
# #     print("WARNING: gtts not installed. Run: pip install gtts")

# # from ..config import settings


# # class VoiceService:
# #     def __init__(self):
# #         self.openai_client = None
        
# #         # Initialize OpenAI Whisper (for STT)
# #         if OPENAI_AVAILABLE:
# #             try:
# #                 api_key = getattr(settings, 'OPENAI_API_KEY', None)
                
# #                 if api_key:
# #                     print(f"Initializing OpenAI with key: {api_key[:10]}...")
# #                     # Simple initialization
# #                     self.openai_client = openai.OpenAI(api_key=api_key)
                    
# #                     # Test the client
# #                     try:
# #                         # Try to list models to verify connection
# #                         models = self.openai_client.models.list()
# #                         print("✓ OpenAI Whisper client initialized and verified")
# #                     except Exception as test_error:
# #                         print(f"⚠️  OpenAI client created but test failed: {test_error}")
# #                         # Keep the client anyway, it might work
# #                 else:
# #                     print("⚠️  OPENAI_API_KEY not set in .env")
# #             except Exception as e:
# #                 print(f"⚠️  OpenAI initialization failed: {e}")
# #                 import traceback
# #                 traceback.print_exc()
# #                 self.openai_client = None
# #         else:
# #             print("⚠️  openai package not installed")
    
# #     # -------------------------
# #     # TEXT-TO-SPEECH using gTTS
# #     # -------------------------
# #     async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
# #         """
# #         Generate speech from text using gTTS.
        
# #         Args:
# #             text: Text to convert to speech
# #             language: Language code (hindi, marathi, english)
        
# #         Returns:
# #             Audio bytes (MP3 format)
# #         """
# #         if not GTTS_AVAILABLE:
# #             raise Exception("gTTS not installed. Run: pip install gtts")
        
# #         try:
# #             # Map language to gTTS language code
# #             lang_code_map = {
# #                 "hindi": "hi",
# #                 "marathi": "mr",
# #                 "english": "en"
# #             }
# #             lang_code = lang_code_map.get(language, "en")
            
# #             print(f"Generating TTS: text='{text[:50]}...', lang={lang_code}")
            
# #             # Generate speech using gTTS
# #             tts = gTTS(text=text, lang=lang_code, slow=False)
            
# #             audio_bytes = io.BytesIO()
# #             tts.write_to_fp(audio_bytes)
# #             audio_bytes.seek(0)
            
# #             result = audio_bytes.read()
# #             print(f"✓ TTS generated: {len(result)} bytes")
            
# #             return result
            
# #         except Exception as e:
# #             print(f"✗ TTS Error: {e}")
# #             raise Exception(f"Error generating speech: {str(e)}")
    
# #     # -------------------------
# #     # SPEECH-TO-TEXT using OpenAI Whisper
# #     # -------------------------
# #     async def transcribe_audio(self, audio_bytes: bytes, language: str = "hi") -> str:
# #         """
# #         Transcribe audio to text using OpenAI Whisper API.
        
# #         Args:
# #             audio_bytes: Audio file bytes
# #             language: Language code (hi=Hindi, mr=Marathi, en=English)
        
# #         Returns:
# #             Transcribed text
# #         """
# #         print(f"Transcribe called: openai_client={self.openai_client is not None}")
        
# #         if not self.openai_client:
# #             raise Exception("OpenAI Whisper not initialized. Check OPENAI_API_KEY in .env file")
        
# #         if not audio_bytes or len(audio_bytes) == 0:
# #             raise Exception("Empty audio file received")
        
# #         try:
# #             print(f"Transcribing audio: {len(audio_bytes)} bytes, lang={language}")
            
# #             # Create temporary file for audio
# #             with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
# #                 temp_audio.write(audio_bytes)
# #                 temp_audio_path = temp_audio.name
            
# #             try:
# #                 # Open file and transcribe using OpenAI Whisper
# #                 with open(temp_audio_path, "rb") as audio_file:
# #                     print(f"Sending to OpenAI Whisper...")
# #                     transcript = self.openai_client.audio.transcriptions.create(
# #                         model="whisper-1",
# #                         file=audio_file,
# #                         language=language,
# #                         response_format="text"
# #                     )
                
# #                 result = transcript.strip()
# #                 print(f"✓ Transcription: '{result}'")
                
# #                 return result
            
# #             finally:
# #                 # Clean up temp file
# #                 try:
# #                     if os.path.exists(temp_audio_path):
# #                         os.remove(temp_audio_path)
# #                 except Exception as e:
# #                     print(f"Warning: Could not delete temp file: {e}")
        
# #         except Exception as e:
# #             print(f"✗ STT Error: {e}")
# #             import traceback
# #             traceback.print_exc()
# #             raise Exception(f"Error transcribing audio: {str(e)}")


# # # Create service instance
# # print("Creating voice service...")
# # try:
# #     voice_service = VoiceService()
# #     print(f"✓ Voice service created (openai_client: {voice_service.openai_client is not None})")
# # except Exception as e:
# #     print(f"✗ Failed to create voice service: {e}")
# #     import traceback
# #     traceback.print_exc()
# #     voice_service = None


# import tempfile
# import os
# import io

# try:
#     from openai import OpenAI
#     OPENAI_AVAILABLE = True
# except ImportError:
#     OPENAI_AVAILABLE = False
#     print("WARNING: openai not installed. Run: pip install openai")

# try:
#     from gtts import gTTS
#     GTTS_AVAILABLE = True
# except ImportError:
#     GTTS_AVAILABLE = False
#     print("WARNING: gtts not installed. Run: pip install gtts")

# from ..config import settings


# class VoiceService:
#     def __init__(self):
#         self.openai_client = None
        
#         # Initialize OpenAI Whisper (for STT)
#         if OPENAI_AVAILABLE:
#             try:
#                 api_key = getattr(settings, 'OPENAI_API_KEY', None)
                
#                 if api_key:
#                     print(f"Initializing OpenAI with key: {api_key[:10]}...")
                    
#                     # Create client WITHOUT any proxy settings
#                     # This avoids the 'proxies' argument error
#                     self.openai_client = OpenAI(
#                         api_key=api_key,
#                         # Don't pass any other arguments that might cause issues
#                     )
                    
#                     print("✓ OpenAI Whisper client initialized")
#                 else:
#                     print("⚠️  OPENAI_API_KEY not set in .env")
#             except TypeError as e:
#                 if 'proxies' in str(e):
#                     print("⚠️  Proxies issue detected, trying alternative initialization...")
#                     try:
#                         # Alternative: Set environment variable instead
#                         os.environ['OPENAI_API_KEY'] = api_key
#                         self.openai_client = OpenAI()
#                         print("✓ OpenAI client initialized (alternative method)")
#                     except Exception as e2:
#                         print(f"⚠️  Alternative initialization also failed: {e2}")
#                         self.openai_client = None
#                 else:
#                     print(f"⚠️  OpenAI initialization failed: {e}")
#                     self.openai_client = None
#             except Exception as e:
#                 print(f"⚠️  OpenAI initialization failed: {e}")
#                 import traceback
#                 traceback.print_exc()
#                 self.openai_client = None
#         else:
#             print("⚠️  openai package not installed")
    
#     # -------------------------
#     # TEXT-TO-SPEECH using gTTS
#     # -------------------------
#     async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
#         """
#         Generate speech from text using gTTS.
        
#         Args:
#             text: Text to convert to speech
#             language: Language code (hindi, marathi, english)
        
#         Returns:
#             Audio bytes (MP3 format)
#         """
#         if not GTTS_AVAILABLE:
#             raise Exception("gTTS not installed. Run: pip install gtts")
        
#         try:
#             # Map language to gTTS language code
#             lang_code_map = {
#                 "hindi": "hi",
#                 "marathi": "mr",
#                 "english": "en"
#             }
#             lang_code = lang_code_map.get(language, "en")
            
#             print(f"Generating TTS: text='{text[:50]}...', lang={lang_code}")
            
#             # Generate speech using gTTS
#             tts = gTTS(text=text, lang=lang_code, slow=False)
            
#             audio_bytes = io.BytesIO()
#             tts.write_to_fp(audio_bytes)
#             audio_bytes.seek(0)
            
#             result = audio_bytes.read()
#             print(f"✓ TTS generated: {len(result)} bytes")
            
#             return result
            
#         except Exception as e:
#             print(f"✗ TTS Error: {e}")
#             raise Exception(f"Error generating speech: {str(e)}")
    
#     # -------------------------
#     # SPEECH-TO-TEXT using OpenAI Whisper
#     # -------------------------
#     async def transcribe_audio(self, audio_bytes: bytes, language: str = "hi") -> str:
#         """
#         Transcribe audio to text using OpenAI Whisper API.
        
#         Args:
#             audio_bytes: Audio file bytes
#             language: Language code (hi=Hindi, mr=Marathi, en=English)
        
#         Returns:
#             Transcribed text
#         """
#         if not self.openai_client:
#             raise Exception("OpenAI Whisper not initialized. Check OPENAI_API_KEY in .env file")
        
#         if not audio_bytes or len(audio_bytes) == 0:
#             raise Exception("Empty audio file received")
        
#         try:
#             print(f"Transcribing audio: {len(audio_bytes)} bytes, lang={language}")
            
#             # Create temporary file for audio
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
#                 temp_audio.write(audio_bytes)
#                 temp_audio_path = temp_audio.name
            
#             try:
#                 # Open file and transcribe using OpenAI Whisper
#                 with open(temp_audio_path, "rb") as audio_file:
#                     print(f"Sending to OpenAI Whisper...")
#                     transcript = self.openai_client.audio.transcriptions.create(
#                         model="whisper-1",
#                         file=audio_file,
#                         language=language,
#                         response_format="text"
#                     )
                
#                 result = transcript.strip()
#                 print(f"✓ Transcription: '{result}'")
                
#                 return result
            
#             finally:
#                 # Clean up temp file
#                 try:
#                     if os.path.exists(temp_audio_path):
#                         os.remove(temp_audio_path)
#                 except Exception as e:
#                     print(f"Warning: Could not delete temp file: {e}")
        
#         except Exception as e:
#             print(f"✗ STT Error: {e}")
#             import traceback
#             traceback.print_exc()
#             raise Exception(f"Error transcribing audio: {str(e)}")


# # Create service instance
# print("Creating voice service...")
# try:
#     voice_service = VoiceService()
#     if voice_service.openai_client:
#         print(f"✓ Voice service created successfully")
#     else:
#         print(f"⚠️  Voice service created but OpenAI client not initialized")
# except Exception as e:
#     print(f"✗ Failed to create voice service: {e}")
#     import traceback
#     traceback.print_exc()
#     voice_service = None



import tempfile
import os
import io

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("WARNING: openai not installed. Run: pip install openai")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("WARNING: gtts not installed. Run: pip install gtts")

from ..config import settings


class VoiceService:
    def __init__(self):
        self.openai_client = None
        
        # Initialize OpenAI Whisper (for STT)
        if OPENAI_AVAILABLE:
            try:
                api_key = getattr(settings, 'OPENAI_API_KEY', None)
                
                if api_key:
                    print(f"Initializing OpenAI with key: {api_key[:10]}...")
                    
                    # Create client WITHOUT any proxy settings
                    self.openai_client = OpenAI(
                        api_key=api_key,
                    )
                    
                    print("✓ OpenAI Whisper client initialized")
                else:
                    print("⚠️  OPENAI_API_KEY not set in .env")
            except TypeError as e:
                if 'proxies' in str(e):
                    print("⚠️  Proxies issue detected, trying alternative initialization...")
                    try:
                        # Alternative: Set environment variable instead
                        os.environ['OPENAI_API_KEY'] = api_key
                        self.openai_client = OpenAI()
                        print("✓ OpenAI client initialized (alternative method)")
                    except Exception as e2:
                        print(f"⚠️  Alternative initialization also failed: {e2}")
                        self.openai_client = None
                else:
                    print(f"⚠️  OpenAI initialization failed: {e}")
                    self.openai_client = None
            except Exception as e:
                print(f"⚠️  OpenAI initialization failed: {e}")
                import traceback
                traceback.print_exc()
                self.openai_client = None
        else:
            print("⚠️  openai package not installed")
    
    # -------------------------
    # TEXT-TO-SPEECH using gTTS
    # -------------------------
    async def generate_speech(self, text: str, language: str = "hindi") -> bytes:
        """
        Generate speech from text using gTTS.
        
        Args:
            text: Text to convert to speech
            language: Language code (hindi, marathi, english)
        
        Returns:
            Audio bytes (MP3 format)
        """
        if not GTTS_AVAILABLE:
            raise Exception("gTTS not installed. Run: pip install gtts")
        
        try:
            # Map language to gTTS language code
            lang_code_map = {
                "hindi": "hi",
                "marathi": "mr",
                "english": "en"
            }
            lang_code = lang_code_map.get(language, "en")
            
            print(f"Generating TTS: text='{text[:50]}...', lang={lang_code}")
            
            # Generate speech using gTTS
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            result = audio_bytes.read()
            print(f"✓ TTS generated: {len(result)} bytes")
            
            return result
            
        except Exception as e:
            print(f"✗ TTS Error: {e}")
            raise Exception(f"Error generating speech: {str(e)}")
    
    # -------------------------
    # SPEECH-TO-TEXT using OpenAI Whisper (FIXED VERSION)
    # -------------------------
    async def transcribe_audio(self, audio_bytes: bytes, language: str = "hi") -> str:
        """
        Transcribe audio to text using OpenAI Whisper API.
        
        Args:
            audio_bytes: Audio file bytes
            language: Language code (hi=Hindi, mr=Marathi, en=English)
        
        Returns:
            Transcribed text
        """
        # Better error message
        if not self.openai_client:
            raise Exception(
                "OpenAI Whisper not initialized. "
                "Please set OPENAI_API_KEY in your .env file. "
                "Get your API key from: https://platform.openai.com/api-keys"
            )
        
        if not audio_bytes or len(audio_bytes) == 0:
            raise Exception("Empty audio file received")
        
        try:
            print(f"Transcribing audio: {len(audio_bytes)} bytes, lang={language}")
            
            # Try multiple audio formats - webm might not work
            temp_audio_path = None
            
            try:
                # Create temporary file - try .mp3 first, then .webm
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                    temp_audio.write(audio_bytes)
                    temp_audio_path = temp_audio.name
                
                # Open file and transcribe using OpenAI Whisper
                with open(temp_audio_path, "rb") as audio_file:
                    print(f"Sending to OpenAI Whisper (file: {temp_audio_path})...")
                    
                    # Whisper API call
                    transcript = self.openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language=language,  # hi, en, mr
                        response_format="text"
                    )
                
                # Handle both string and object responses
                if isinstance(transcript, str):
                    result = transcript.strip()
                else:
                    result = transcript.text.strip() if hasattr(transcript, 'text') else str(transcript).strip()
                
                print(f"✓ Transcription successful: '{result[:100]}...'")
                return result
                
            finally:
                # Clean up temp file
                if temp_audio_path and os.path.exists(temp_audio_path):
                    try:
                        os.remove(temp_audio_path)
                        print(f"✓ Cleaned up temp file")
                    except Exception as cleanup_error:
                        print(f"⚠️  Could not delete temp file: {cleanup_error}")
        
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Transcription Error: {error_msg}")
            import traceback
            traceback.print_exc()
            
            # Provide helpful error messages
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                raise Exception(
                    "OpenAI API authentication failed. "
                    "Check your OPENAI_API_KEY in .env file"
                )
            elif "billing" in error_msg.lower() or "quota" in error_msg.lower():
                raise Exception(
                    "OpenAI API quota exceeded or billing issue. "
                    "Check your OpenAI account at https://platform.openai.com"
                )
            else:
                raise Exception(f"Transcription failed: {error_msg}")


# Create service instance
print("Creating voice service...")
try:
    voice_service = VoiceService()
    if voice_service.openai_client:
        print(f"✓ Voice service created successfully")
    else:
        print(f"⚠️  Voice service created but OpenAI client not initialized")
except Exception as e:
    print(f"✗ Failed to create voice service: {e}")
    import traceback
    traceback.print_exc()
    voice_service = None