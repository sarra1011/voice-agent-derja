import csv
import os


def read_prompts(path: str = "data/prompts.csv") -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_manifest(prompts_csv: str = "data/prompts.csv", audio_dir: str = "data/audio",
                   out_csv: str = "data/manifest.csv") -> int:
    """Join prompts with the WAV files that exist (audio_dir/<id>.wav)."""
    rows = []
    for p in read_prompts(prompts_csv):
        wav = os.path.join(audio_dir, f"{p['id']}.wav")
        if os.path.exists(wav):
            rows.append({**p, "audio_path": wav})
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "intent", "text", "audio_path"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)

