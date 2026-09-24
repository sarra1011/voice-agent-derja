"""Per-call / per-turn tracing with monotonic timestamps.

Usage:
    trace = CallTrace(sink=JsonlSink("logs/traces.jsonl"))
    turn = trace.new_turn()
    turn.mark("ts_last_user_audio_ingest")
    ...
    turn.mark("ts_first_agent_audio_sent")
    trace.finish_turn(turn)          # writes one JSON line
"""
from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable

MARKS = (
    "ts_last_user_audio_ingest",
    "ts_stt_final",
    "ts_llm_first_token",
    "ts_tts_first_chunk",
    "ts_first_agent_audio_sent",
)

# stage name -> (start mark, end mark)
STAGES = {
    "stt_final_ms": ("ts_last_user_audio_ingest", "ts_stt_final"),
    "llm_ttft_ms": ("ts_stt_final", "ts_llm_first_token"),
    "tts_ttfb_ms": ("ts_llm_first_token", "ts_tts_first_chunk"),
    "egress_ms": ("ts_tts_first_chunk", "ts_first_agent_audio_sent"),
    "e2e_ms": ("ts_last_user_audio_ingest", "ts_first_agent_audio_sent"),
}


@dataclass
class TurnTrace:
    call_id: str
    turn: int
    clock: Callable[[], float] = time.perf_counter
    marks: dict[str, float] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)

    def mark(self, name: str) -> float:
        if name not in MARKS:
            raise ValueError(f"unknown mark {name!r}; expected one of {MARKS}")
        self.marks[name] = self.clock()
        return self.marks[name]

    def event(self, name: str, **fields) -> None:
        """e.g. turn.event("event_barge_in", playback_cancelled=True)"""
        self.events.append({"event": name, "t": self.clock(), **fields})

    def latencies_ms(self) -> dict[str, float]:
        out = {}
        for stage, (a, b) in STAGES.items():
            if a in self.marks and b in self.marks:
                out[stage] = round((self.marks[b] - self.marks[a]) * 1000.0, 3)
        return out

    def to_dict(self) -> dict:
        return {
            "call_id": self.call_id,
            "turn": self.turn,
            "marks": self.marks,
            "events": self.events,
            "latencies_ms": self.latencies_ms(),
        }


class JsonlSink:
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.path = path

    def write(self, record: dict) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


class CallTrace:
    def __init__(self, call_id: str | None = None, sink: JsonlSink | None = None,
                 clock: Callable[[], float] = time.perf_counter):
        self.call_id = call_id or uuid.uuid4().hex[:12]
        self.sink = sink
        self.clock = clock
        self.turns: list[TurnTrace] = []

    def new_turn(self) -> TurnTrace:
        t = TurnTrace(self.call_id, len(self.turns) + 1, clock=self.clock)
        self.turns.append(t)
        return t

    def finish_turn(self, turn: TurnTrace) -> dict:
        record = turn.to_dict()
        if self.sink:
            self.sink.write(record)
        return record
