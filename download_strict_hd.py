#!/usr/bin/env python3
"""
STRICT HD/4K Downloader
Downloads ONLY in Full HD (1080p) or better
DELETES anything below 1080p automatically
"""

import yt_dlp
import os
import subprocess
from pathlib import Path

class StrictHDDownloader:
    """Downloads ONLY HD content, deletes everything else"""

    def __init__(self):
        self.min_width = 1920   # Full HD width
        self.min_height = 1080  # Full HD height

    def get_video_resolution(self, filepath):
        """Get video resolution using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=s=x:p=0',
                filepath
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout:
                width, height = map(int, result.stdout.strip().split('x'))
                return width, height
        except:
            pass
        return 0, 0

    def download_strict_hd(self, url, output_dir=None):
        """Download with STRICT quality requirements"""

        if output_dir is None:
            output_dir = os.path.expanduser("~/Downloads")

        print("\n" + "="*70)
        print("🔒 STRICT HD/4K DOWNLOADER")
        print("="*70)
        print("⚠️  NUR 1080p oder höher wird akzeptiert!")
        print("⚠️  Niedrigere Qualität wird AUTOMATISCH GELÖSCHT!")
        print("="*70 + "\n")

        # Temporärer Dateiname für Download
        temp_filename = os.path.join(output_dir, "temp_download_%(id)s.%(ext)s")

        # yt-dlp Optionen für BESTE Qualität
        ydl_opts = {
            'outtmpl': temp_filename,

            # SEHR WICHTIG: Format-String für HD/4K
            # Versuche verschiedene Format-IDs direkt
            'format': (
                # 4K Formate
                '313+251/313+140/'  # 4K VP9 + Opus/AAC
                '401+251/401+140/'  # 4K AV1 + Opus/AAC
                '308+251/308+140/'  # 4K60 VP9 + Opus/AAC

                # 1440p Formate
                '271+251/271+140/'  # 1440p VP9 + Opus/AAC
                '400+251/400+140/'  # 1440p AV1 + Opus/AAC

                # 1080p Formate (Minimum)
                '137+140/'  # 1080p H264 + AAC
                '248+251/248+140/'  # 1080p VP9 + Opus/AAC
                '399+251/399+140/'  # 1080p60 AV1 + Opus/AAC
                '303+251/303+140/'  # 1080p60 VP9 + Opus/AAC

                # Fallback mit Höhen-Filter
                'bestvideo[height>=1080]+bestaudio/'
                'best[height>=1080]'
            ),

            'merge_output_format': 'mp4',
            'noplaylist': True,

            # WICHTIG: Browser Cookies nutzen
            'cookiesfrombrowser': ('chrome',),

            # Network settings
            'retries': 10,
            'fragment_retries': 10,
            'concurrent_fragment_downloads': 4,

            # Headers
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
            },

            # Verbose für Debugging
            'quiet': False,
            'verbose': True,
        }

        downloaded_file = None
        video_title = "Unknown"

        try:
            print("📥 Lade Video herunter...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Erst Info holen
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
                video_id = info.get('id', 'unknown')

                # Check verfügbare Formate
                formats = info.get('formats', [])
                hd_formats = [f for f in formats if f.get('height') and f.get('height') >= 1080]

                if not hd_formats:
                    print(f"\n❌ ABGELEHNT: Keine HD-Formate verfügbar!")
                    print(f"   Video: {video_title}")
                    print(f"   Beste Qualität: {max([f.get('height', 0) for f in formats if f.get('height')])}p")
                    return False

                # Download durchführen
                ydl.download([url])

                # Finde die heruntergeladene Datei
                temp_file = os.path.join(output_dir, f"temp_download_{video_id}.mp4")
                if os.path.exists(temp_file):
                    downloaded_file = temp_file

        except Exception as e:
            print(f"❌ Download-Fehler: {e}")
            return False

        # Qualitätsprüfung
        if downloaded_file and os.path.exists(downloaded_file):
            print("\n🔍 Prüfe Video-Qualität...")

            width, height = self.get_video_resolution(downloaded_file)
            print(f"   Auflösung: {width}x{height}")

            if height >= self.min_height:
                # Qualität OK - Umbenennen
                final_filename = os.path.join(output_dir, f"{video_title}.mp4")
                final_filename = final_filename.replace('/', '_').replace('\\', '_')

                os.rename(downloaded_file, final_filename)

                filesize = os.path.getsize(final_filename) / (1024*1024)

                print(f"\n✅ DOWNLOAD ERFOLGREICH!")
                print(f"   📹 Titel: {video_title}")
                print(f"   📺 Qualität: {width}x{height}")
                print(f"   💾 Größe: {filesize:.1f} MB")
                print(f"   📁 Datei: {final_filename}")

                return True
            else:
                # Qualität zu niedrig - LÖSCHEN!
                print(f"\n🗑️ QUALITÄT ZU NIEDRIG - LÖSCHE DATEI!")
                print(f"   ❌ {width}x{height} ist unter Minimum (1920x1080)")

                os.remove(downloaded_file)
                print(f"   ✅ Datei gelöscht: {downloaded_file}")

                return False

        print(f"\n❌ Download fehlgeschlagen - keine Datei gefunden")
        return False

    def batch_download_strict(self, urls, output_dir=None):
        """Batch download with strict quality control"""

        if output_dir is None:
            output_dir = os.path.expanduser("~/Downloads")

        total = len(urls)
        successful = []
        failed = []
        rejected = []

        print(f"\n{'='*70}")
        print(f"🔒 STRICT HD/4K BATCH DOWNLOAD")
        print(f"{'='*70}")
        print(f"⚠️  MINIMUM: 1920x1080 (Full HD)")
        print(f"⚠️  Videos unter 1080p werden GELÖSCHT!")
        print(f"Videos: {total}")
        print(f"{'='*70}\n")

        for i, url in enumerate(urls, 1):
            print(f"\n{'─'*70}")
            print(f"📥 Video {i}/{total}")
            print(f"URL: {url}")
            print(f"{'─'*70}")

            result = self.download_strict_hd(url, output_dir)

            if result:
                successful.append(url)
            else:
                rejected.append(url)

        # Summary
        print(f"\n{'='*70}")
        print(f"📊 ERGEBNIS")
        print(f"{'='*70}")
        print(f"✅ Erfolgreich (HD/4K): {len(successful)}/{total}")
        print(f"🗑️ Abgelehnt (<1080p): {len(rejected)}/{total}")

        if rejected:
            print(f"\n🗑️ Abgelehnte URLs (Qualität zu niedrig):")
            for url in rejected:
                print(f"   - {url}")

        print(f"{'='*70}\n")

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='STRICT HD/4K Downloader - NUR 1080p oder höher, Rest wird GELÖSCHT!'
    )

    parser.add_argument('url', nargs='?', help='YouTube URL')
    parser.add_argument('--batch', nargs='+', help='Mehrere URLs')
    parser.add_argument('--output', '-o', help='Output directory')

    args = parser.parse_args()

    downloader = StrictHDDownloader()

    if args.batch:
        downloader.batch_download_strict(args.batch, args.output)
    elif args.url:
        success = downloader.download_strict_hd(args.url, args.output)
        if not success:
            print("\n⚠️  Video wurde abgelehnt oder gelöscht!")
            exit(1)
    else:
        print("🔒 STRICT HD/4K DOWNLOADER")
        print("="*50)
        print("⚠️  NUR 1080p oder höher!")
        print("⚠️  Niedrigere Qualität wird GELÖSCHT!")
        print("="*50)

        url = input("\nYouTube URL: ").strip()
        if url:
            downloader.download_strict_hd(url)

if __name__ == "__main__":
    main()