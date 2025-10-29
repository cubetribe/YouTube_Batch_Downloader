#!/usr/bin/env python3
"""
Video Downloader GUI - Setup Script
Automatische Installation aller Dependencies
"""

import sys
import subprocess
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True,
                               capture_output=True, text=True)
        print(f"✅ {description} erfolgreich")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei {description}:")
        print(f"   {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} ist zu alt")
        print("   Mindestens Python 3.8 erforderlich")
        return False

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} ist kompatibel")
    return True

def check_tkinter():
    """Check if Tkinter is available"""
    try:
        import tkinter
        print("✅ Tkinter ist verfügbar")
        return True
    except ImportError:
        print("❌ Tkinter ist nicht verfügbar")
        print("   Installieren Sie python3-tk:")
        if sys.platform.startswith('linux'):
            print("   sudo apt-get install python3-tk")
        elif sys.platform == 'darwin':
            print("   Tkinter sollte mit Python installiert sein")
        return False

def main():
    """Main setup function"""
    print("🎬 Video Downloader GUI - Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        return 1

    # Check Tkinter
    if not check_tkinter():
        return 1

    # Install/upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip",
                      "Aktualisiere pip"):
        return 1

    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements_gui.txt",
                      "Installiere Dependencies"):
        return 1

    # Check FFmpeg (optional but recommended)
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg ist verfügbar")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  FFmpeg nicht gefunden (optional aber empfohlen)")
        print("   Für beste Qualität installieren Sie FFmpeg:")
        if sys.platform == 'darwin':
            print("   brew install ffmpeg")
        elif sys.platform.startswith('linux'):
            print("   sudo apt-get install ffmpeg")
        elif sys.platform == 'win32':
            print("   Herunterladen von: https://ffmpeg.org/download.html")

    print("\n" + "=" * 40)
    print("🎉 Setup abgeschlossen!")
    print("\n📝 Nächste Schritte:")
    print("   1. Starten Sie die GUI mit: python start_gui.py")
    print("   2. Oder doppelklicken Sie auf 'YouTube Downloader.command' (Mac)")
    print("\n💡 Tipp: Fügen Sie URLs einfach in die Zwischenablage ein!")

    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        input("\nEnter drücken zum Beenden...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nSetup abgebrochen.")
        sys.exit(1)