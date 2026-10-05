<div align="center">

# 🎙️ Derja Voice Agent (voice-agent-derja)

**An AI-powered voice agent designed for understanding and processing Tunisian Arabic (Derja).**

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-Active_Development-orange?style=for-the-badge)
![Tunisia](https://img.shields.io/badge/Region-Tunisia_%F0%9F%87%B9%F0%9F%87%B3-red?style=for-the-badge)

<p align="center">
  <a href="#-about-the-project">About</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-repository-structure">Structure</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-audio-dataset">Dataset</a> •
  <a href="#-tech-stack">Tech Stack</a>
</p>

---

</div>

## 📌 About The Project

**Derja Voice Agent** is a dedicated natural language and speech processing workflow tailored specifically for the **Tunisian Arabic dialect (Derja)**. Standard Speech-to-Text (STT) and voice agents often struggle with regional dialects—this project bridges that gap by offering specialized audio processing, dataset management, and voice agent capabilities for Derja.

---

## ✨ Key Features

- 🗣️ **Derja Speech Processing:** Custom audio dataset pipeline trained on local dialect nuances.
- ⚡ **Automation with Makefile:** Pre-configured commands to run, build, and test seamlessly.
- 🔐 **Environment Configuration:** Built-in secret and environment variable management using `.env`.
- 📁 **Structured Audio Data:** Clean modular audio ingestion setup.

---

## 📁 Repository Structure

```text
voice-agent-derja/
├── 📁 audio/            # Sample audio files (U01.wav, U02.wav, U03.wav, U04.wav)
├── 📄 .env.example      # Template for environment variables
├── 📄 .gitignore         # Git ignore rules
├── 📄 Makefile           # Project automation scripts
└── 📄 README.md          # Project documentation
