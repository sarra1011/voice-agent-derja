import requests

from voiceagent.config import env


class DeepgramREST:
    """Pre-recorded endpoint, used for accuracy + rough latency comparison.
    Check the Deepgram docs for which language codes your chosen model supports."""
    name = "deepgram"

    def __init__(self):
        self.key = env("DEEPGRAM_API_KEY")
        if not self.key:
            raise RuntimeError("DEEPGRAM_API_KEY is missing (see .env.example)")
        self.params = {
            "model": env("DEEPGRAM_MODEL", "nova-3"),
            "language": env("DEEPGRAM_LANGUAGE", "multi"),
            "smart_format": "true",
        }

    def transcribe(self, wav: bytes, hint: str | None = None) -> str:
        r = requests.post(
            "https://api.deepgram.com/v1/listen",
            params=self.params,
            headers={"Authorization": f"Token {self.key}", "Content-Type": "audio/wav"},
            data=wav,
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["results"]["channels"][0]["alternatives"][0]["transcript"]
