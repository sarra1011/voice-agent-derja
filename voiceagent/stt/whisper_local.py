from voiceagent.audio import read_wav
from voiceagent.config import env


class WhisperLocal:
    name = "whisper"

    def __init__(self):
        from faster_whisper import WhisperModel  # pip install -r requirements-extra.txt

        size = env("WHISPER_MODEL", "small")
        self.language = env("WHISPER_LANGUAGE", "ar")  # set to "" in .env for auto-detect
        self.model = WhisperModel(size, device="cpu", compute_type="int8")

    def transcribe(self, wav: bytes, hint: str | None = None) -> str:
        x, _ = read_wav(wav)  # already 16 kHz mono
        segments, _info = self.model.transcribe(x, language=self.language or None, beam_size=5)
        return " ".join(s.text.strip() for s in segments).strip()

