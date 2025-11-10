#!/usr/bin/env python3
"""
YouTube 4K Downloader - Maximum Quality Edition
Downloads videos in highest available quality (up to 4K/8K)
"""

import sys
import yt_dlp
import os
import json

def get_video_info(url):
    """Get video information to check available qualities"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'cookiesfrombrowser': ('chrome',),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            # Get available video qualities
            qualities = set()
            for f in formats:
                if f.get('height'):
                    qualities.add(f['height'])

            return info['title'], sorted(qualities, reverse=True)
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None, []

def download_highest_quality(url, output_dir=None):
    """Download video in the highest available quality"""

    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    # Get video info first
    title, available_qualities = get_video_info(url)

    if title:
        print(f"\n📹 Video: {title}")
        if available_qualities:
            print(f"📊 Verfügbare Qualitäten: {', '.join([f'{q}p' for q in available_qualities])}")
            max_quality = available_qualities[0]

            quality_label = "8K" if max_quality > 4320 else \
                           "4K" if max_quality >= 2160 else \
                           "1440p" if max_quality >= 1440 else \
                           "1080p" if max_quality >= 1080 else \
                           "720p" if max_quality >= 720 else \
                           f"{max_quality}p"

            print(f"🎯 Lade in höchster Qualität: {quality_label} ({max_quality}p)")

    # Configure for maximum quality download
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s [%(height)sp].%(ext)s'),

        # Format selection für höchste Qualität
        # Priorität: 8K > 4K > 1440p > 1080p > 720p > beste verfügbar
        'format': (
            # Versuche zuerst 8K
            'bestvideo[height>=4320][ext=webm]+bestaudio[ext=webm]/'
            'bestvideo[height>=4320][ext=mp4]+bestaudio[ext=m4a]/'
            'bestvideo[height>=4320]+bestaudio/'
            # Dann 4K
            'bestvideo[height>=2160][ext=webm]+bestaudio[ext=webm]/'
            'bestvideo[height>=2160][ext=mp4]+bestaudio[ext=m4a]/'
            'bestvideo[height>=2160]+bestaudio/'
            # Dann 1440p
            'bestvideo[height>=1440][ext=webm]+bestaudio[ext=webm]/'
            'bestvideo[height>=1440][ext=mp4]+bestaudio[ext=m4a]/'
            'bestvideo[height>=1440]+bestaudio/'
            # Dann 1080p
            'bestvideo[height>=1080][ext=webm]+bestaudio[ext=webm]/'
            'bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]/'
            'bestvideo[height>=1080]+bestaudio/'
            # Fallback auf beste verfügbare Qualität
            'bestvideo[ext=webm]+bestaudio[ext=webm]/'
            'bestvideo[ext=mp4]+bestaudio[ext=m4a]/'
            'bestvideo+bestaudio/'
            'best'
        ),

        'merge_output_format': 'mp4',  # Finale Datei als MP4
        'noplaylist': True,

        # Wichtig: Browser Cookies für volle Qualität
        'cookiesfrombrowser': ('chrome',),  # oder 'firefox', 'safari', 'edge'

        # Erweiterte Optionen für bessere Downloads
        'retries': 10,
        'fragment_retries': 10,
        'concurrent_fragment_downloads': 4,  # Mehr parallele Downloads für große Dateien
        'buffersize': 1024 * 1024,  # 1MB buffer

        # User-Agent und Headers
        'http_headers': {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/131.0.0.0 Safari/537.36'),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        },

        # YouTube-spezifische Einstellungen
        'extractor_args': {
            'youtube': {
                # Versuche verschiedene Player-Clients für beste Qualität
                'player_client': ['web_creator', 'tv_embedded', 'web', 'ios', 'android'],
                'player_skip': ['configs', 'webpage'],
            }
        },

        # Rate limiting (wichtig für große Downloads)
        'sleep_interval': 3,
        'max_sleep_interval': 8,
        'sleep_interval_requests': 1,

        # Fortschrittsanzeige
        'progress_hooks': [progress_hook],
        'quiet': False,
        'no_warnings': False,
    }

    try:
        print("\n⏬ Download startet...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Zeige finale Qualität
            if info:
                actual_height = info.get('height', 0)
                actual_format = info.get('format_note', 'unbekannt')
                filesize = info.get('filesize', 0) or info.get('filesize_approx', 0)

                print(f"\n✅ Download abgeschlossen!")
                print(f"📺 Finale Qualität: {actual_height}p ({actual_format})")
                if filesize:
                    print(f"💾 Dateigröße: {filesize / (1024*1024):.1f} MB")
                print(f"📁 Gespeichert in: {output_dir}")
                return True

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        print(f"\n❌ Download-Fehler: {error_msg}")

        # Spezifische Fehlerbehandlung
        if "Sign in to confirm" in error_msg:
            print("\n⚠️  YouTube erfordert Anmeldung für dieses Video.")
            print("Lösung: Stelle sicher, dass du in Chrome bei YouTube angemeldet bist.")
        elif "Private video" in error_msg:
            print("\n⚠️  Dies ist ein privates Video.")
        elif "403" in error_msg or "Forbidden" in error_msg:
            print("\n⚠️  Zugriff verweigert. Mögliche Lösungen:")
            print("1. Stelle sicher, dass du in Chrome bei YouTube angemeldet bist")
            print("2. Verwende einen PO Token (siehe PO_TOKEN_ANLEITUNG.md)")
            print("3. Versuche es mit einem VPN")

        return False

    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        return False

def progress_hook(d):
    """Show download progress"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')

        # Clear line and show progress
        print(f"\r⏬ Progress: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\n✨ Download fertig, verarbeite...")

def batch_download_4k(urls, output_dir=None):
    """Download multiple videos in highest quality"""
    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    total = len(urls)
    successful = []
    failed = []

    print(f"\n{'='*60}")
    print(f"🎬 4K BATCH DOWNLOAD")
    print(f"{'='*60}")
    print(f"Videos: {total}")
    print(f"Zielordner: {output_dir}")
    print(f"{'='*60}")

    for i, url in enumerate(urls, 1):
        print(f"\n{'─'*60}")
        print(f"📥 Video {i}/{total}")
        print(f"URL: {url}")
        print(f"{'─'*60}")

        if download_highest_quality(url, output_dir):
            successful.append(url)
        else:
            failed.append(url)

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 ZUSAMMENFASSUNG")
    print(f"{'='*60}")
    print(f"✅ Erfolgreich: {len(successful)}/{total}")
    print(f"❌ Fehlgeschlagen: {len(failed)}/{total}")

    if failed:
        print(f"\n⚠️  Fehlgeschlagene URLs:")
        for url in failed:
            print(f"   - {url}")

    print(f"{'='*60}\n")

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='YouTube 4K Downloader - Lädt Videos in höchster Qualität',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s https://youtube.com/watch?v=xxx
  %(prog)s --batch url1 url2 url3
  %(prog)s --output ~/Desktop https://youtube.com/watch?v=xxx
        """
    )

    parser.add_argument('url', nargs='?', help='YouTube URL zum Download')
    parser.add_argument('--batch', nargs='+', help='Mehrere URLs auf einmal')
    parser.add_argument('--output', '-o', help='Output-Verzeichnis (Standard: ~/Downloads)')

    args = parser.parse_args()

    output_dir = args.output if args.output else None

    if args.batch:
        batch_download_4k(args.batch, output_dir)
    elif args.url:
        download_highest_quality(args.url, output_dir)
    else:
        # Interaktiver Modus
        print("🎬 YouTube 4K Downloader")
        print("=" * 40)
        url = input("YouTube URL eingeben: ").strip()
        if url:
            download_highest_quality(url)
        else:
            print("❌ Keine URL eingegeben!")

if __name__ == "__main__":
    main()