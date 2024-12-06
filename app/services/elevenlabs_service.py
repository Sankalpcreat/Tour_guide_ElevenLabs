import logging
from pathlib import Path
from datetime import datetime
import os
from elevenlabs import play, save, Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from typing import Optional, List

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElevenLabsService:
    def __init__(self, api_key: Optional[str] = None, output_dir: str = "./tour_audio"):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required")
        
        self.client = ElevenLabs(api_key=self.api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_voices(self) -> List[Voice]:
        try:
            available_voices = self.client.voices.get_all()
            logger.info(f"Retrieved {len(available_voices.voices)} voices")
            return available_voices.voices
        except Exception as e:
            logger.error(f"Failed to get voices: {e}")
            return []

    def text_to_speech(
        self,
        text: str,
        voice_name: str = "Rachel",
        output_path: Optional[str] = None
    ) -> Optional[bytes]:
        if not text.strip():
            logger.error("Empty text provided")
            return None

        try:
            audio = self.client.generate(
                text=text,
                voice=voice_name,
                model="eleven_turbo_v2_5"
            )
            
            if output_path:
                save(audio, output_path)
                logger.info(f"Audio saved to {output_path}")

            return audio
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            return None

    def generate_tour_audio(
        self,
        location_description: str,
        location_name: Optional[str] = None,
        voice_name: str = "Rachel"
    ) -> Optional[str]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = location_name if location_name else "_".join(location_description.split()[:5])
            filename = "".join(c if c.isalnum() or c == "_" else "_" for c in filename.lower())
            output_path = self.output_dir / f"{filename}_{timestamp}.mp3"
            
            audio = self.text_to_speech(
                text=location_description,
                voice_name=voice_name,
                output_path=str(output_path)
            )

            if audio and output_path.exists():
                logger.info(f"Tour audio generated: {output_path}")
                return str(output_path)

            return None
        except Exception as e:
            logger.error(f"Error generating tour audio: {e}")
            return None
