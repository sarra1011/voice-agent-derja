"""Synthetic (non-speech) audio, only to smoke-test the pipeline without recordings."""
import os

import numpy as np

from voiceagent.audio import save_wav
from voiceagent.dataset import build_manifest, read_prompts

SR = 16000

if __name__ == "__main__":
    os.makedirs("data/demo_audio", exist_ok=True)
    rng = np.random.default_rng(1)
    for p in read_prompts():
        t = np.arange(int(SR * 2.5)) / SR
        f0 = rng.uniform(110, 220)
        x = sum(np.sin(2 * np.pi * f0 * k * t) / k for k in range(1, 8))
        x *= 0.15 * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t))
        save_wav(f"data/demo_audio/{p['id']}.wav", x.astype(np.float32), SR)
    n = build_manifest(audio_dir="data/demo_audio", out_csv="data/demo_manifest.csv")
    print(f"demo audio + data/demo_manifest.csv created ({n} files)")
