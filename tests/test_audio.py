import numpy as np

from voiceagent.audio import (add_noise, pcm16k_to_ulaw8k, read_wav, telephony_simulate,
                              to_wav_bytes, ulaw8k_to_pcm16k, ulaw_decode, ulaw_encode)


def test_ulaw_known_values():
    assert ulaw_encode(np.array([0], dtype=np.int16))[0] == 0xFF
    assert ulaw_decode(np.array([0xFF], dtype=np.uint8))[0] == 0


def test_ulaw_roundtrip_error_is_small():
    x = (np.sin(np.linspace(0, 60, 8000)) * 20000).astype(np.int16)
    y = ulaw_decode(ulaw_encode(x))
    big = np.abs(x) > 1000
    rel = np.abs(x[big].astype(float) - y[big]) / np.abs(x[big])
    assert rel.max() < 0.07


def test_wav_roundtrip():
    x = (np.random.default_rng(0).uniform(-0.5, 0.5, 1600)).astype(np.float32)
    y, sr = read_wav(to_wav_bytes(x, 16000))
    assert sr == 16000 and len(y) == len(x)
    assert np.max(np.abs(x - y)) < 1e-3


def test_transport_roundtrip_keeps_length_ratio():
    x = np.sin(2 * np.pi * 440 * np.arange(16000) / 16000).astype(np.float32) * 0.5
    y = ulaw8k_to_pcm16k(pcm16k_to_ulaw8k(x))
    assert abs(len(y) - len(x)) <= 4


def test_telephony_simulate_shape_and_noise():
    x = (np.random.default_rng(0).normal(0, 0.1, 16000)).astype(np.float32)
    y = telephony_simulate(x, 16000)
    assert abs(len(y) - len(x)) <= 4
    n = add_noise(x, 10, np.random.default_rng(0))
    snr = 10 * np.log10(np.mean(x ** 2) / np.mean((n - x) ** 2))
    assert 9 < snr < 11
