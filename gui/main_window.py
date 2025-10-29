#!/usr/bin/env python3
"""
Video Downloader - Main GUI Window
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
import pyperclip
import re
from pathlib import Path

from .downloader_backend import DownloadBackend, DownloadOptions, VideoInfo, is_valid_url, get_clipboard_url

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Video Downloader")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)

        # Application state
        self.config_file = "gui_config.json"
        self.config = self.load_config()
        self.is_downloading = False
        self.download_thread = None

        # Progress tracking
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Bereit")
        self.speed_var = tk.StringVar(value="")
        self.eta_var = tk.StringVar(value="")

        # Download backend
        self.backend = DownloadBackend(self.root)
        self.backend.set_callbacks(
            on_progress=self.update_progress,
            on_complete=self.download_complete,
            on_error=self.download_error,
            on_log=self.log
        )

        # Create GUI
        self.create_widgets()
        self.setup_layout()
        self.bind_events()

        # Load saved settings
        self.load_saved_settings()

        # Auto-detect clipboard URL
        self.check_clipboard()

    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'last_download_dir': str(Path.home() / 'Downloads'),
            'default_format': 'video',
            'default_quality': 'best',
            'window_geometry': '800x600'
        }

    def save_config(self):
        """Save configuration to JSON file"""
        try:
            # Update window geometry
            self.config['window_geometry'] = self.root.geometry()
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass

    def create_widgets(self):
        """Create all GUI widgets"""

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Video Downloader",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # URL Section
        url_frame = ttk.LabelFrame(main_frame, text="Video URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)

        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var,
                                  font=('Arial', 10))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        paste_btn = ttk.Button(url_frame, text="Einfügen", command=self.paste_url)
        paste_btn.grid(row=0, column=1)

        # Download Directory Section
        dir_frame = ttk.LabelFrame(main_frame, text="Download-Verzeichnis", padding="10")
        dir_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)

        self.dir_var = tk.StringVar()
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var,
                                  font=('Arial', 10), state='readonly')
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        browse_btn = ttk.Button(dir_frame, text="Durchsuchen...",
                               command=self.browse_directory)
        browse_btn.grid(row=0, column=1)

        # Format & Quality Section
        options_frame = ttk.LabelFrame(main_frame, text="Download-Optionen", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Format selection
        ttk.Label(options_frame, text="Format:").grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        self.format_var = tk.StringVar()
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var,
                                   values=['video', 'audio'], state='readonly', width=10)
        format_combo.grid(row=0, column=1, padx=(0, 20))
        format_combo.bind('<<ComboboxSelected>>', self.on_format_change)

        # Audio format selection (initially hidden)
        self.audio_label = ttk.Label(options_frame, text="Audio Format:")
        self.audio_var = tk.StringVar()
        self.audio_combo = ttk.Combobox(options_frame, textvariable=self.audio_var,
                                       values=['mp3', 'm4a', 'flac'], state='readonly', width=10)

        # Quality selection
        ttk.Label(options_frame, text="Qualität:").grid(row=0, column=4, padx=(0, 10), sticky=tk.W)
        self.quality_var = tk.StringVar()
        self.quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var,
                                         values=['best', '1080p', '720p', '480p', '360p'],
                                         state='readonly', width=10)
        self.quality_combo.grid(row=0, column=5)

        # Download Button
        self.download_btn = ttk.Button(main_frame, text="Download starten",
                                      command=self.start_download)
        self.download_btn.grid(row=4, column=0, columnspan=3, pady=20)

        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="Download-Fortschritt", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)

        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Status labels
        status_frame = ttk.Frame(progress_frame)
        status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(2, weight=1)

        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=0, sticky=tk.W)

        self.speed_label = ttk.Label(status_frame, textvariable=self.speed_var)
        self.speed_label.grid(row=0, column=1)

        self.eta_label = ttk.Label(status_frame, textvariable=self.eta_var)
        self.eta_label.grid(row=0, column=2, sticky=tk.E)

        # Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8,
                                                 font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def setup_layout(self):
        """Setup the layout and make it responsive"""
        # This is handled in create_widgets with grid configuration
        pass

    def bind_events(self):
        """Bind keyboard and window events"""
        self.root.bind('<Control-v>', lambda e: self.paste_url())
        self.root.bind('<Command-v>', lambda e: self.paste_url())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_saved_settings(self):
        """Load saved settings from config"""
        self.dir_var.set(self.config.get('last_download_dir', str(Path.home() / 'Downloads')))
        self.format_var.set(self.config.get('default_format', 'video'))
        self.quality_var.set(self.config.get('default_quality', 'best'))
        self.audio_var.set(self.config.get('default_audio_format', 'mp3'))

        # Set window geometry
        try:
            self.root.geometry(self.config.get('window_geometry', '800x600'))
        except:
            pass

        self.on_format_change()

    def check_clipboard(self):
        """Check clipboard for video URLs and auto-fill"""
        try:
            clipboard_url = get_clipboard_url()
            if clipboard_url:
                self.url_var.set(clipboard_url)
                self.log("URL aus Zwischenablage erkannt")
        except:
            pass

    def paste_url(self):
        """Paste URL from clipboard"""
        try:
            clipboard_text = pyperclip.paste().strip()
            if clipboard_text:
                self.url_var.set(clipboard_text)
                self.log("URL eingefügt")
        except:
            pass

    def browse_directory(self):
        """Open directory browser"""
        initial_dir = self.dir_var.get() or str(Path.home() / 'Downloads')
        directory = filedialog.askdirectory(initialdir=initial_dir,
                                          title="Download-Verzeichnis auswählen")
        if directory:
            self.dir_var.set(directory)
            self.config['last_download_dir'] = directory
            self.save_config()

    def on_format_change(self, event=None):
        """Handle format selection change"""
        format_type = self.format_var.get()
        if format_type == 'audio':
            # Show audio format options
            self.audio_label.grid(row=0, column=2, padx=(20, 10), sticky=tk.W)
            self.audio_combo.grid(row=0, column=3, padx=(0, 20))
            # Update quality options for audio
            self.quality_combo['values'] = ['best', '320kbps', '192kbps', '128kbps']
        else:
            # Hide audio format options
            self.audio_label.grid_remove()
            self.audio_combo.grid_remove()
            # Update quality options for video
            self.quality_combo['values'] = ['best', '1080p', '720p', '480p', '360p']

    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_download(self):
        """Start the download process"""
        url = self.url_var.get().strip()
        download_dir = self.dir_var.get().strip()

        # Validation
        if not url:
            messagebox.showerror("Fehler", "Bitte geben Sie eine URL ein")
            return

        if not is_valid_url(url):
            messagebox.showerror("Fehler", "Ungültige Video-URL")
            return

        if not download_dir:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Download-Verzeichnis")
            return

        if not os.path.exists(download_dir):
            try:
                os.makedirs(download_dir)
            except:
                messagebox.showerror("Fehler", "Verzeichnis konnte nicht erstellt werden")
                return

        # Create download options
        options = DownloadOptions()
        options.output_dir = download_dir
        options.format_type = self.format_var.get()
        options.video_quality = self.quality_var.get()

        if options.format_type == 'audio':
            options.audio_format = self.audio_var.get()
            options.audio_quality = self.quality_var.get()

        # Start download
        self.is_downloading = True
        self.download_btn.config(text="Wird heruntergeladen...", state='disabled')
        self.progress_var.set(0)
        self.status_var.set("Vorbereitung...")

        success = self.backend.download(url, options)
        if not success:
            self.is_downloading = False
            self.download_btn.config(text="Download starten", state='normal')

    def update_progress(self, progress_info):
        """Update progress from backend"""
        self.progress_var.set(progress_info['percentage'])
        self.status_var.set(f"{progress_info['status']} - {progress_info['size_str']}")
        self.speed_var.set(progress_info['speed_str'])
        self.eta_var.set(progress_info['eta_str'])

    def download_error(self, error_message):
        """Handle download error"""
        self.log(f"Fehler: {error_message}")
        messagebox.showerror("Download-Fehler", error_message)
        self.is_downloading = False
        self.download_btn.config(text="Download starten", state='normal')
        self.status_var.set("Fehler")
        self.speed_var.set("")
        self.eta_var.set("")

    def download_complete(self):
        """Called when download is complete"""
        self.is_downloading = False
        self.download_btn.config(text="Download starten", state='normal')
        self.status_var.set("Abgeschlossen")
        self.speed_var.set("")
        self.eta_var.set("")

    def cancel_download(self):
        """Cancel current download"""
        if self.is_downloading:
            self.backend.cancel_download()
            self.is_downloading = False
            self.download_btn.config(text="Download starten", state='normal')
            self.status_var.set("Abgebrochen")
            self.speed_var.set("")
            self.eta_var.set("")
            self.log("Download abgebrochen")

    def on_close(self):
        """Handle window close event"""
        # Stop any running download
        if self.is_downloading:
            if messagebox.askokcancel("Beenden", "Download wird abgebrochen. Trotzdem beenden?"):
                self.backend.cancel_download()
                self.is_downloading = False
            else:
                return

        self.save_config()
        self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == '__main__':
    app = MainWindow()
    app.run()