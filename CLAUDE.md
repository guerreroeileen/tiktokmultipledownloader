# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

Requires Python 3.7+, FFmpeg on PATH, and the following packages:

```bash
pip install -U yt-dlp
pip install curl_cffi   # optional but recommended — enables Chrome impersonation for better TikTok access
```

The project uses a `.venv` virtual environment. Activate it before running:

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

## Running

```bash
python main.py
```

The script is interactive: it prompts for a TikTok username, scans the public profile, reports total video count, then asks how many videos to download.

## Architecture

`main.py` is the entire codebase — a single-file script with three distinct phases:

1. **Profile scan** (`get_profile_data`): Uses `yt_dlp` with `extract_flat=True` to fetch video metadata only (no download). Returns a list of video entry dicts with `url` and `title`.

2. **Download** (`download_selected_videos`): Slices the entry list to the requested count, then downloads each video with `bestvideo+bestaudio` format merged into mp4 via FFmpeg. Output path is `./download/{username}/{title}.mp4`. Includes random `sleep_interval` (3–7s) between downloads.

3. **TikTok anti-bot handling**: If `curl_cffi` is installed, Chrome impersonation (`impersonate='chrome'`) is used; otherwise falls back to a Chrome user-agent string. Both phases use `api_hostname: api-h2.tiktokv.com` via `extractor_args`.

Downloaded videos land in a folder named after the username (e.g., `./someuser/`).
