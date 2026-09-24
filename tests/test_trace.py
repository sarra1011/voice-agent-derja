import json

from voiceagent.telemetry.metrics import summarize_traces
from voiceagent.telemetry.trace import CallTrace, JsonlSink


def fake_clock(times):
    it = iter(times)
    return lambda: next(it)


def test_latencies_and_jsonl(tmp_path):
    sink = JsonlSink(str(tmp_path / "t.jsonl"))
    tr = CallTrace("c1", sink, clock=fake_clock([0.0, 0.2, 0.5, 0.6, 0.65, 0.7]))
    turn = tr.new_turn()
    turn.mark("ts_last_user_audio_ingest")   # 0.0
    turn.mark("ts_stt_final")                # 0.2
    turn.mark("ts_llm_first_token")          # 0.5
    turn.mark("ts_tts_first_chunk")          # 0.6
    turn.mark("ts_first_agent_audio_sent")   # 0.65
    turn.event("event_barge_in", playback_cancelled=True)  # 0.7
    rec = tr.finish_turn(turn)
    lat = rec["latencies_ms"]
    assert lat["stt_final_ms"] == 200 and lat["llm_ttft_ms"] == 300
    assert lat["e2e_ms"] == 650
    line = json.loads(open(sink.path).read())
    assert line["events"][0]["event"] == "event_barge_in"
    assert summarize_traces(sink.path)["e2e_ms"]["p50"] == 650


def test_unknown_mark_rejected():
    import pytest
    turn = CallTrace("c").new_turn()
    with pytest.raises(ValueError):
        turn.mark("nope")
