"""Record one WAV per prompt: press Enter to start, Enter to stop. Skips prompts already recorded.
Needs: pip install -r requirements-extra.txt  (sounddevice)"""
import os

import numpy as np

from voiceagent.audio import save_wav
from voiceagent.dataset import build_manifest, read_prompts

SR = 16000

if __name__ == "__main__":
    import sounddevice as sd

    os.makedirs("data/audio", exist_ok=True)
    for p in read_prompts():
        path = f"data/audio/{p['id']}.wav"
        if os.path.exists(path):
            continue
        print(f"\n[{p['id']}] ({p['intent']})\n  {p['text']}")
        while True:
            input("  Enter = start recording... ")
            chunks = []
            with sd.InputStream(samplerate=SR, channels=1, dtype="float32",
                                callback=lambda d, *_: chunks.append(d.copy())):
                input("  Recording... Enter = stop ")
            x = np.concatenate(chunks).ravel() if chunks else np.zeros(0, np.float32)
            print(f"  {len(x) / SR:.1f}s recorded")
            if input("  Keep it? [Y/n] ").strip().lower() != "n":
                save_wav(path, x, SR)
                break
    print(f"\nmanifest: {build_manifest()} recordings -> data/manifest.csv")
