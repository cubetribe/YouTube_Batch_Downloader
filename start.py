#!/usr/bin/env python3
"""
YouTube Downloader - Start Script
Einfaches Menü zum Auswählen von Video oder Audio Download
"""

import subprocess
import sys
import os
import re
from src.downloader import batch_download

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """Display the main menu"""
    print("=" * 50)
    print("🎬 YOUTUBE DOWNLOADER 🎵")
    print("=" * 50)
    print()
    print("1️⃣  Video herunterladen (MP4)")
    print("2️⃣  Audio herunterladen (MP3)")
    print("3️⃣  Batch Download - Videos (MP4)")
    print("4️⃣  Batch Download - Audios (MP3)")
    print("5️⃣  Beenden")
    print()
    print("=" * 50)

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
    # Regex patterns for YouTube URLs
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

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        # Clean URL (remove extra parameters but keep video ID)
        if 'youtube.com/watch?v=' in url:
            # Extract video ID and rebuild clean URL
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
    """Get multiple YouTube URLs from user - supports multi-line paste and multiple inputs"""
    print("\n" + "=" * 70)
    print("📋 BATCH DOWNLOAD - URLs eingeben")
    print("=" * 70)
    print("Du kannst:")
    print("  • URLs einzeln oder mehrere auf einmal einfügen (Cmd+V)")
    print("  • Mehrfach einfügen (URLs werden gesammelt)")
    print("  • 'file' eingeben um URLs aus einer Datei zu laden")
    print()
    print("Befehle:")
    print("  • Tippe 'start' oder 'fertig' wenn du alle URLs eingefügt hast")
    print("  • Tippe 'clear' um alle bisher eingegebenen URLs zu löschen")
    print("  • Tippe 'show' um bisher gefundene URLs anzuzeigen")
    print("=" * 70 + "\n")

    all_collected_text = []
    all_urls = []

    while True:
        user_input = input(">>> ").strip()

        # Check for commands
        if user_input.lower() in ['start', 'fertig', 'done']:
            break

        if user_input.lower() == 'clear':
            all_collected_text = []
            all_urls = []
            print("✅ Alle URLs gelöscht.\n")
            continue

        if user_input.lower() == 'show':
            current_urls = extract_youtube_urls('\n'.join(all_collected_text))
            if current_urls:
                print(f"\n📋 Bisher {len(current_urls)} URLs gefunden:")
                for i, url in enumerate(current_urls, 1):
                    print(f"  {i}. {url}")
                print()
            else:
                print("⚠️  Noch keine URLs gefunden.\n")
            continue

        if user_input.lower() == 'file':
            file_path = input("Pfad zur Textdatei mit URLs: ").strip()
            try:
                with open(file_path, 'r') as f:
                    file_content = f.read()
                    all_collected_text.append(file_content)
                    file_urls = extract_youtube_urls(file_content)
                    print(f"✅ {len(file_urls)} URLs aus Datei geladen\n")
            except FileNotFoundError:
                print(f"❌ Datei nicht gefunden: {file_path}\n")
            except Exception as e:
                print(f"❌ Fehler beim Laden der Datei: {e}\n")
            continue

        # Regular input - collect it
        if user_input:
            all_collected_text.append(user_input)
            # Extract URLs from current input and show count
            current_batch = extract_youtube_urls(user_input)
            if current_batch:
                print(f"✅ {len(current_batch)} URL(s) erkannt")
            else:
                print("⚠️  Keine YouTube URLs in dieser Eingabe gefunden")

    # Final extraction of all URLs
    full_text = '\n'.join(all_collected_text)
    all_urls = extract_youtube_urls(full_text)

    # Show summary and ask for confirmation
    print("\n" + "=" * 70)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 70)

    if not all_urls:
        print("❌ Keine YouTube URLs gefunden!")
        print("=" * 70 + "\n")
        return []

    print(f"✅ Insgesamt {len(all_urls)} YouTube URL(s) gefunden:\n")
    for i, url in enumerate(all_urls, 1):
        print(f"  {i}. {url}")

    print("\n" + "=" * 70)

    # Ask for confirmation
    confirm = input("\n🚀 Mit diesen URLs fortfahren? (ja/j für Start, alles andere bricht ab): ").strip().lower()

    if confirm in ['ja', 'j', 'yes', 'y']:
        print("✅ Download wird gestartet...\n")
        return all_urls
    else:
        print("❌ Abgebrochen. Keine Downloads gestartet.\n")
        return []

def run_downloader(url, mode):
    """Run the downloader script"""
    try:
        if mode == "video":
            print(f"\n🎬 Starte Video Download...")
        else:
            print(f"\n🎵 Starte Audio Download...")

        subprocess.run([sys.executable, "src/downloader.py", url, mode])

        print("\n✅ Download abgeschlossen!")
        input("Enter drücken zum Fortfahren...")

    except Exception as e:
        print(f"❌ Fehler: {e}")
        input("Enter drücken zum Fortfahren...")

def run_batch_download(urls, mode):
    """Run batch download"""
    if not urls:
        print("❌ Keine URLs zum Download vorhanden!")
        input("Enter drücken zum Fortfahren...")
        return

    try:
        output_dir = os.path.expanduser("~/Downloads")
        batch_download(urls, mode=mode, output_dir=output_dir)

        print("\n✅ Batch-Download abgeschlossen!")
        input("Enter drücken zum Fortfahren...")

    except Exception as e:
        print(f"❌ Fehler: {e}")
        input("Enter drücken zum Fortfahren...")

def main():
    """Main function"""

    while True:
        clear_screen()
        show_menu()

        choice = input("Auswahl (1-5): ").strip()

        if choice == "1":
            url = get_youtube_url()
            run_downloader(url, "video")

        elif choice == "2":
            url = get_youtube_url()
            run_downloader(url, "audio")

        elif choice == "3":
            urls = get_batch_urls()
            run_batch_download(urls, "video")

        elif choice == "4":
            urls = get_batch_urls()
            run_batch_download(urls, "audio")

        elif choice == "5":
            print("\n👋 Auf Wiedersehen!")
            break

        else:
            print("❌ Ungültige Auswahl!")
            input("Enter drücken zum Fortfahren...")

if __name__ == "__main__":
    main()