#!/usr/bin/env python3
"""
Video Downloader GUI - Starter Script
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []

    try:
        import yt_dlp
    except ImportError:
        missing_deps.append("yt-dlp")

    try:
        import PIL
    except ImportError:
        missing_deps.append("Pillow")

    try:
        import mutagen
    except ImportError:
        missing_deps.append("mutagen")

    try:
        import pyperclip
    except ImportError:
        missing_deps.append("pyperclip")

    try:
        import requests
    except ImportError:
        missing_deps.append("requests")

    return missing_deps

def show_error_dialog(title, message):
    """Show error dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    messagebox.showerror(title, message)
    root.destroy()

def install_dependencies(missing_deps):
    """Show installation instructions for missing dependencies"""
    deps_str = " ".join(missing_deps)
    message = f"""Fehlende Abhängigkeiten: {', '.join(missing_deps)}

Bitte installieren Sie diese mit:
pip install {deps_str}

Oder führen Sie das folgende Kommando aus:
python -m pip install {deps_str}

Danach starten Sie die Anwendung erneut."""

    show_error_dialog("Fehlende Abhängigkeiten", message)

def main():
    """Main function to start the GUI"""

    # Set working directory to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Check dependencies first
    missing_deps = check_dependencies()
    if missing_deps:
        install_dependencies(missing_deps)
        return 1

    try:
        # Import and start the GUI
        from gui.main_window import MainWindow

        # Create and run the application
        app = MainWindow()
        app.run()

        return 0

    except ImportError as e:
        error_msg = f"""Fehler beim Import der GUI-Module:
{str(e)}

Stellen Sie sicher, dass Sie sich im richtigen Verzeichnis befinden und alle Dateien vorhanden sind.

Verzeichnis: {script_dir}"""
        show_error_dialog("Import-Fehler", error_msg)
        return 1

    except Exception as e:
        error_msg = f"""Unerwarteter Fehler beim Starten der Anwendung:
{str(e)}

Bitte überprüfen Sie die Konsole für weitere Details."""
        show_error_dialog("Anwendungsfehler", error_msg)

        # Print detailed error to console
        import traceback
        print(f"Fehler beim Starten der GUI: {e}")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nAnwendung durch Benutzer beendet.")
        sys.exit(0)
    except Exception as e:
        print(f"Kritischer Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)