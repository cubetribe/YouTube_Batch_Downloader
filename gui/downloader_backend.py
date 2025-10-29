#!/usr/bin/env python3
"""
Download Backend Integration for GUI
"""

import os
import sys
import threading
import tempfile
import json
import copy
from pathlib import Path
from typing import Callable, Optional, Dict, Any, List
import yt_dlp
from PIL import Image
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.flac import FLAC, Picture

# Import existing utilities from the CLI version
import re
import requests
import subprocess

from .progress import ProgressTracker, ThreadSafeGUIUpdater

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 "
    "Safari/537.36"
)

DEFAULT_HTTP_HEADERS = {
    'User-Agent': DEFAULT_USER_AGENT,
    'Accept-Language': 'en-US,en;q=0.9',
}


class VideoInfo:
    """Video information class"""
    def __init__(self, info_dict: Dict[str, Any]):
        self.title = info_dict.get('title', 'Unknown')
        self.uploader = info_dict.get('uploader', 'Unknown')
        self.duration = info_dict.get('duration', 0)
        self.view_count = info_dict.get('view_count', 0)
        self.url = info_dict.get('webpage_url', '')
        self.thumbnail = info_dict.get('thumbnail', '')
        self.description = info_dict.get('description', '')
        self.is_playlist = 'entries' in info_dict
        self.entries = []

        if self.is_playlist:
            self.entries = [
                {
                    'title': entry.get('title', f'Video {i+1}'),
                    'id': entry.get('id', ''),
                    'url': entry.get('webpage_url', ''),
                    'duration': entry.get('duration', 0)
                }
                for i, entry in enumerate(info_dict.get('entries', []))
            ]

    def format_duration(self, seconds: int) -> str:
        """Format duration in human-readable format"""
        if seconds <= 0:
            return "Unknown"

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"


class DownloadOptions:
    """Download options configuration"""
    def __init__(self):
        self.format_type = "video"  # "video" or "audio"
        self.audio_format = "mp3"   # "mp3", "m4a", "flac"
        self.video_quality = "best" # "best", "1080p", "720p", etc.
        self.audio_quality = "best" # "best", "320kbps", "192kbps", etc.
        self.output_dir = str(Path.home() / 'Downloads')
        self.include_subtitles = True
        self.include_thumbnail = True
        self.include_metadata = True
        self.playlist_start = None
        self.playlist_end = None


class DownloadBackend:
    """Main download backend class"""

    def __init__(self, gui_root=None):
        self.gui_root = gui_root
        self.progress_tracker = None
        self.gui_updater = None
        self.is_downloading = False
        self.current_download_thread = None

        # Callbacks
        self.on_progress = None
        self.on_complete = None
        self.on_error = None
        self.on_log = None

    def set_callbacks(self,
                     on_progress: Optional[Callable] = None,
                     on_complete: Optional[Callable] = None,
                     on_error: Optional[Callable] = None,
                     on_log: Optional[Callable] = None):
        """Set callback functions for GUI updates"""
        self.on_progress = on_progress
        self.on_complete = on_complete
        self.on_error = on_error
        self.on_log = on_log

        if self.gui_root and self.on_progress:
            self.gui_updater = ThreadSafeGUIUpdater(self.gui_root, self.on_progress)
            self.progress_tracker = ProgressTracker(self.gui_updater.schedule_update)

    def get_video_info(self, url: str) -> Optional[VideoInfo]:
        """Get video information without downloading"""
        try:
            self._log("Hole Video-Informationen...")

            base_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'noplaylist': True,
                'forcejson': True,
                'user_agent': DEFAULT_USER_AGENT,
                'http_headers': DEFAULT_HTTP_HEADERS.copy(),
                'extractor_args': {'youtube': {'player_client': ['android']}},
            }

            strategies = [
                {
                    'name': 'Android Client (no cookies)',
                    'opts': copy.deepcopy(base_opts)
                }
            ]

            for browser in ('chrome', 'firefox', 'safari'):
                browser_opts = copy.deepcopy(base_opts)
                browser_opts['cookiesfrombrowser'] = (browser,)
                strategies.append({
                    'name': f'{browser.title()} Cookies',
                    'opts': browser_opts
                })

            web_fallback = copy.deepcopy(base_opts)
            web_fallback['extractor_args'] = {'youtube': {'player_client': ['web']}}
            strategies.append({
                'name': 'Web Client (fallback)',
                'opts': web_fallback
            })

            for strategy in strategies:
                try:
                    self._log(f"Versuche Info-Extraktion mit: {strategy['name']}")
                    with yt_dlp.YoutubeDL(strategy['opts']) as ydl:
                        info = ydl.extract_info(url, download=False)
                        self._log(f"✓ Info-Extraktion erfolgreich mit {strategy['name']}")
                        return VideoInfo(info)
                except Exception as e:
                    self._log(f"✗ Fehler mit {strategy['name']}: {str(e)}")
                    continue

            return None

        except Exception as e:
            self._error(f"Fehler beim Abrufen der Video-Informationen: {str(e)}")
            return None

    def download(self, url: str, options: DownloadOptions) -> bool:
        """Start download in separate thread"""
        if self.is_downloading:
            self._error("Download bereits aktiv")
            return False

        self.is_downloading = True

        self.current_download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, options),
            daemon=True
        )
        self.current_download_thread.start()
        return True

    def cancel_download(self):
        """Cancel current download"""
        if self.is_downloading:
            self.is_downloading = False
            self._log("Download wird abgebrochen...")

    def _download_worker(self, url: str, options: DownloadOptions):
        """Download worker function running in separate thread"""
        try:
            self._log(f"Starte Download: {url}")
            self._log(f"Ausgabeverzeichnis: {options.output_dir}")

            # Create output directory if it doesn't exist
            os.makedirs(options.output_dir, exist_ok=True)

            # Build yt-dlp options
            ydl_opts = self._build_ydl_opts(options)

            # Add progress hook if available
            if self.progress_tracker:
                self.progress_tracker.reset()
                ydl_opts['progress_hooks'] = [self.progress_tracker.progress_hook]

            # Try download with adaptive fallback strategies
            success = self._attempt_download_with_fallbacks(url, ydl_opts)

            if success:
                self._log("Download erfolgreich abgeschlossen!")
                self._complete()
            else:
                self._error("Download fehlgeschlagen - alle Fallback-Optionen ausgeschöpft")

        except Exception as e:
            error_msg = str(e)
            self._log(f"Download-Fehler: {error_msg}")
            self._error(error_msg)
        finally:
            self.is_downloading = False

    def _attempt_download_with_fallbacks(self, url: str, base_opts: Dict[str, Any]) -> bool:
        """Attempt download with various fallback strategies"""
        fallback_strategies: List[Dict[str, Any]] = []

        # Strategy 1: Android client without cookies (works for most videos)
        fallback_strategies.append({
            'name': 'Android Client (no cookies)',
            'opts': copy.deepcopy(base_opts)
        })

        # Strategies 2-4: Reuse Android client but try available browser cookies
        for browser in ('chrome', 'firefox', 'safari'):
            browser_opts = copy.deepcopy(base_opts)
            browser_opts['cookiesfrombrowser'] = (browser,)
            fallback_strategies.append({
                'name': f'{browser.title()} Cookies',
                'opts': browser_opts
            })

        # Strategy 5: Web client without cookies (last resort)
        web_opts = copy.deepcopy(base_opts)
        web_opts.pop('cookiesfrombrowser', None)
        web_opts['extractor_args'] = {'youtube': {'player_client': ['web']}}
        fallback_strategies.append({
            'name': 'Web Client (no cookies)',
            'opts': web_opts
        })

        for i, strategy in enumerate(fallback_strategies, 1):
            if not self.is_downloading:  # Check if cancelled
                return False

            try:
                self._log(f"Versuch {i}/{len(fallback_strategies)}: {strategy['name']}")

                with yt_dlp.YoutubeDL(strategy['opts']) as ydl:
                    ydl.download([url])

                self._log(f"✓ Erfolgreich mit {strategy['name']}")
                return True

            except Exception as e:
                error_msg = str(e)
                self._log(f"✗ Fehler mit {strategy['name']}: {error_msg}")

                # Don't retry for certain permanent errors
                if any(keyword in error_msg.lower() for keyword in
                       ['private video', 'video unavailable', 'removed by user']):
                    self._log("Permanenter Fehler erkannt - keine weiteren Versuche")
                    return False

                continue

        return False

    def _build_ydl_opts(self, options: DownloadOptions) -> Dict[str, Any]:
        """Build yt-dlp options dictionary"""

        # Base options
        ydl_opts = {
            'outtmpl': self._get_output_template(options),
            'noplaylist': True,
            'retries': 3,
            'fragment_retries': 3,
            'concurrent_fragment_downloads': 1,
            'writeinfojson': False,
            'writedescription': options.include_metadata,
            'writesubtitles': options.include_subtitles and options.format_type == "video",
            'writeautomaticsub': options.include_subtitles and options.format_type == "video",
            'subtitleslangs': ['de', 'en'],
            'ignoreerrors': False,
            'user_agent': DEFAULT_USER_AGENT,
            'http_headers': DEFAULT_HTTP_HEADERS.copy(),
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                }
            },
        }

        # Format-specific options
        if options.format_type == "audio":
            ydl_opts.update(self._get_audio_opts(options))
        else:
            ydl_opts.update(self._get_video_opts(options))

        # Playlist options
        if options.playlist_start or options.playlist_end:
            if options.playlist_start:
                ydl_opts['playliststart'] = options.playlist_start
            if options.playlist_end:
                ydl_opts['playlistend'] = options.playlist_end

        return ydl_opts

    def _get_output_template(self, options: DownloadOptions) -> str:
        """Get output filename template"""
        return os.path.join(options.output_dir, "%(title)s.%(ext)s")

    def _get_audio_opts(self, options: DownloadOptions) -> Dict[str, Any]:
        """Get audio-specific yt-dlp options"""
        opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
        }

        if options.audio_format == "mp3":
            opts.update({
                'audioformat': 'mp3',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': self._get_audio_quality_value(options.audio_quality),
                }]
            })
        elif options.audio_format == "m4a":
            opts.update({
                'audioformat': 'm4a',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }]
            })
        elif options.audio_format == "flac":
            opts.update({
                'audioformat': 'flac',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                }]
            })

        return opts

    def _get_video_opts(self, options: DownloadOptions) -> Dict[str, Any]:
        """Get video-specific yt-dlp options"""
        # Video format selection
        if options.video_quality == "best":
            video_format = 'bv*+ba/b'
        else:
            height = ''.join(filter(str.isdigit, options.video_quality))
            if height:
                video_format = f'bv*[height<={height}]+ba/b[height<={height}]'
            else:
                video_format = 'bv*+ba/b'

        return {
            'format': video_format,
            'merge_output_format': 'mp4',
            'embedsubtitles': options.include_subtitles,
        }

    def _get_audio_quality_value(self, quality: str) -> str:
        """Convert audio quality to bitrate value"""
        quality_map = {
            "best": "320",
            "320kbps": "320",
            "192kbps": "192",
            "128kbps": "128"
        }
        return quality_map.get(quality, "192")

    def check_available_browsers(self) -> List[str]:
        """Check which browsers are available for cookie extraction"""
        available_browsers = []
        browsers_to_check = ['chrome', 'firefox', 'safari', 'edge']

        for browser in browsers_to_check:
            try:
                # Try to extract cookies to test if browser is available
                import tempfile
                with tempfile.NamedTemporaryFile(delete=True) as tmp:
                    test_opts = {
                        'cookiesfrombrowser': (browser,),
                        'quiet': True,
                        'no_warnings': True,
                    }
                    with yt_dlp.YoutubeDL(test_opts) as ydl:
                        # Don't actually extract, just test if cookies are accessible
                        pass
                    available_browsers.append(browser)
            except Exception:
                continue

        self._log(f"Verfügbare Browser für Cookies: {', '.join(available_browsers) if available_browsers else 'keine'}")
        return available_browsers

    def check_yt_dlp_update(self) -> Optional[str]:
        """Check for yt-dlp updates and return new version if available"""
        try:
            # Get current version
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'],
                                   capture_output=True, text=True, timeout=10)
            current_version = result.stdout.strip()

            # Get latest version from PyPI
            response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=10)
            latest_version = response.json()["info"]["version"]

            if current_version != latest_version:
                return latest_version

        except Exception:
            pass

        return None

    def update_yt_dlp(self) -> bool:
        """Update yt-dlp to latest version"""
        try:
            self._log("Aktualisiere yt-dlp...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp'],
                                   capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                self._log("yt-dlp erfolgreich aktualisiert")
                return True
            else:
                self._error(f"Fehler beim Aktualisieren: {result.stderr}")
                return False

        except Exception as e:
            self._error(f"Fehler beim Aktualisieren: {str(e)}")
            return False

    def _log(self, message: str):
        """Log message"""
        if self.on_log:
            self.on_log(message)

    def _error(self, message: str):
        """Handle error"""
        if self.on_error:
            self.on_error(message)

    def _complete(self):
        """Handle completion"""
        if self.on_complete:
            self.on_complete()


# Utility functions adapted from original CLI version
def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem"""
    return re.sub(r'[\/\\\:\*\?"<>\|]', '_', filename)


def is_valid_url(url: str) -> bool:
    """Check if URL is valid for downloading"""
    patterns = [
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be)',
        r'(https?://)?(www\.)?instagram\.com',
        r'(https?://)?(www\.)?facebook\.com',
        r'(https?://)?(www\.)?tiktok\.com'
    ]
    return any(re.search(pattern, url, re.IGNORECASE) for pattern in patterns)


def get_clipboard_url():
    """Get URL from clipboard if it's a valid video URL"""
    try:
        import pyperclip
        text = pyperclip.paste().strip()
        if is_valid_url(text):
            return text
    except Exception:
        pass
    return None
