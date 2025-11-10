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
    print("=" * 60)
    print("🎬 YOUTUBE HD/4K DOWNLOADER 🎵")
    print("=" * 60)
    print()
    print("📹 EINZELNE DOWNLOADS:")
    print("  1️⃣  Video herunterladen (HD/4K)")
    print("  2️⃣  Audio herunterladen (MP3 320kbps)")
    print()
    print("📦 BATCH DOWNLOADS:")
    print("  3️⃣  Batch Download - Videos (HD/4K)")
    print("  4️⃣  Batch Download - Audios (MP3)")
    print()
    print("🔧 ERWEITERTE OPTIONEN:")
    print("  5️⃣  Ultimate HD Downloader (Multi-Strategie)")
    print("  6️⃣  HD-Only Download (min. 1080p, lehnt niedrigere ab)")
    print("  7️⃣  PO Token Setup (für bessere Qualität)")
    print()
    print("  8️⃣  Beenden")
    print()
    print("=" * 60)
    print("ℹ️  Hinweis: Für beste Qualität in Chrome bei YouTube anmelden!")
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

def run_ultimate_downloader():
    """Run the Ultimate HD Downloader for difficult videos"""
    try:
        print("\n" + "=" * 60)
        print("🚀 ULTIMATE HD DOWNLOADER")
        print("=" * 60)
        print("Verwendet mehrere Strategien für beste Qualität!")
        print("=" * 60 + "\n")

        url = get_youtube_url()

        # Import and use the ultimate downloader
        from download_ultimate import UltimateHDDownloader
        downloader = UltimateHDDownloader()
        downloader.download_hd(url)

        input("\nEnter drücken zum Fortfahren...")

    except ImportError:
        print("❌ download_ultimate.py nicht gefunden!")
        input("Enter drücken zum Fortfahren...")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        input("Enter drücken zum Fortfahren...")

def run_hd_only_downloader():
    """Run HD-Only downloader that rejects videos below 1080p"""
    try:
        print("\n" + "=" * 60)
        print("🎬 HD-ONLY DOWNLOADER")
        print("=" * 60)
        print("⚠️  Lehnt Videos unter 1080p ab!")
        print("=" * 60 + "\n")

        mode = input("Einzelnes Video oder Batch? (e/b) [e]: ").strip().lower() or "e"

        if mode == "b":
            # Batch mode
            urls = get_batch_urls()
            if urls:
                from download_hd import batch_download_hd
                batch_download_hd(urls)
        else:
            # Single video mode
            url = get_youtube_url()
            from download_hd import HDQualityDownloader
            downloader = HDQualityDownloader()
            downloader.download_hd(url)

        input("\nEnter drücken zum Fortfahren...")

    except ImportError:
        print("❌ download_hd.py nicht gefunden!")
        input("Enter drücken zum Fortfahren...")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        input("Enter drücken zum Fortfahren...")

def run_po_token_setup():
    """Setup PO Token for better quality"""
    try:
        print("\n" + "=" * 60)
        print("🔑 PO TOKEN SETUP")
        print("=" * 60)
        print()
        print("Ein PO Token kann helfen, HD-Videos herunterzuladen.")
        print()
        print("Anleitung:")
        print("1. Öffne YouTube in Chrome und melde dich an")
        print("2. Öffne Developer Tools (F12)")
        print("3. Network Tab → Reload → Suche 'player' Request")
        print("4. Finde 'po_token' im Response")
        print("5. Kopiere den Token (ohne Präfix)")
        print()
        print("Details: Siehe PO_TOKEN_ANLEITUNG.md")
        print("=" * 60 + "\n")

        from download_ultimate import UltimateHDDownloader
        downloader = UltimateHDDownloader()
        downloader.setup_po_token()

        input("\nEnter drücken zum Fortfahren...")

    except ImportError:
        print("❌ download_ultimate.py nicht gefunden!")
        input("Enter drücken zum Fortfahren...")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        input("Enter drücken zum Fortfahren...")

def main():
    """Main function"""

    while True:
        clear_screen()
        show_menu()

        choice = input("Auswahl (1-8): ").strip()

        if choice == "1":
            # Einzelnes Video in HD/4K
            url = get_youtube_url()
            run_downloader(url, "video")

        elif choice == "2":
            # Einzelnes Audio
            url = get_youtube_url()
            run_downloader(url, "audio")

        elif choice == "3":
            # Batch Videos in HD/4K
            urls = get_batch_urls()
            run_batch_download(urls, "video")

        elif choice == "4":
            # Batch Audios
            urls = get_batch_urls()
            run_batch_download(urls, "audio")

        elif choice == "5":
            # Ultimate HD Downloader
            run_ultimate_downloader()

        elif choice == "6":
            # HD-Only Downloader
            run_hd_only_downloader()

        elif choice == "7":
            # PO Token Setup
            run_po_token_setup()

        elif choice == "8":
            print("\n👋 Auf Wiedersehen!")
            break

        else:
            print("❌ Ungültige Auswahl!")
            input("Enter drücken zum Fortfahren...")

if __name__ == "__main__":
    main()