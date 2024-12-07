import os
import tempfile
import traceback
import wave
from dataclasses import dataclass
from typing import Any, Dict

from openai import OpenAI

from app.config.env_vars import OPENAI_API_KEY


# @dataclass
# class AudioChunk:
#     data: bytes


class TranscriptionService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    async def transcribe_audio(self, audio_data: bytes) -> Dict[str, Any]:
        """Transcribe complete audio data"""
        try:
            # Validate audio data
            if not audio_data or len(audio_data) == 0:
                return {"status": "error", "message": "Invalid audio data received"}

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                with wave.open(temp_file.name, "wb") as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(16000)  # 16kHz
                    wav_file.writeframes(audio_data)

                try:
                    with open(temp_file.name, "rb") as audio_file:
                        response = self.client.audio.transcriptions.create(
                            model="whisper-1", file=audio_file, response_format="text"
                        )

                    text = response.replace("\n", "")

                except Exception as e:
                    traceback.print_exc()
                    return {
                        "status": "error",
                        "message": f"Transcription failed: {str(e)}",
                    }
                finally:
                    os.unlink(temp_file.name)

            return (
                {"text": text} if text else {"text": "", "status": "no_speech_detected"}
            )

        except Exception as e:
            print(f"[TranscriptionService] Unexpected error: {str(e)}")
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}
