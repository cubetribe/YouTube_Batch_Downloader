#!/usr/bin/env python3
"""
YouTube Best Quality Downloader
Downloads videos in the best available quality
"""

import sys
import yt_dlp
import os

def download_best_quality(url, output_dir=None):
    """Download video in best available quality"""

    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\n🎬 Downloading in BEST available quality...")
    print(f"📁 Output folder: {output_dir}")

    # Options for best quality
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),

        # Simple format string for best quality
        'format': 'best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',

        'merge_output_format': 'mp4',
        'noplaylist': True,

        # Use browser cookies for authentication
        'cookiesfrombrowser': ('chrome',),

        # Network settings
        'retries': 10,
        'fragment_retries': 10,
        'concurrent_fragment_downloads': 4,

        # User agent
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },

        # Progress output
        'quiet': False,
        'no_warnings': False,
        'progress': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First, get video info
            print("📊 Getting video info...")
            info = ydl.extract_info(url, download=False)

            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown')

            # Check available formats
            formats = info.get('formats', [])
            heights = sorted(set(f.get('height') for f in formats if f.get('height')), reverse=True)

            print(f"\n📹 Video: {title}")
            print(f"👤 Uploader: {uploader}")
            print(f"⏱️ Duration: {duration // 60}:{duration % 60:02d}")

            if heights:
                best_height = heights[0]
                quality_label = "8K" if best_height >= 4320 else \
                               "4K" if best_height >= 2160 else \
                               "1440p" if best_height >= 1440 else \
                               "1080p" if best_height >= 1080 else \
                               "720p" if best_height >= 720 else \
                               f"{best_height}p"
                print(f"🎯 Best available quality: {quality_label} ({best_height}p)")
                print(f"📊 All available qualities: {', '.join(f'{h}p' for h in heights[:5])}")

            # Now download
            print(f"\n⬇️ Starting download...")
            ydl.download([url])

            print(f"\n✅ Download completed successfully!")
            print(f"📁 Saved to: {output_dir}")
            return True

    except Exception as e:
        print(f"\n❌ Error: {e}")

        # Try fallback with simpler options
        print("\n🔄 Trying fallback method...")

        fallback_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'best',
            'cookiesfrombrowser': ('chrome',),
        }

        try:
            with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                ydl.download([url])
                print(f"\n✅ Download completed with fallback method!")
                return True
        except Exception as e2:
            print(f"\n❌ Fallback also failed: {e2}")
            return False

def main():
    """Main function"""
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        print("🎬 YouTube Best Quality Downloader")
        print("=" * 40)
        url = input("YouTube URL: ").strip()
        output = None

    if url:
        download_best_quality(url, output)
    else:
        print("❌ No URL provided!")

if __name__ == "__main__":
    main()