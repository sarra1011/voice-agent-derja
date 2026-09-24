from typing import Protocol


class STTProvider(Protocol):
    name: str

    def transcribe(self, wav: bytes, hint: str | None = None) -> str:
        """wav = 16 kHz mono 16-bit PCM WAV bytes. `hint` is only used by test doubles."""
        ...
