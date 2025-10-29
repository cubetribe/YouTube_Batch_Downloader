#!/usr/bin/env python3
"""
Einfacher YouTube Downloader
Verwendung: 
  python simple_downloader.py [URL]           # Video herunterladen
  python simple_downloader.py [URL] audio     # Nur Audio (MP3)
"""

import sys
import yt_dlp
import os

def download_video(url, output_dir=None):
    """Download a video from YouTube"""

    # Use Mac's default Downloads folder if no output_dir specified
    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    # Create downloads directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Configure yt-dlp options with modern YouTube workarounds
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bv*+ba/b',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'retries': 3,
        'fragment_retries': 3,
        'concurrent_fragment_downloads': 1,
        'http_headers': {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'),
            'Accept-Language': 'en-US,en;q=0.9',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video: {url}")
            ydl.download([url])
            print("Video download completed!")
            
    except Exception as e:
        print(f"Error downloading video: {e}")
        return False
    
    return True

def download_audio(url, output_dir=None):
    """Download only audio from YouTube as MP3"""

    # Use Mac's default Downloads folder if no output_dir specified
    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    # Create downloads directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Configure yt-dlp options for audio only with the same YouTube workarounds
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'retries': 3,
        'fragment_retries': 3,
        'concurrent_fragment_downloads': 1,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'http_headers': {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'),
            'Accept-Language': 'en-US,en;q=0.9',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio: {url}")
            ydl.download([url])
            print("Audio download completed!")
            
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return False
    
    return True

def batch_download(urls, mode="video", output_dir=None):
    """
    Download multiple videos/audios from a list of URLs

    Args:
        urls: List of YouTube URLs
        mode: "video" or "audio"
        output_dir: Output directory (default: ~/Downloads)

    Returns:
        dict: Statistics with successful and failed downloads
    """
    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    total = len(urls)
    successful = []
    failed = []

    print(f"\n{'='*60}")
    print(f"🚀 BATCH DOWNLOAD GESTARTET")
    print(f"{'='*60}")
    print(f"Modus: {'🎬 Video (MP4)' if mode == 'video' else '🎵 Audio (MP3)'}")
    print(f"Anzahl URLs: {total}")
    print(f"Zielordner: {output_dir}")
    print(f"{'='*60}\n")

    for i, url in enumerate(urls, 1):
        print(f"\n{'─'*60}")
        print(f"📥 Download {i}/{total}")
        print(f"URL: {url}")
        print(f"{'─'*60}")

        try:
            if mode == "audio":
                result = download_audio(url, output_dir)
            else:
                result = download_video(url, output_dir)

            if result:
                successful.append(url)
                print(f"✅ Erfolgreich ({i}/{total})")
            else:
                failed.append(url)
                print(f"❌ Fehlgeschlagen ({i}/{total})")

        except KeyboardInterrupt:
            print("\n\n⚠️  Batch-Download vom Benutzer abgebrochen!")
            print(f"Verarbeitet: {i-1}/{total}")
            break
        except Exception as e:
            failed.append(url)
            print(f"❌ Fehler: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 BATCH DOWNLOAD ABGESCHLOSSEN")
    print(f"{'='*60}")
    print(f"✅ Erfolgreich: {len(successful)}/{total}")
    print(f"❌ Fehlgeschlagen: {len(failed)}/{total}")

    if failed:
        print(f"\n⚠️  Fehlgeschlagene URLs:")
        for url in failed:
            print(f"   - {url}")

    print(f"{'='*60}\n")

    return {
        'total': total,
        'successful': len(successful),
        'failed': len(failed),
        'failed_urls': failed
    }

def main():
    """Main function"""

    # Check arguments
    if len(sys.argv) > 1:
        url = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else "video"
    else:
        url = input("YouTube URL eingeben: ")
        mode = input("Video oder Audio? (video/audio) [video]: ").lower() or "video"

    if not url.strip():
        print("Keine URL eingegeben!")
        return

    if "youtube.com" not in url and "youtu.be" not in url:
        print("Das ist keine YouTube URL!")
        return

    if mode == "audio":
        download_audio(url)
    else:
        download_video(url)

if __name__ == "__main__":
    main()
