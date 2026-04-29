import yt_dlp
from yt_dlp.networking.impersonate import ImpersonateTarget
import sys
import traceback

try:
    import curl_cffi
    HAS_IMPERSONATE = True
except ImportError:
    HAS_IMPERSONATE = False

class MyLogger:
    """
    Custom logger class to handle yt_dlp internal messages.
    """
    def debug(self, msg):
        if not msg.startswith('[debug] '):
            print(f"[INFO] {msg}")

    def warning(self, msg):
        print(f"[WARNING] {msg}")

    def error(self, msg):
        print(f"[ERROR] {msg}")

def progress_hook(d):
    """
    Displays progress during the download process.
    """
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%')
        speed = d.get('_speed_str', 'N/A')
        print(f"📥 Progress: {percent} | Speed: {speed}", end='\r')
    
    if d['status'] == 'finished':
        print(f"\n✅ Video download finished.")

def get_profile_data(user):
    """
    Scans the profile to get the list of available videos without downloading them yet.
    """
    print(f"🔍 Scanning @{user}'s profile... This may take a few seconds.")
    profile_url = f'https://www.tiktok.com/@{user}'
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {'tiktok': {'api_hostname': 'api-h2.tiktokv.com'}},
    }

    if HAS_IMPERSONATE:
        ydl_opts['impersonate'] = ImpersonateTarget('chrome')
    else:
        ydl_opts['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(profile_url, download=False)
            if 'entries' in info:
                return list(info['entries'])
            return []
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error accessing profile: {e}")
        if not error_msg:
            print("⚠️ The error message is empty. Printing full traceback:")
            traceback.print_exc()
        return None

def download_selected_videos(user, video_list, amount):
    """
    Downloads the top 'N' videos from the provided list in High Definition.
    """
    # Slice the list to match the user's requested amount
    videos_to_process = video_list[:amount]
    
    # Configuration for high-quality, watermark-free downloads
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': f'download/{user}/%(title).50s.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
        'sleep_interval': 3,
        'max_sleep_interval': 7,
        'extractor_args': {'tiktok': {'api_hostname': 'api-h2.tiktokv.com'}},
    }

    if HAS_IMPERSONATE:
        ydl_opts['impersonate'] = ImpersonateTarget('chrome')
    else:
        ydl_opts['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

    print(f"\n🚀 Starting download of {len(videos_to_process)} videos...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, video in enumerate(videos_to_process, 1):
            print(f"\n[Video {i}/{len(videos_to_process)}] Processing: {video.get('title', 'No Title')[:40]}...")
            try:
                ydl.download([video['url']])
            except Exception as e:
                print(f"⚠️ Could not download video {i}: {e}")

# --- MAIN EXECUTION FLOW ---
if __name__ == "__main__":
    # Step 1: User Input for the profile
    target_user = input("Enter TikTok username (without @): ").strip().lower()
    
    # Step 2: Fetch metadata and show total
    all_videos = get_profile_data(target_user)
    
    if all_videos is not None:
        total_found = len(all_videos)
        
        if total_found == 0:
            print("❌ No public videos found or the profile is private.")
            sys.exit()
            
        print(f"✅ Found {total_found} public videos in @{target_user}'s profile.")
        
        # Step 3: Ask for the specific amount to download
        try:
            requested = input(f"How many videos do you want to download? (1-{total_found}): ")
            requested_count = int(requested)
            
            if requested_count <= 0:
                print("Invalid number. Operation cancelled.")
            else:
                # Step 4: Run the actual download
                download_selected_videos(target_user, all_videos, requested_count)
                print(f"\n✨ All tasks completed. Files are in the '{target_user}' folder.")
                
        except ValueError:
            print("❌ Invalid input. Please enter a whole number.")