# import openai
# from ..config import settings
# import tempfile
# import os


# class WhisperService:
#     def __init__(self):
#         openai.api_key = settings.OPENAI_API_KEY
#         self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
#     async def transcribe_audio(self, audio_bytes: bytes, language: str = "hi") -> str:
#         """
#         Transcribe audio to text using OpenAI Whisper API.
        
#         Args:
#             audio_bytes: Audio file bytes
#             language: Language code (hi=Hindi, mr=Marathi, en=English)
        
#         Returns:
#             Transcribed text
#         """
#         try:
#             # Create temporary file for audio
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
#                 temp_audio.write(audio_bytes)
#                 temp_audio_path = temp_audio.name
            
#             try:
#                 # Open file and transcribe
#                 with open(temp_audio_path, "rb") as audio_file:
#                     transcript = self.client.audio.transcriptions.create(
#                         model="whisper-1",
#                         file=audio_file,
#                         language=language,
#                         response_format="text"
#                     )
                
#                 return transcript.strip()
            
#             finally:
#                 # Clean up temp file
#                 if os.path.exists(temp_audio_path):
#                     os.remove(temp_audio_path)
        
#         except Exception as e:
#             raise Exception(f"Error transcribing audio: {str(e)}")


# # Create service instance
# whisper_service = WhisperService()

import tempfile
import os
from ..config import settings
class WhisperService:
    def __init__(self):
        try:
            import openai
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        except ImportError:
            print("WARNING: OpenAI not installed. Run: pip install openai")
            self.client = None
        except Exception as e:
            print(f"WARNING: Whisper initialization failed: {e}")
            self.client = None
    
    async def transcribe_audio(self, audio_bytes: bytes, language: str = "hi") -> str:
        """
        Transcribe audio to text using OpenAI Whisper API.
        
        Args:
            audio_bytes: Audio file bytes
            language: Language code (hi=Hindi, mr=Marathi, en=English)
        
        Returns:
            Transcribed text
        """
        if not self.client:
            raise Exception("Whisper client not initialized. Check OpenAI API key.")
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name
            try:
                with open(temp_audio_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language=language,
                        response_format="text"
                    )
                return transcript.strip()
            finally:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")
try:
    whisper_service = WhisperService()
except Exception as e:
    print(f"Failed to initialize Whisper service: {e}")
    whisper_service = None