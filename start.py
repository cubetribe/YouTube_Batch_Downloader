#!/usr/bin/env python3
"""
YouTube Downloader - Start Script
Einfaches Menü zum Auswählen von Video oder Audio Download
"""

import os
import re
from src.downloader_enhanced import EnhancedDownloader, batch_download

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """Display the main menu"""
    print("=" * 60)
    print("🎬 YOUTUBE HD/4K DOWNLOADER 🎵")
    print("=" * 60)
    print("Alle Video-Downloads folgen der Regel: 4K > 1080p > Abbruch")
    print("Ein Protokoll wird in 'src/download_log.txt' geführt.")
    print("-" * 60)
    print()
    print("📹 EINZELNE DOWNLOADS:")
    print("  1️⃣  Video herunterladen (4K/1080p)")
    print("  2️⃣  Audio herunterladen (MP3 320kbps)")
    print()
    print("📦 BATCH DOWNLOADS:")
    print("  3️⃣  Batch Download - Videos (4K/1080p)")
    print("  4️⃣  Batch Download - Audios (MP3)")
    print()
    print("  5️⃣  Beenden")
    print()
    print("=" * 60)

def get_youtube_url():
    """Get YouTube URL from user"""
    while True:
        url = input("\nYouTube URL eingeben: ").strip()

        if not url:
            print("❌ Keine URL eingegeben!")
            continue

        if "youtube.com" not in url and "youtu.be" not in url:
            print("❌ Das ist keine YouTube URL!")
            continue

        return url

def extract_youtube_urls(text):
    """Extract all YouTube URLs from text using regex"""
    patterns = [
        r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+(?:&[\w=&-]*)?',
        r'https?://youtu\.be/[\w-]+(?:\?[\w=&-]*)?',
        r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
        r'https?://(?:www\.)?youtube\.com/v/[\w-]+'
    ]

    urls = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        urls.extend(found)

    seen = set()
    unique_urls = []
    for url in urls:
        if 'youtube.com/watch?v=' in url:
            video_id_match = re.search(r'v=([\w-]+)', url)
            if video_id_match:
                clean_url = f"https://www.youtube.com/watch?v={video_id_match.group(1)}"
                if clean_url not in seen:
                    seen.add(clean_url)
                    unique_urls.append(clean_url)
        elif url not in seen:
            seen.add(url)
            unique_urls.append(url)

    return unique_urls

def get_batch_urls():
    """Get multiple YouTube URLs from user"""
    print("\n" + "=" * 70)
    print("📋 BATCH DOWNLOAD - URLs eingeben")
    print("=" * 70)
    print("Füge eine oder mehrere YouTube URLs ein und drücke Enter.")
    print("Gib 'start' oder 'fertig' ein, wenn du alle URLs eingefügt hast.")
    print("=" * 70 + "\n")

    all_collected_text = []
    while True:
        user_input = input(">>> ").strip()
        if user_input.lower() in ['start', 'fertig', 'done']:
            break
        if user_input:
            all_collected_text.append(user_input)

    full_text = '\n'.join(all_collected_text)
    all_urls = extract_youtube_urls(full_text)

    if not all_urls:
        print("❌ Keine gültigen YouTube URLs gefunden!")
        return []

    print(f"\n✅ {len(all_urls)} URL(s) gefunden. Download wird vorbereitet...")
    return all_urls

def main():
    """Main function"""
    downloader = EnhancedDownloader()

    while True:
        clear_screen()
        show_menu()

        choice = input("Auswahl (1-5): ").strip()

        if choice == "1":
            url = get_youtube_url()
            downloader.download_video(url)
            input("\nEnter drücken zum Fortfahren...")

        elif choice == "2":
            url = get_youtube_url()
            downloader.download_audio(url)
            input("\nEnter drücken zum Fortfahren...")

        elif choice == "3":
            urls = get_batch_urls()
            if urls:
                batch_download(urls, mode='video')
            input("\nBatch-Download abgeschlossen. Enter drücken zum Fortfahren...")

        elif choice == "4":
            urls = get_batch_urls()
            if urls:
                batch_download(urls, mode='audio')
            input("\nBatch-Download abgeschlossen. Enter drücken zum Fortfahren...")

        elif choice == "5":
            print("\n👋 Auf Wiedersehen!")
            break

        else:
            print("❌ Ungültige Auswahl!")
            input("Enter drücken zum Fortfahren...")

if __name__ == "__main__":
    main()