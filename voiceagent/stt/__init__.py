def get_provider(name: str):
    """Lazy imports so a missing optional dependency only breaks the provider that needs it."""
    if name == "oracle":
        from .oracle import Oracle
        return Oracle()
    if name == "noisy_oracle":
        from .oracle import NoisyOracle
        return NoisyOracle()
    if name == "whisper":
        from .whisper_local import WhisperLocal
        return WhisperLocal()
    if name == "deepgram":
        from .deepgram_rest import DeepgramREST
        return DeepgramREST()
    if name == "elevenlabs":
        from .elevenlabs_scribe import ElevenLabsScribe
        return ElevenLabsScribe()
    if name == "tunispeech":
        from .tunispeech import TuniSpeechWhisper
        return TuniSpeechWhisper()
    raise ValueError(f"unknown STT provider {name!r}")

