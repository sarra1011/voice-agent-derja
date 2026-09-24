"""Benchmark STT providers on your recordings under clean / telephony / noisy-telephony conditions.

    python -m eval.stt_bench --manifest data/manifest.csv --providers whisper,deepgram,elevenlabs
"""
from __future__ import annotations

import argparse
import csv
import os
import time

import jiwer

from eval.text_norm import normalize
from voiceagent.audio import read_wav, resample, telephony_simulate, to_wav_bytes, TARGET_SR
from voiceagent.stt import get_provider
from voiceagent.telemetry.metrics import percentiles

CONDITIONS = {
    "clean": lambda x, sr: resample(x, sr, TARGET_SR),
    "phone": lambda x, sr: telephony_simulate(x, sr, snr_db=None),
    "phone_noisy": lambda x, sr: telephony_simulate(x, sr, snr_db=10),
}


def load_manifest(path: str) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def run(manifest: str, providers: list[str], conditions: list[str], out_dir: str) -> list[dict]:
    rows_in = load_manifest(manifest)
    if not rows_in:
        raise SystemExit(f"{manifest} is empty - record audio first (make record).")
    audio = {r["id"]: read_wav(r["audio_path"]) for r in rows_in}
    results: list[dict] = []

    for pname in providers:
        try:
            provider = get_provider(pname)
        except Exception as e:  # missing key / dependency: skip this provider, keep going
            print(f"[skip] {pname}: {e}")
            continue
        for cond in conditions:
            for r in rows_in:
                x, sr = audio[r["id"]]
                wav = to_wav_bytes(CONDITIONS[cond](x, sr), TARGET_SR)
                ref = normalize(r["text"])
                hyp, err = "", ""
                t0 = time.perf_counter()
                try:
                    hyp = normalize(provider.transcribe(wav, hint=r["text"]))
                except Exception as e:
                    err = str(e)[:200]
                latency_ms = (time.perf_counter() - t0) * 1000
                results.append({
                    "provider": pname, "condition": cond, "id": r["id"], "intent": r["intent"],
                    "ref": ref, "hyp": hyp, "latency_ms": round(latency_ms, 1), "error": err,
                })
            print(f"[done] {pname} / {cond}")

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "results.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()) if results else ["provider"])
        w.writeheader()
        w.writerows(results)
    summary = summarize(results)
    write_summary(summary, os.path.join(out_dir, "summary.csv"))
    print_summary(summary)
    print(f"\nDetails: {out_dir}/results.csv   Summary: {out_dir}/summary.csv")
    return results


def summarize(results: list[dict]) -> list[dict]:
    out = []
    keys = sorted({(r["provider"], r["condition"]) for r in results})
    for provider, cond in keys:
        rows = [r for r in results if r["provider"] == provider and r["condition"] == cond]
        ok = [r for r in rows if not r["error"] and r["ref"]]
        if ok:
            refs, hyps = [r["ref"] for r in ok], [r["hyp"] for r in ok]
            wer, cer = jiwer.wer(refs, hyps), jiwer.cer(refs, hyps)
        else:
            wer = cer = float("nan")
        lat = percentiles([r["latency_ms"] for r in ok], (50, 95))
        out.append({"provider": provider, "condition": cond, "n": len(rows),
                    "errors": len(rows) - len(ok), "WER": round(wer, 3), "CER": round(cer, 3),
                    "lat_p50_ms": round(lat["p50"], 0), "lat_p95_ms": round(lat["p95"], 0)})
    return out


def write_summary(summary: list[dict], path: str) -> None:
    if not summary:
        return
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)


def print_summary(summary: list[dict]) -> None:
    if not summary:
        print("No results.")
        return
    cols = list(summary[0].keys())
    widths = [max(len(c), *(len(str(r[c])) for r in summary)) for c in cols]
    print("\n" + "  ".join(c.ljust(w) for c, w in zip(cols, widths)))
    for r in summary:
        print("  ".join(str(r[c]).ljust(w) for c, w in zip(cols, widths)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="data/manifest.csv")
    ap.add_argument("--providers", default="whisper,deepgram,elevenlabs")
    ap.add_argument("--conditions", default="clean,phone,phone_noisy")
    ap.add_argument("--out", default="results/real")
    a = ap.parse_args()
    run(a.manifest, a.providers.split(","), a.conditions.split(","), a.out)

