# 🎙️ AI Voice Transcriber

<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=9,12,20&height=200&section=header&text=AI%20Voice%20Transcriber&fontSize=46&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Whisper-Powered%20Transcription%20%7C%2099%20Languages%20%7C%20100%25%20Offline%20%7C%20No%20API%20Key&descAlignY=55&descSize=14)

<p>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenAI%20Whisper-Local-412991?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/99%20Languages-Supported-22C55E?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/No%20API%20Key-100%25%20Offline-brightgreen?style=for-the-badge&logo=lock"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge"/>
</p>

<p>
  <b>Upload any audio or video file → Get an accurate transcript, timestamped segments, SRT/VTT subtitles, and text statistics — all running 100% locally on your machine.</b><br/>
  Powered by OpenAI's Whisper — the same model behind industry-leading transcription services, running free on your CPU.
</p>

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [How It Works](#-how-it-works) • [Models](#-whisper-models) • [FAQ](#-faq)

</div>

---

## 🌟 Why This Project?

Most transcription tools either:
- 💸 Charge per minute (Otter.ai, Rev, Descript)
- ☁️ Upload your audio to their servers (privacy risk)
- 🔑 Require paid API keys

This tool uses **OpenAI Whisper running locally** — the same model that powers professional transcription services, completely free, with zero uploads, supporting 99 languages.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **High Accuracy** | OpenAI Whisper achieves near-human transcription accuracy |
| 🌍 **99 Languages** | Auto-detects or manually specify the audio language |
| ⏱️ **Timestamped Output** | Every segment includes precise start/end timestamps |
| 🎬 **SRT & VTT Export** | Download subtitle files ready for YouTube, VLC, Premiere |
| 📄 **Plain Text Export** | Clean transcript download as .txt |
| 🔍 **Transcript Search** | Search for any word or phrase across all segments |
| 📊 **Text Statistics** | Word count, speaking pace (WPM), reading time, sentence count |
| 🤖 **5 Model Sizes** | Choose tiny (fastest) to large (most accurate) |
| 🔒 **100% Private** | Audio never leaves your machine — zero data transmission |
| ⚡ **Smart Caching** | Whisper model loaded once and cached for the session |

---

## 🖥️ Demo

```
╔══════════════════════════════════════════════════════════════════╗
║  🎙️ AI Voice Transcriber                                         ║
║  interview_recording.mp3  │  12.4 MB  │  audio/mpeg             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ✅ Transcribed in 47.3s                                         ║
║                                                                  ║
║  📊 Stats:                                                       ║
║  ┌──────────┬───────────┬──────────┬────────┬──────────┐        ║
║  │  3,847   │    142    │  28:34   │  134   │    EN    │        ║
║  │  Words   │ Segments  │ Duration │  WPM   │ Language │        ║
║  └──────────┴───────────┴──────────┴────────┴──────────┘        ║
║                                                                  ║
║  📜 Transcript  ⏱️ Segments  📋 Summary  📥 Export  🔍 Search   ║
║  ──────────────────────────────────────────────────────────────  ║
║  [00:00]  Welcome to today's interview. I'm joined by...        ║
║  [00:14]  Thanks for having me. I've been working on AI...      ║
║  [00:28]  Let's start with how you got into machine learning... ║
║                                                                  ║
║  📥 Downloads: Plain Text │ With Timestamps │ .SRT │ .VTT       ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📦 Installation

### Prerequisites
- Python 3.9+ → [Download](https://www.python.org/downloads/)
- **ffmpeg** (required by Whisper for audio decoding)

### Install ffmpeg

**Windows:**
```bash
# Using winget
winget install ffmpeg

# Or download from https://ffmpeg.org/download.html and add to PATH
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

---

### Step 1 — Clone
```bash
git clone https://github.com/YOUR_USERNAME/ai-voice-transcriber.git
cd ai-voice-transcriber
```

### Step 2 — Virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **First run:** Whisper will auto-download the model weights. Sizes range from 39MB (tiny) to 1.5GB (large). Internet required once — then fully offline.

### Step 4 — Run
```bash
streamlit run app.py
```

Opens at **http://localhost:8501** 🎉

---

## 🤖 Whisper Models

Choose the right model for your needs:

| Model | Size | Speed | Accuracy | Best For |
|---|---|---|---|---|
| `tiny` | 39 MB | ⚡⚡⚡⚡⚡ | ⭐⭐ | Quick drafts, notes |
| `base` | 74 MB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Everyday use *(recommended)* |
| `small` | 244 MB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Interviews, podcasts |
| `medium` | 769 MB | ⚡⚡ | ⭐⭐⭐⭐⭐ | High-quality transcription |
| `large` | 1.5 GB | ⚡ | ⭐⭐⭐⭐⭐ | Maximum accuracy |

All models run on **CPU** — no GPU required!

---

## 🧠 How It Works

```
┌──────────────────────────────────────────────────────────────┐
│  User uploads audio/video file                               │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  ffmpeg decodes audio to 16kHz mono WAV                      │
│  (handles MP3, MP4, WAV, M4A, OGG, FLAC, AAC, MKV...)       │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  Whisper preprocessing                                       │
│  • Log-mel spectrogram computation (80 frequency bins)       │
│  • 30-second audio window chunking                           │
│  • Optional language detection from first 30s               │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  Whisper Encoder-Decoder Transformer                         │
│  • Audio encoder: processes spectrogram → audio features    │
│  • Text decoder: auto-regressive token generation           │
│  • Trained on 680,000 hours of multilingual audio           │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  Post-processing                                             │
│  • Segment timestamps extracted                             │
│  • Optional word-level timestamps                           │
│  • Full text assembled                                       │
└──────────────────────────┬───────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┬──────────────┐
          ▼                ▼                ▼              ▼
    📜 Transcript    ⏱️ Segments      📥 SRT/VTT     🔍 Search
```

---

## 📁 Project Structure

```
ai-voice-transcriber/
│
├── app.py              # 🧠 Main Streamlit app — all transcription logic
├── requirements.txt    # 📦 Just 3 dependencies
├── .gitignore          # 🚫 Excludes model cache, temp files
├── LICENSE             # 📄 MIT License
└── README.md           # 📖 You are here
```

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| [OpenAI Whisper](https://github.com/openai/whisper) | 20231117 | Speech-to-text model |
| [Streamlit](https://streamlit.io) | 1.35 | Web UI |
| [NumPy](https://numpy.org) | 1.26 | Audio array processing |
| [ffmpeg](https://ffmpeg.org) | system | Audio decoding & format conversion |

Only **3 pip dependencies** — incredibly lightweight stack.

---

## 📂 Supported File Formats

| Audio | Video |
|---|---|
| MP3, WAV, M4A, OGG | MP4, MKV, AVI, MOV |
| FLAC, AAC, WMA | WebM |

---

## 🤔 FAQ

**Q: Does this need an internet connection?**
> Only for the first run to download the Whisper model weights. After that, everything is 100% offline.

**Q: How fast is it?**
> Depends on the model and your CPU. On a modern laptop: `tiny` runs at ~32x realtime (1 min audio = 2 sec), `base` at ~16x. GPU users get 10x+ faster speeds.

**Q: What's the maximum file size?**
> No hard limit in the app. Very long files (1h+) may use significant RAM. For large files, use the `small` or `base` model.

**Q: Can I transcribe videos?**
> Yes! Upload MP4, MKV, AVI, MOV, or WebM — ffmpeg extracts the audio automatically.

**Q: Is the accuracy good enough for professional use?**
> Whisper `medium` and `large` achieve near-human accuracy on clear audio in English. Accuracy drops with heavy accents, multiple speakers talking simultaneously, or very noisy audio.

**Q: Can I use a GPU for faster transcription?**
> Yes! Install `torch` with CUDA support: `pip install torch --index-url https://download.pytorch.org/whl/cu118`. Whisper auto-detects and uses the GPU.

---

## 🗺️ Roadmap

- [ ] 🎤 Live microphone recording in-app
- [ ] 👥 Speaker diarization — "who said what"
- [ ] 🌐 YouTube URL input — paste link, auto-download and transcribe
- [ ] 📝 AI-powered meeting minutes generator
- [ ] 🔠 Paragraph formatting for cleaner transcripts
- [ ] 📊 Waveform visualisation with clickable timestamps
- [ ] 🌍 Translation to any language after transcription

---

## 🤝 Contributing

1. Fork this repo
2. Create a branch: `git checkout -b feature/your-idea`
3. Commit: `git commit -m 'feat: your feature'`
4. Push & open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) — the extraordinary open-source speech model
- [Streamlit](https://streamlit.io) — for making Python apps effortless
- [ffmpeg](https://ffmpeg.org) — the universal audio/video Swiss Army knife

---

<div align="center">

**⭐ If this saved you time, star the repo — it really helps!**

Made with ❤️ and Python

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=9,12,20&height=100&section=footer)

</div>
