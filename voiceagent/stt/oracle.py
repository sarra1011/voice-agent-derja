"""Test doubles: let you run the whole benchmark without API keys or models."""
import random


class Oracle:
    name = "oracle"

    def transcribe(self, wav: bytes, hint: str | None = None) -> str:
        return hint or ""


class NoisyOracle:
    """Drops ~20% of words, deterministically, to check the WER maths end to end."""
    name = "noisy_oracle"

    def __init__(self, drop: float = 0.2, seed: int = 0):
        self.drop, self.rng = drop, random.Random(seed)

    def transcribe(self, wav: bytes, hint: str | None = None) -> str:
        words = (hint or "").split()
        return " ".join(w for w in words if self.rng.random() > self.drop)
