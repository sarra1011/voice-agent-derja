PY ?= python

install:
	$(PY) -m pip install -r requirements.txt

install-extra:
	$(PY) -m pip install -r requirements-extra.txt

test:
	$(PY) -m pytest -q

# Smoke test of the whole benchmark pipeline on synthetic audio (no API keys needed)
demo:
	$(PY) -m scripts.make_demo_data
	$(PY) -m eval.stt_bench --manifest data/demo_manifest.csv --providers oracle,noisy_oracle --out results/demo

# Record your own Derja/French utterances, one per prompt in data/prompts.csv
record:
	$(PY) -m scripts.record

# Real benchmark on your recordings
bench:
	$(PY) -m scripts.build_manifest
	$(PY) -m eval.stt_bench --manifest data/manifest.csv --providers whisper,deepgram,elevenlabs --out results/real
