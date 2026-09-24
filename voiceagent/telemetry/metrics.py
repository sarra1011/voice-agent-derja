import json
from collections import defaultdict

import numpy as np


def percentiles(values, ps=(50, 95, 99)) -> dict[str, float]:
    if not len(values):
        return {f"p{p}": float("nan") for p in ps}
    arr = np.asarray(values, dtype=float)
    return {f"p{p}": float(np.percentile(arr, p)) for p in ps}


def summarize_traces(jsonl_path: str) -> dict[str, dict[str, float]]:
    """Read a traces.jsonl and return p50/p95/p99 per stage."""
    by_stage: dict[str, list[float]] = defaultdict(list)
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            for stage, ms in json.loads(line).get("latencies_ms", {}).items():
                by_stage[stage].append(ms)
    return {stage: percentiles(v) for stage, v in by_stage.items()}
