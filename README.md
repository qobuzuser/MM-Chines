# 🇹🇭🇲🇲 AI-Powered Thai-Myanmar Dictionary Telegram Bot

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Built with](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![AI Engine](https://img.shields.io/badge/Powered%20By-Google%20Gemini%202.5%20Flash-green)](https://ai.google.dev/)

An advanced, high-speed Telegram Bot built to provide accurate bidirectional translation between Thai and Myanmar languages, powered by the Google Gemini 2.5 Flash model. This bot is designed for 24/7 operation using a Webhook architecture.

## ✨ Key Features

* **⚡️ Optimized Performance:** Uses the high-speed **Gemini 2.5 Flash** model and an optimized prompt structure for fast text responses.
* **🌐 Bi-Directional Translation:** Seamlessly translates between Thai $\leftrightarrow$ Myanmar.
* **📖 Detailed Dictionary Functionality:** Provides translation, context/definition, and Thai **Romanization** (English phonetic spelling).
* **📝 Extended Grammar & Usage:** The "📝 Explain More" button provides detailed explanations of grammar, usage examples, and similar words.
* **🎤 Voice Input Support:** Accepts and processes Telegram Voice Messages for transcription and translation (requires `ffmpeg`).
* **🛡️ 24/7 Webhook Operation:** Configured for robust, continuous operation using Telegram Webhooks on PaaS like Zeabur or Railway.
* **🔒 Remote Admin Control:** The `/admin` command allows the administrator to remotely toggle the bot's public ON/OFF status.

---

## 🚀 Deployment Guide

This project is containerized using Docker and is designed for deployment on platforms like Zeabur or Railway.

### 1. Prerequisites

* A **Telegram Bot Token** (from @BotFather).
* A **Gemini API Key** (Free Tier is sufficient).
* A **Docker Hub** account (for pushing the image via GitHub Actions).
* Your hosting service's **Public Domain Name** (e.g., `my-bot.zeabur.app`).

### 2. Environment Variables Setup

These variables must be set in your hosting platform's dashboard (Zeabur Variables) for the bot to run correctly in Webhook mode. **Do NOT commit your keys to GitHub.**

| Variable Name | Description | Example Value |
| :--- | :--- | :--- |
| `TELEGRAM_TOKEN` | Your BotFather Token. | `123456:AAH...` |
| `GEMINI_API_KEY` | Your Google Gemini API Key. | `AIzaSy...` |
| `ADMIN_IDS` | Your Telegram User IDs (for `/admin` access). | `123456, 987654` (Comma-separated) |
| `WEBHOOK_HOST` | The public domain name provided by your host. **(Crucial for Webhook)** | `my-bot-service.zeabur.app` |
| `PORT` | The internal port the service listens on. | `8080` (Default in `main.py`) |

### 3. Build and Deploy

1.  **Commit Code:** Commit all files (`src/` folder, `main.py`, `Dockerfile`, `.github/workflows/docker-build.yml`) to your GitHub repository.
2.  **Run GitHub Actions:** Ensure your Docker Hub credentials (`DOCKER_HUB_USERNAME`, `DOCKER_HUB_PW`) are set in GitHub Secrets. The workflow will automatically build the Docker image (`gberube/main:thai-mm`) and push it to Docker Hub.
3.  **Deploy on Zeabur:** Connect your Zeabur project to the deployed Docker image, ensuring the Environment Variables are set as instructed above. The bot will automatically start in Webhook mode, listening on port 8080.

---

## 📚 Bot Usage

The bot is designed to be highly intuitive and multilingual.

| Command / Input | Action |
| :--- | :--- |
| **`/start`** | Displays the welcome message and instructions. |
| **`/admin`** | (Admin Only) Displays the control panel to turn the bot Public ON/OFF. |
| **Text Input** | Automatically detects Thai or Myanmar and provides translation, Romanization, and Definition. |
| **Voice Input** | Transcribes and translates audio input from the Telegram Voice Message feature. |
| **📝 Explain More** | Appears under every text response. Provides deeper insight into the word/phrase, including **grammar, usage, and similar words.** |

*✨ Developed by @MyanmarTecharea*
