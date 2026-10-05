<div align="center">

# 🎙️ Voice Agent Derja

**An end-to-end benchmark and pipeline for Tunisian Arabic (Derja) Speech-to-Text and Voice Agent workflows.**

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-Active_Development-orange?style=for-the-badge)

<p align="center">
  <a href="#-repository-structure">Structure</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-benchmarks--evaluation">Evaluation</a> •
  <a href="#-usage">Usage</a>
</p>

---

</div>

## 📌 About The Project

`voice-agent-derja` is designed to benchmark and implement Speech-to-Text (STT) and voice agent pipelines specifically optimized for **Tunisian Arabic (Derja)**. It evaluates leading speech recognition engines (such as Whisper, Deepgram, ElevenLabs) against local audio benchmarks and provides tools for agent processing.

---

## 📁 Repository Structure

```text
voice-agent-derja/
├── 📁 audio/               # Raw audio samples for speech processing
├── 📁 data/                # Processed datasets and metadata
├── 📁 eval/                 # STT benchmarking and evaluation scripts
├── 📁 raw/                 # Unprocessed dataset files
├── 📁 scripts/              # Utility scripts for data processing and pipeline tasks
├── 📁 tests/                # Automated test suite (Pytest setup)
├── 📁 voiceagent/           # Core Voice Agent package & pipeline modules
├── 📄 .env.example         # Template for required environment secrets
├── 📄 .gitignore            # Git ignore configuration
├── 📄 Makefile              # Shortcut commands for running, testing, and building
├── 📄 pytest.ini            # Pytest configuration settings
├── 📄 requirements.txt      # Core Python dependencies
├── 📄 requirements-extra.txt# Additional optional dependencies
└── 📄 README.md             # Project documentation
