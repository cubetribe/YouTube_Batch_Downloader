#!/usr/bin/env python3
"""
Enhanced YouTube Downloader mit PO Token Support
Verwendet moderne Fallback-Strategien für YouTube Downloads
"""

import sys
import yt_dlp
import os
import json
from typing import Optional, Dict, List

def load_config():
    """Load configuration including PO Token if available"""
    config_path = os.path.expanduser("~/.yt_downloader_config.json")

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            pass

    return {}

def save_po_token(token: str):
    """Save PO Token to configuration file"""
    config_path = os.path.expanduser("~/.yt_downloader_config.json")

    config = load_config()
    config['po_token'] = token

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✅ PO Token gespeichert in: {config_path}")

def get_enhanced_ydl_opts(mode: str = "video", output_dir: str = None, po_token: str = None) -> Dict:
    """
    Get enhanced yt-dlp options with multiple fallback strategies

    Args:
        mode: "video" or "audio"
        output_dir: Output directory
        po_token: Optional PO Token for authentication
    """

    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    # Base configuration
    base_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'retries': 5,
        'fragment_retries': 5,
        'concurrent_fragment_downloads': 1,
        'ignoreerrors': False,  # Stop on errors to try alternative methods
        'no_warnings': False,
        'quiet': False,
        'verbose': True,  # Enable verbose output for debugging

        # Enhanced HTTP headers to appear more like a real browser
        'http_headers': {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,de;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
        },

        # Rate limiting to avoid detection
        'sleep_interval': 2,
        'max_sleep_interval': 5,
        'sleep_interval_requests': 1,
    }

    # Enhanced extractor arguments with multiple client strategies
    extractor_args = {
        'youtube': {
            'player_client': ['web', 'android', 'ios'],  # Try multiple clients
            'player_skip': ['configs'],
        }
    }

    # Add PO Token if available
    if po_token:
        extractor_args['youtube']['po_token'] = f'android.gvs+{po_token}'
        print(f"🔑 Using PO Token for authentication")

    base_opts['extractor_args'] = extractor_args

    # Mode-specific options
    if mode == "audio":
        base_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Video mode with fallback formats
        base_opts.update({
            'format': 'bv*+ba/b/best',  # More fallback options
            'merge_output_format': 'mp4',
        })

    return base_opts

def download_with_fallback(url: str, mode: str = "video", output_dir: str = None) -> bool:
    """
    Download with multiple fallback strategies

    Strategies:
    1. Try with PO Token if available
    2. Try with android client
    3. Try with web client
    4. Try with ios client
    5. Try with cookies from browser
    """

    config = load_config()
    po_token = config.get('po_token')

    # Strategy 1: Try with PO Token if available
    if po_token:
        print("🔧 Strategie 1: Mit PO Token...")
        opts = get_enhanced_ydl_opts(mode, output_dir, po_token)
        if try_download(url, opts, f"Downloading {mode} (with PO Token)"):
            return True

    # Strategy 2: Android client without PO Token
    print("🔧 Strategie 2: Android Client...")
    opts = get_enhanced_ydl_opts(mode, output_dir)
    opts['extractor_args']['youtube']['player_client'] = ['android']
    if try_download(url, opts, f"Downloading {mode} (Android client)"):
        return True

    # Strategy 3: Web client
    print("🔧 Strategie 3: Web Client...")
    opts = get_enhanced_ydl_opts(mode, output_dir)
    opts['extractor_args']['youtube']['player_client'] = ['web']
    if try_download(url, opts, f"Downloading {mode} (Web client)"):
        return True

    # Strategy 4: iOS client
    print("🔧 Strategie 4: iOS Client...")
    opts = get_enhanced_ydl_opts(mode, output_dir)
    opts['extractor_args']['youtube']['player_client'] = ['ios']
    if try_download(url, opts, f"Downloading {mode} (iOS client)"):
        return True

    # Strategy 5: Try with browser cookies
    print("🔧 Strategie 5: Mit Browser Cookies...")
    opts = get_enhanced_ydl_opts(mode, output_dir)
    opts['cookiesfrombrowser'] = ('chrome',)  # Try Chrome cookies
    if try_download(url, opts, f"Downloading {mode} (with cookies)"):
        return True

    # Strategy 6: Minimal format (360p or lower)
    print("🔧 Strategie 6: Niedrige Qualität (360p)...")
    opts = get_enhanced_ydl_opts(mode, output_dir)
    if mode == "video":
        opts['format'] = 'best[height<=360]/worst'
    if try_download(url, opts, f"Downloading {mode} (low quality)"):
        return True

    print("❌ Alle Download-Strategien fehlgeschlagen")
    return False

def try_download(url: str, opts: Dict, description: str) -> bool:
    """Try to download with given options"""
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            print(f"📥 {description}: {url}")
            info = ydl.extract_info(url, download=True)
            if info:
                print(f"✅ Download erfolgreich!")
                return True
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "403" in error_msg or "PO Token" in error_msg:
            print(f"⚠️  HTTP 403 Error - PO Token benötigt")
        elif "Video unavailable" in error_msg:
            print(f"⚠️  Video nicht verfügbar")
        elif "Private video" in error_msg:
            print(f"⚠️  Privates Video")
        else:
            print(f"⚠️  Download-Fehler: {error_msg[:100]}...")
    except Exception as e:
        print(f"⚠️  Fehler: {str(e)[:100]}...")

    return False

def batch_download_enhanced(urls: List[str], mode: str = "video", output_dir: str = None) -> Dict:
    """
    Enhanced batch download with fallback strategies
    """
    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    total = len(urls)
    successful = []
    failed = []
    failed_details = {}

    print(f"\n{'='*60}")
    print(f"🚀 ENHANCED BATCH DOWNLOAD")
    print(f"{'='*60}")
    print(f"Modus: {'🎬 Video (MP4)' if mode == 'video' else '🎵 Audio (MP3)'}")
    print(f"Anzahl URLs: {total}")
    print(f"Zielordner: {output_dir}")

    config = load_config()
    if config.get('po_token'):
        print(f"🔑 PO Token verfügbar")
    else:
        print(f"⚠️  Kein PO Token konfiguriert")

    print(f"{'='*60}\n")

    for i, url in enumerate(urls, 1):
        print(f"\n{'─'*60}")
        print(f"📥 Download {i}/{total}")
        print(f"URL: {url}")
        print(f"{'─'*60}")

        try:
            result = download_with_fallback(url, mode, output_dir)

            if result:
                successful.append(url)
                print(f"✅ Erfolgreich ({i}/{total})")
            else:
                failed.append(url)
                failed_details[url] = "Alle Strategien fehlgeschlagen"
                print(f"❌ Fehlgeschlagen ({i}/{total})")

        except KeyboardInterrupt:
            print("\n\n⚠️  Batch-Download vom Benutzer abgebrochen!")
            print(f"Verarbeitet: {i-1}/{total}")
            break
        except Exception as e:
            failed.append(url)
            failed_details[url] = str(e)
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
            detail = failed_details.get(url, "Unbekannter Fehler")
            print(f"   - {url}")
            print(f"     Grund: {detail}")

    print(f"{'='*60}\n")

    return {
        'total': total,
        'successful': len(successful),
        'failed': len(failed),
        'failed_urls': failed,
        'failed_details': failed_details
    }

def setup_po_token():
    """Interactive setup for PO Token"""
    print("\n" + "="*70)
    print("🔑 PO TOKEN SETUP")
    print("="*70)
    print("\nEin PO Token hilft, YouTube's Sicherheitsbeschränkungen zu umgehen.")
    print("\nAnleitung zum Erhalten eines PO Tokens:")
    print("1. Öffne YouTube im Browser und melde dich an")
    print("2. Öffne die Entwicklertools (F12)")
    print("3. Gehe zum 'Network' Tab")
    print("4. Lade eine YouTube-Seite neu")
    print("5. Suche nach Requests zu 'player' oder 'watch'")
    print("6. Finde den 'po_token' Parameter in den Headers oder Response")
    print("\nAlternativ: https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide")
    print("="*70)

    token = input("\nPO Token eingeben (oder Enter für Abbruch): ").strip()

    if token:
        # Remove common prefixes if user included them
        if token.startswith('android.gvs+'):
            token = token[12:]
        elif token.startswith('gvs+'):
            token = token[4:]

        save_po_token(token)
        print("✅ Token gespeichert! Wird bei zukünftigen Downloads verwendet.")
    else:
        print("❌ Kein Token eingegeben. Setup abgebrochen.")

def main():
    """Main function for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='Enhanced YouTube Downloader')
    parser.add_argument('url', nargs='?', help='YouTube URL')
    parser.add_argument('--mode', choices=['video', 'audio'], default='video', help='Download mode')
    parser.add_argument('--setup-token', action='store_true', help='Setup PO Token')
    parser.add_argument('--batch', nargs='+', help='Batch download URLs')

    args = parser.parse_args()

    if args.setup_token:
        setup_po_token()
        return

    if args.batch:
        batch_download_enhanced(args.batch, args.mode)
    elif args.url:
        download_with_fallback(args.url, args.mode)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()