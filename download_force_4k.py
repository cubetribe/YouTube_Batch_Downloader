#!/usr/bin/env python3
"""
FORCE 4K/HD Downloader
Forces download of HD/4K content ONLY
Uses specific format IDs for guaranteed quality
"""

import yt_dlp
import os
import subprocess
import sys
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return True
    except:
        print("❌ ffmpeg nicht gefunden! Installiere mit: brew install ffmpeg")
        return False

def get_4k_format_string():
    """Return format string for 4K/HD content"""
    return (
        # 4K VP9 + best audio
        '313+bestaudio/'
        '308+bestaudio/'

        # 4K H264 (wenn verfügbar)
        '266+bestaudio/'

        # 1440p als Fallback
        '271+bestaudio/'
        '264+bestaudio/'

        # 1080p60 als Minimum
        '299+bestaudio/'
        '303+bestaudio/'

        # 1080p als absolutes Minimum
        '137+bestaudio/'
        '248+bestaudio/'

        # NICHTS darunter!
    ).rstrip('/')

def download_force_4k(url, output_dir=None):
    """Force download in 4K/HD quality"""

    if not check_ffmpeg():
        return False

    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    print("\n" + "="*70)
    print("⚡ FORCE 4K/HD DOWNLOADER")
    print("="*70)
    print("📺 Akzeptiert NUR: 4K, 1440p, 1080p")
    print("🔒 Verwendet spezifische Format-IDs")
    print("="*70 + "\n")

    # Optionen für 4K Download
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s [%(height)sp].%(ext)s'),

        # Verwende spezifische Format-IDs
        'format': get_4k_format_string(),

        # Merge zu MP4
        'merge_output_format': 'mp4',

        # Keine Playlists
        'noplaylist': True,

        # ffmpeg für merge
        'prefer_ffmpeg': True,

        # Browser Cookies
        'cookiesfrombrowser': ('chrome',),

        # Network
        'retries': 15,
        'fragment_retries': 15,
        'concurrent_fragment_downloads': 5,

        # Headers
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': '*/*',
        },

        # Verbose
        'verbose': False,
        'quiet': False,

        # Postprocessors
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        print("📋 Prüfe verfügbare Formate...")

        # Erst Formate checken
        with yt_dlp.YoutubeDL({'quiet': True, 'cookiesfrombrowser': ('chrome',)}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            formats = info.get('formats', [])

            # Finde HD Formate
            hd_formats = []
            for f in formats:
                if f.get('format_id') in ['313', '308', '271', '264', '299', '303', '137', '248', '266']:
                    height = f.get('height', 0)
                    format_id = f.get('format_id')
                    vcodec = f.get('vcodec', 'unknown')
                    hd_formats.append((format_id, height, vcodec))

            if not hd_formats:
                print(f"\n❌ KEINE HD FORMATE VERFÜGBAR!")
                print(f"   Video: {title}")
                print(f"   Verfügbare Format IDs: {[f.get('format_id') for f in formats[:10]]}")

                # Zeige beste verfügbare Qualität
                video_formats = [f for f in formats if f.get('height')]
                if video_formats:
                    best = max(video_formats, key=lambda x: x.get('height', 0))
                    print(f"   Beste Qualität: {best.get('height')}p (Format {best.get('format_id')})")

                return False

            # Zeige gefundene HD Formate
            print(f"\n✅ HD Formate gefunden:")
            for fmt_id, height, codec in sorted(hd_formats, key=lambda x: x[1], reverse=True):
                quality = "4K" if height >= 2160 else "1440p" if height >= 1440 else "1080p"
                print(f"   Format {fmt_id}: {quality} ({height}p) - {codec}")

            best_format = max(hd_formats, key=lambda x: x[1])
            print(f"\n🎯 Verwende Format {best_format[0]}: {best_format[1]}p")

        # Jetzt downloaden
        print(f"\n⬇️ Starte Download...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

            print(f"\n✅ DOWNLOAD ERFOLGREICH!")
            print(f"   📹 Titel: {title}")
            print(f"   📁 Speicherort: {output_dir}")

            return True

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)

        if "not available" in error_msg.lower():
            print(f"\n❌ Format nicht verfügbar!")
            print("Mögliche Lösungen:")
            print("1. Stelle sicher dass du in Chrome bei YouTube angemeldet bist")
            print("2. Versuche es mit --use-cookies")
            print("3. Das Video hat möglicherweise kein HD")
        else:
            print(f"\n❌ Download-Fehler: {error_msg}")

        return False

    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        return False

def use_cookies_download(url, output_dir=None):
    """Alternative: Download mit exportierten Cookies"""

    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    print("\n🍪 Versuche mit Cookies-Datei...")
    print("Exportiere Cookies aus Chrome mit einer Extension wie 'Get cookies.txt'")

    cookie_file = Path.home() / "Downloads" / "youtube.com_cookies.txt"

    if not cookie_file.exists():
        print(f"❌ Cookies-Datei nicht gefunden: {cookie_file}")
        print("\nAnleitung:")
        print("1. Installiere 'Get cookies.txt' Extension in Chrome")
        print("2. Gehe zu YouTube und melde dich an")
        print("3. Klicke auf die Extension und exportiere Cookies")
        print("4. Speichere als 'youtube.com_cookies.txt' in Downloads")
        return False

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s [%(height)sp].%(ext)s'),
        'format': get_4k_format_string(),
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'cookiefile': str(cookie_file),  # Verwende Cookie-Datei
        'verbose': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"❌ Fehler mit Cookies: {e}")
        return False

def main():
    """Main function"""

    if len(sys.argv) < 2:
        print("⚡ FORCE 4K/HD DOWNLOADER")
        print("="*50)
        print("\nVerwendung:")
        print("  python download_force_4k.py <URL>")
        print("  python download_force_4k.py --cookies <URL>")
        print("\nBeispiel:")
        print("  python download_force_4k.py https://youtube.com/watch?v=xxx")
        sys.exit(1)

    use_cookies = "--cookies" in sys.argv
    url = sys.argv[-1]

    if not url.startswith("http"):
        print("❌ Keine gültige URL!")
        sys.exit(1)

    if use_cookies:
        success = use_cookies_download(url)
    else:
        success = download_force_4k(url)

    if not success:
        print("\n⚠️  Download fehlgeschlagen oder abgelehnt!")

        print("\n💡 Alternativen:")
        print("1. Verwende yt-dlp direkt mit:")
        print(f"   yt-dlp -f '313+bestaudio' '{url}'")
        print("2. Exportiere Cookies und verwende:")
        print(f"   python download_force_4k.py --cookies '{url}'")

        sys.exit(1)

if __name__ == "__main__":
    main()