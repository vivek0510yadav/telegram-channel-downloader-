# 🚀 Ultra-Fast Telegram Lecture & Channel Downloader

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Speed: 16x Threads](https://img.shields.io/badge/Speed-16x%20Multi--Threaded-brightgreen.svg)]()
[![Auto-Resume](https://img.shields.io/badge/Auto--Resume-Enabled-success.svg)]()

A high-speed, multi-threaded Telegram channel and lecture downloader designed specifically for students and offline study. Saturates your full internet connection and automatically organizes lectures into sequential chronological order (`001_`, `002_`, `003_`...) with 1-click offline video playlists.

---

## ✨ Features

- ⚡ **16 Parallel Threads (Max Speed)**: Squeezes maximum download speed from Telegram's MTProto DC servers (up to 10x faster than standard Telegram client).
- 🔢 **Automatic Chronological Numbering**: Telegram channels often have unnumbered or randomly named lecture files. This tool tracks the exact Telegram upload timeline and prefixes files sequentially (`001_Lecture.mp4`, `002_Lecture.mp4`, etc.).
- 🎵 **1-Click Offline Playlist (`.m3u`)**: Automatically generates a VLC-compatible playlist so you can play all lectures in sequence offline without touching your keyboard.
- 🔄 **Auto-Resume on Disconnect**: If your Wi-Fi flickers or drops, it automatically pauses and resumes without re-downloading finished chunks or files.
- 🔍 **Interactive Channel Finder**: Search through your joined channels/groups by typing keywords (e.g. `upsc`, `vision`, `lectures`), or paste message links directly.
- 🎯 **Filter by Media Type**: Choose between downloading **Everything**, **Only Videos** (`.mp4`, `.mkv`), or **Only PDFs & Notes** (`.pdf`, `.docx`).
- 📦 **Zero-Config Engine**: Automatically fetches and configures the required multi-threaded core engine (`tdl`) on first run.

---

## 🚀 Quick Start (Windows)

### 1. Clone the Repository
```bash
git clone https://github.com/Vivek0510Yadav/telegram-lecture-downloader.git
cd telegram-lecture-downloader
```

### 2. Run the Downloader
Simply double-click:
```bash
START_DOWNLOAD.bat
```
*(Or run in terminal: `python download_lectures.py`)*

---

## 📖 Step-by-Step Usage

1. **Log in to Telegram (One-time only)**:
   - Choose **Option 1 (QR Code)**.
   - On your phone: Open **Telegram** $\rightarrow$ **Settings** $\rightarrow$ **Devices** $\rightarrow$ **Link Desktop Device**.
   - Point your phone camera at the terminal screen to log in instantly.
2. **Select Your Channel**:
   - Type a keyword to search your joined channels (e.g. `upsc`, `geography`, `net`), OR paste a post link (`https://t.me/c/...`).
3. **Select Download Type**:
   - `1` = All Lectures (Videos + PDFs + Notes)
   - `2` = Only Videos (`.mp4`, `.mkv`)
   - `3` = Only Notes (`.pdf`, `.docx`)
4. **Offline Access**:
   - All files are saved into the `Lectures/` folder.
   - Double-click `000_PLAY_ALL_LECTURES_IN_ORDER.m3u` in VLC or Windows Media Player to watch your course offline in chronological sequence!

---

## 📂 Output Folder Structure

```text
Lectures/
└── [Channel Name]/
    ├── 000_PLAY_ALL_LECTURES_IN_ORDER.m3u   <-- 1-Click offline playlist
    ├── 000_LECTURE_INDEX.txt                <-- Full printable lecture list
    ├── 001_Introduction.mp4                <-- Chronologically ordered
    ├── 002_Topic_01_Basics.mp4
    ├── 003_Class_Notes.pdf
    └── ...
```

---

## 🔒 Privacy & Security

- Your Telegram login session is stored strictly on your local machine (`.tdl/` folder).
- No credentials, tokens, or downloaded media are uploaded or shared.
- The `.gitignore` file is pre-configured to ensure no personal session data or downloaded media can ever be accidentally committed to git.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
