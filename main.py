import sys
import traceback
from typing import Optional

import yt_dlp
from yt_dlp.networking.impersonate import ImpersonateTarget

try:
    import curl_cffi  # noqa: F401
    HAS_IMPERSONATE = True
except ImportError:
    HAS_IMPERSONATE = False


class MyLogger:
    """Custom logger to handle yt_dlp internal messages."""

    def debug(self, msg: str) -> None:
        if not msg.startswith('[debug] '):
            print(f"[INFO] {msg}")

    def warning(self, msg: str) -> None:
        print(f"[WARNING] {msg}")

    def error(self, msg: str) -> None:
        print(f"[ERROR] {msg}")


def progress_hook(d: dict) -> None:
    """Display download progress.

    Args:
        d: yt_dlp progress dictionary containing status and progress data.
    """
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%')
        speed = d.get('_speed_str', 'N/A')
        print(f"📥 Progress: {percent} | Speed: {speed}", end='\r')

    if d['status'] == 'finished':
        print("\n✅ Video download finished.")


def _base_ydl_opts() -> dict:
    """Return shared yt_dlp options used by both scan and download phases."""
    opts: dict = {
        'extractor_args': {'tiktok': {'api_hostname': 'api-h2.tiktokv.com'}},
    }
    if HAS_IMPERSONATE:
        opts['impersonate'] = ImpersonateTarget('chrome')
    else:
        opts['user_agent'] = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0.0.0 Safari/537.36'
        )
    return opts


def get_profile_data(user: str) -> Optional[list]:
    """Scan a TikTok profile and return its video metadata without downloading.

    Args:
        user: TikTok username (without @).

    Returns:
        List of video entry dicts (each containing at least 'url' and 'title'),
        an empty list if the profile has no public videos, or None on error.
    """
    print(f"🔍 Scanning @{user}'s profile... This may take a few seconds.")
    profile_url = f'https://www.tiktok.com/@{user}'

    ydl_opts = {
        **_base_ydl_opts(),
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(profile_url, download=False)
            return list(info['entries']) if 'entries' in info else []
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error accessing profile: {e}")
        if not error_msg:
            print("⚠️ The error message is empty. Printing full traceback:")
            traceback.print_exc()
        return None


def download_selected_videos(user: str, video_list: list, amount: int) -> None:
    """Download the first N videos from a pre-fetched list in HD.

    Args:
        user: TikTok username, used as the output subfolder name under download/.
        video_list: List of video entry dicts from get_profile_data.
        amount: Number of videos to download from the start of the list.
    """
    videos_to_process = video_list[:amount]

    ydl_opts = {
        **_base_ydl_opts(),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': f'download/{user}/%(title).50s.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
        'sleep_interval': 3,
        'max_sleep_interval': 7,
    }

    print(f"\n🚀 Starting download of {len(videos_to_process)} videos...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, video in enumerate(videos_to_process, 1):
            title = video.get('title', 'No Title')[:40]
            print(f"\n[Video {i}/{len(videos_to_process)}] Processing: {title}...")
            try:
                ydl.download([video['url']])
            except Exception as e:
                print(f"⚠️ Could not download video {i}: {e}")


if __name__ == "__main__":
    target_user = input("Enter TikTok username (without @): ").strip().lower()

    all_videos = get_profile_data(target_user)

    if all_videos is not None:
        total_found = len(all_videos)

        if total_found == 0:
            print("❌ No public videos found or the profile is private.")
            sys.exit()

        print(f"✅ Found {total_found} public videos in @{target_user}'s profile.")

        try:
            requested_count = int(
                input(f"How many videos do you want to download? (1-{total_found}): ")
            )

            if requested_count <= 0:
                print("Invalid number. Operation cancelled.")
            else:
                download_selected_videos(target_user, all_videos, requested_count)
                print(f"\n✨ All tasks completed. Files are in the 'download/{target_user}' folder.")

        except ValueError:
            print("❌ Invalid input. Please enter a whole number.")
