from typing import BinaryIO
from app.core.openai import client

class STT:
    def __init__(self, model: str = "whisper-1"):
        self.client = client
        self.model = model

    def transcribe_audio(self, audio_file: BinaryIO) -> str:
        try:
            transcription = self.client.audio.transcriptions.create(
                model=self.model, 
                file=audio_file, 
                )
            return transcription.text
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"
        
    def transcribe_from_path(self, file_path: str) -> str:
        """
        Transcribe audio file from path
        """
        try:
            with open(file_path, "rb") as audio_file:
                return self.transcribe_audio(audio_file)
        except FileNotFoundError:
            return "Error: Audio file not found"
        except Exception as e:
            return f"Error opening audio file: {str(e)}"