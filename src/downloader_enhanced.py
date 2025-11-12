#!/usr/bin/env python3
"""
Enhanced YouTube Downloader
Provides a reliable way to download videos in 4K or 1080p.
"""

import yt_dlp
import os
import logging
from typing import Optional

class EnhancedDownloader:
    """
    A downloader that strictly attempts to download in 4K, falls back to 1080p,
    and aborts if neither is available. It also logs all operations.
    """

    def __init__(self, output_dir: Optional[str] = None):
        """
        Initializes the downloader and sets up logging.

        Args:
            output_dir: The directory where downloads should be saved.
                        Defaults to '~/Downloads'.
        """
        self.output_dir = output_dir or os.path.expanduser("~/Downloads")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers if this class is instantiated multiple times
        if not self.logger.handlers:
            log_file_path = os.path.join(os.path.dirname(__file__), '..', 'download_log.txt')
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # Also log to console for immediate feedback
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def _get_base_opts(self, output_path: str) -> dict:
        """Returns the base options for yt-dlp."""
        return {
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'retries': 3,
            'fragment_retries': 3,
            'quiet': True,  # We do our own logging
            'no_warnings': True,
            'ignoreerrors': False, # Important: Fail on error to allow fallback
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            },
            'cookiesfrombrowser': ('chrome', None), # Try to use chrome cookies
        }

    def _attempt_download(self, url: str, format_selector: str, quality_label: str) -> bool:
        """
        Tries to download a video with a specific format selector.

        Args:
            url: The YouTube URL.
            format_selector: The yt-dlp format string.
            quality_label: A label for logging (e.g., "4K").

        Returns:
            True if download was successful, False otherwise.
        """
        opts = self._get_base_opts(os.path.join(self.output_dir, '%(title)s.%(ext)s'))
        opts['format'] = format_selector

        self.logger.info(f"Attempting to download '{url}' as {quality_label}...")

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                # The download happens here
                ydl.extract_info(url, download=True)
            self.logger.info(f"SUCCESS: Downloaded '{url}' as {quality_label}.")
            return True
        except yt_dlp.utils.DownloadError as e:
            # This error is often raised when no suitable stream is found
            self.logger.warning(f"Could not download '{url}' as {quality_label}. Reason: No suitable stream found or access denied. ({str(e)[:100]}...)")
            return False
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while trying to download '{url}' as {quality_label}: {e}")
            return False

    def download_video(self, url: str):
        """
        Downloads a video using the 4K > 1080p > Abort logic.

        Args:
            url: The YouTube URL to download.
        """
        self.logger.info(f"--- Starting download process for URL: {url} ---")

        # 1. Attempt 4K download
        format_4k = 'bestvideo[height>=2160]+bestaudio/best[height>=2160]'
        if self._attempt_download(url, format_4k, "4K (2160p)"):
            return

        # 2. Attempt 1080p download if 4K failed
        self.logger.info("4K download failed, falling back to 1080p.")
        format_1080p = 'bestvideo[height>=1080]+bestaudio/best[height>=1080]'
        if self._attempt_download(url, format_1080p, "Full HD (1080p)"):
            return

        # 3. Abort if both failed
        self.logger.error(f"FAILURE: Could not download '{url}'. No 4K or 1080p stream available or accessible.")

    def download_audio(self, url: str):
        """
        Downloads the best available audio and converts it to MP3.

        Args:
            url: The YouTube URL to download.
        """
        self.logger.info(f"--- Starting AUDIO download process for URL: {url} ---")

        opts = self._get_base_opts(os.path.join(self.output_dir, '%(title)s.%(ext)s'))
        opts['format'] = 'bestaudio/best'
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320', # High quality MP3
        }]

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.extract_info(url, download=True)
            self.logger.info(f"SUCCESS: Downloaded audio for '{url}' as MP3.")
        except Exception as e:
            self.logger.error(f"FAILURE: Could not download audio for '{url}'. Reason: {e}")

def batch_download(urls: list[str], mode: str, output_dir: Optional[str] = None):
    """
    Performs a batch download of videos or audios.

    Args:
        urls: A list of YouTube URLs.
        mode: 'video' or 'audio'.
        output_dir: The directory to save files in.
    """
    downloader = EnhancedDownloader(output_dir)
    for url in urls:
        if mode == 'video':
            downloader.download_video(url)
        elif mode == 'audio':
            downloader.download_audio(url)
