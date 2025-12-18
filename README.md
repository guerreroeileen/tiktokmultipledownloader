# TikTok Profile Downloader (No Watermark) 📥

A lightweight Python-based automation tool that allows you to download a specific number of videos from any public TikTok profile without watermarks.

## 🚀 Features
* **Interactive Flow:** Scans the profile first, shows the total video count, and then asks you how many to download.
* **HD Quality:** Automatically fetches the best video and audio streams available.
* **No Watermark:** Downloads clean videos directly from TikTok's servers.
* **Anti-Ban Protection:** Includes random sleep intervals between downloads to mimic human behavior.

## 🛠️ Prerequisites
To ensure HD quality and file merging, you need:
1. **Python 3.7+**
2. **yt-dlp library:** `pip install -U yt-dlp`
3. **FFmpeg:** Required for merging HD video and audio.
   * **Windows:** Install via [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add to PATH.
   * **Mac:** `brew install ffmpeg`
   * **Linux:** `sudo apt install ffmpeg`

## 📦 Installation

1. **Clone or download** this repository.
2. **Install the required library** using pip:

    ```
    pip install -U yt-dlp
    ```

## 🖥️ Usage

1. Run the script:
    ```
    python main.py
    ```
2. Enter the TikTok username (without the @ symbol).

3. Enter the number of videos you wish to download.

note: it will create a folder ./username which contains all the downloaded videos


## ⚖️ Disclaimer
This tool is for educational purposes only. Please respect the intellectual property rights of content creators. Downloading content for redistribution without permission may violate TikTok's Terms of Service and copyright laws.