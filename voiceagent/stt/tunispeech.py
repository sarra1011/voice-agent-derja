from voiceagent.audio import read_wav
from voiceagent.config import env


class TuniSpeechWhisper:
    """Whisper-large-v2 fine-tuned on ~21h of Tunisian Derja (TuniSpeech-AI/whisper-tunisian-dialect).
    Runs locally, no API key. Large download (~3GB) on first use."""
    name = "tunispeech"

    def __init__(self):
        import torch
        from transformers import pipeline

        model_id = env("TUNISPEECH_MODEL", "TuniSpeech-AI/whisper-tunisian-dialect")
        device = 0 if torch.cuda.is_available() else -1
        self.pipe = pipeline("automatic-speech-recognition", model=model_id, device=device)

    def transcribe(self, wav: bytes, hint: str | None = None) -> str:
        x, sr = read_wav(wav)  # already 16 kHz mono float32
        out = self.pipe({"array": x, "sampling_rate": sr})
        return out.get("text", "").strip()
