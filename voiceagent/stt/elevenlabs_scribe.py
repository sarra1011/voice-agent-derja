import requests

from voiceagent.config import env


class ElevenLabsScribe:
    """Batch Scribe endpoint (the streaming model is a separate websocket API)."""
    name = "elevenlabs"

    def __init__(self):
        self.key = env("ELEVENLABS_API_KEY")
        if not self.key:
            raise RuntimeError("ELEVENLABS_API_KEY is missing (see .env.example)")
        self.model_id = env("ELEVENLABS_STT_MODEL", "scribe_v1")
        self.language = env("ELEVENLABS_STT_LANGUAGE")  # empty = auto-detect

    def transcribe(self, wav: bytes, hint: str | None = None) -> str:
        data = {"model_id": self.model_id}
        if self.language:
            data["language_code"] = self.language
        r = requests.post(
            "https://api.elevenlabs.io/v1/speech-to-text",
            headers={"xi-api-key": self.key},
            data=data,
            files={"file": ("audio.wav", wav, "audio/wav")},
            timeout=120,
        )
        r.raise_for_status()
        return r.json().get("text", "")
