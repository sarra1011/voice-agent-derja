<div align="center">

# 🎙️ Derja Voice Agent (`voice-agent-derja`)

**An end-to-end benchmark suite and AI-powered Voice Agent framework tailored for Tunisian Arabic (Derja / الدارجة التونسية).**

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge&logo=python)
![STT Benchmark](https://img.shields.io/badge/STT-Whisper%20%7C%20Deepgram%20%7C%20ElevenLabs-purple?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-Active_Development-orange?style=for-the-badge)
![Tunisia](https://img.shields.io/badge/Region-Tunisia_%F0%9F%87%B9%F0%9F%87%B3-red?style=for-the-badge)

<p align="center">
  <a href="#-about-the-project">About</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-repository-structure">Structure</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-benchmarking--evaluation">STT Benchmarks</a> •
  <a href="#-project-roadmap">Roadmap</a>
</p>

---

</div>

## 📌 About The Project

Standard Speech-to-Text (STT) models and Voice Agents frequently struggle with regional dialects due to code-switching (mixing French, Arabic, and local slang), phonetics, and sparse training data. 

**`voice-agent-derja`** bridges this gap by providing:
1. **Benchmarking Suite:** Systematic Word Error Rate (WER) and Character Error Rate (CER) evaluation across top-tier STT providers on real Tunisian speech samples.
2. **Modular Voice Pipeline:** A specialized architecture in `voiceagent/` for processing audio inputs, dialect parsing, and generating contextual voice responses.

---

## ✨ Key Features

- 🎯 **STT Benchmark Harness:** Unified pipeline to test OpenAI Whisper, Deepgram, ElevenLabs, and custom models side-by-side.
- 🗣️ **Derja-Centric Data Pipeline:** Ingestion and preprocessing routines tuned for low-resource dialectal speech.
- 🧪 **Comprehensive Automated Testing:** Integrated `pytest` infrastructure for audio validation, evaluation logic, and agent responses.
- ⚙️️ **One-Command Workflows:** Standardized `Makefile` targets for installation, running benchmarks, linting, and running unit tests.
- 🔐 **Secure Setup:** Environment-isolated key management through `.env`.

---

## 📁 Repository Structure

```text
voice-agent-derja/
├── 📁 audio/               # Core audio dataset samples (wav/mp3)
├── 📁 data/                # Transcripts, ground truth annotations, & preprocessed datasets
├── 📁 eval/                # Benchmarking scripts (WER/CER calculators, latency metrics)
├── 📁 raw/                 # Unprocessed audio recordings and experimental captures
├── 📁 scripts/             # Data preparation, conversion, and helper utilities
├── 📁 tests/               # Unit and integration test suites (Pytest)
├── 📁 voiceagent/          # Core Python modules (Agent logic, STT connectors, TTS pipeline)
├── 📄 .env.example        # Environment variable setup (API keys for Whisper/Deepgram/etc.)
├── 📄 .gitignore           # Git version control exclusions
├── 📄 Makefile             # Automation commands for dev, test, and evaluation
├── 📄 pytest.ini           # Test runner configuration settings
├── 📄 requirements.txt     # Main production dependencies
├── 📄 requirements-extra.txt # Optional dependencies (GPU acceleration, heavy evaluation tools)
└── 📄 README.md            # Repository documentation
