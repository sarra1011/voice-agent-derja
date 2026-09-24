"""Audio helpers: WAV I/O, resampling, G.711 mu-law, and telephony simulation.

Pure numpy/scipy (Python 3.13 removed `audioop`).
"""
from __future__ import annotations

import io
import wave
from math import gcd

import numpy as np
from scipy.signal import butter, resample_poly, sosfilt

TARGET_SR = 16000
TELEPHONY_SR = 8000


# ---------- WAV I/O ----------
def read_wav(src: str | bytes) -> tuple[np.ndarray, int]:
    """Return (mono float32 in [-1, 1], sample_rate). Only 16-bit PCM WAV."""
    f = io.BytesIO(src) if isinstance(src, (bytes, bytearray)) else src
    with wave.open(f, "rb") as w:
        if w.getsampwidth() != 2:
            raise ValueError("Only 16-bit PCM WAV is supported. Convert with: "
                             "ffmpeg -i in.xxx -ar 16000 -ac 1 -sample_fmt s16 out.wav")
        sr, ch = w.getframerate(), w.getnchannels()
        raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x, sr


def to_wav_bytes(x: np.ndarray, sr: int) -> bytes:
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    return buf.getvalue()


def save_wav(path: str, x: np.ndarray, sr: int) -> None:
    with open(path, "wb") as f:
        f.write(to_wav_bytes(x, sr))


def resample(x: np.ndarray, sr_in: int, sr_out: int) -> np.ndarray:
    if sr_in == sr_out:
        return x
    g = gcd(sr_in, sr_out)
    return resample_poly(x, sr_out // g, sr_in // g).astype(np.float32)


# ---------- G.711 mu-law (bit-exact with the standard, e.g. Twilio media streams) ----------
def ulaw_encode(pcm16: np.ndarray) -> np.ndarray:
    x = pcm16.astype(np.int32)
    sign = np.where(x < 0, 0x80, 0)
    x = np.minimum(np.abs(x), 32635) + 0x84
    exponent = np.frexp(x.astype(np.float64))[1] - 1 - 7  # floor(log2(x)) - 7
    mantissa = (x >> (exponent + 3)) & 0x0F
    return (~(sign | (exponent << 4) | mantissa) & 0xFF).astype(np.uint8)


def ulaw_decode(ulaw: np.ndarray) -> np.ndarray:
    u = (~ulaw.astype(np.int32)) & 0xFF
    sign = u & 0x80
    exponent = (u >> 4) & 0x07
    mantissa = u & 0x0F
    sample = (((mantissa << 3) + 0x84) << exponent) - 0x84
    return np.where(sign != 0, -sample, sample).astype(np.int16)


def ulaw8k_to_pcm16k(ulaw_bytes: bytes) -> np.ndarray:
    """Telephony frame (8 kHz mu-law bytes) -> float32 16 kHz, ready for STT."""
    pcm = ulaw_decode(np.frombuffer(ulaw_bytes, dtype=np.uint8)).astype(np.float32) / 32768.0
    return resample(pcm, TELEPHONY_SR, TARGET_SR)


def pcm16k_to_ulaw8k(x: np.ndarray) -> bytes:
    """float32 16 kHz (e.g. TTS output) -> 8 kHz mu-law bytes for the phone leg."""
    x8 = resample(x, TARGET_SR, TELEPHONY_SR)
    pcm = (np.clip(x8, -1.0, 1.0) * 32767.0).astype(np.int16)
    return ulaw_encode(pcm).tobytes()


# ---------- Telephony simulation (for benchmarking on clean recordings) ----------
def add_noise(x: np.ndarray, snr_db: float, rng: np.random.Generator) -> np.ndarray:
    p_signal = float(np.mean(x ** 2))
    if p_signal == 0:
        return x
    p_noise = p_signal / (10 ** (snr_db / 10))
    return (x + rng.normal(0.0, np.sqrt(p_noise), size=x.shape)).astype(np.float32)


def telephony_simulate(x: np.ndarray, sr: int, snr_db: float | None = None,
                       seed: int = 0) -> np.ndarray:
    """Clean speech -> what an STT sees on a phone call: 8 kHz, 300-3400 Hz band,
    optional additive noise, mu-law companding. Returned at 16 kHz."""
    rng = np.random.default_rng(seed)
    y = resample(x, sr, TELEPHONY_SR)
    sos = butter(4, [300, 3400], btype="bandpass", fs=TELEPHONY_SR, output="sos")
    y = sosfilt(sos, y).astype(np.float32)
    if snr_db is not None:
        y = add_noise(y, snr_db, rng)
    pcm = (np.clip(y, -1.0, 1.0) * 32767.0).astype(np.int16)
    y = ulaw_decode(ulaw_encode(pcm)).astype(np.float32) / 32768.0
    return resample(y, TELEPHONY_SR, TARGET_SR)
