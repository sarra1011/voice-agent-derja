# Derja + French voice line for a public utility

Step 1 = measure before building: telemetry + STT benchmark on your own Derja/French audio.

```bash
pip install -r requirements.txt
make test            # 10 tests
make demo            # smoke test of the whole benchmark, no keys, synthetic audio

pip install -r requirements-extra.txt   # faster-whisper + sounddevice
cp .env.example .env                    # add DEEPGRAM_API_KEY / ELEVENLABS_API_KEY
make record          # records the 21 prompts in data/prompts.csv (fix the Derja first!)
make bench           # WER/CER + latency, clean vs phone vs noisy phone -> results/real/
```

- `voiceagent/audio.py`: bit-exact G.711 mu-law (Twilio), 8k<->16k, telephony simulation
- `voiceagent/telemetry/`: per-turn marks (`ts_last_user_audio_ingest` ... `ts_first_agent_audio_sent`), barge-in events, JSONL + p50/p95/p99
- `voiceagent/stt/`: swappable providers (whisper, deepgram, elevenlabs, test doubles)
- `eval/stt_bench.py`: the benchmark; `eval/text_norm.py`: Arabic/French normalization
