import yt_dlp

class MyLogger:
    """
    Custom logger class to handle yt_dlp internal messages.
    """
    def debug(self, msg):
        # Filter out purely technical debug messages to keep the console clean
        if not msg.startswith('[debug] '):
            print(f"[INFO] {msg}")

    def warning(self, msg):
        print(f"[WARNING] {msg}")

    def error(self, msg):
        print(f"[ERROR] {msg}")

def progress_hook(d):
    """
    Function to track and display the progress of each individual video.
    """
    if d['status'] == 'downloading':
        # Extracts filename and percentage string
        filename = d.get('filename', 'video')
        percent = d.get('_percent_str', '0%')
        print(f"📥 Downloading: {filename} | Progress: {percent}", end='\r')
    
    if d['status'] == 'finished':
        print(f"\n✅ Finished: {d['filename']}")

def download_from_tiktok_user(user, total_videos=10):
    """
    Main function to download a specific number of videos from a TikTok profile.
    """
    profile_url = f'https://www.tiktok.com/@{user}'
    
    # Configuration options for yt-dlp
    ydl_opts = {
        'format': 'best',
        # 'playlist_items' defines the range of videos to fetch (e.g., '1-10')
        'playlist_items': f'1-{total_videos}',
        # Saves files in a folder named after the uploader
        'outtmpl': f'%(uploader)s/%(title).50s.%(ext)s', 
        'noplaylist': False,
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
    }

    try:
        print(f"--- Starting process for user: @{user} ---")
        print(f"--- Target: Latest {total_videos} videos ---\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([profile_url])
            
        print(f"\n--- Task Completed. Check the '{user}' folder ---")
    except Exception as e:
        print(f"\n❌ A critical error occurred: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    target_user = input("Enter TikTok username (without @): ")
    video_count = input("Enter number of videos to download (e.g., 5): ")
    
    download_from_tiktok_user(target_user, total_videos=video_count)