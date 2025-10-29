#!/usr/bin/env python3
"""
Real-time Progress Handler for Video Downloads
"""

import threading
import time
from typing import Callable, Optional, Dict, Any


class ProgressTracker:
    """Real-time progress tracking for yt-dlp downloads"""

    def __init__(self, gui_callback: Optional[Callable] = None):
        self.gui_callback = gui_callback
        self.current_info = {}
        self.start_time = None
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.speed = 0
        self.eta = 0
        self.status = "idle"
        self.filename = ""
        self.lock = threading.Lock()

    def progress_hook(self, d: Dict[str, Any]):
        """
        Progress hook for yt-dlp
        This function is called by yt-dlp during download progress
        """
        with self.lock:
            self.current_info = d.copy()

            if d['status'] == 'downloading':
                self._handle_downloading(d)
            elif d['status'] == 'finished':
                self._handle_finished(d)
            elif d['status'] == 'error':
                self._handle_error(d)

            # Update GUI if callback is provided
            if self.gui_callback:
                self.gui_callback(self.get_progress_info())

    def _handle_downloading(self, d: Dict[str, Any]):
        """Handle downloading status"""
        self.status = "downloading"

        # Extract filename
        if 'filename' in d:
            self.filename = d['filename']

        # Get download progress
        if 'total_bytes' in d and d['total_bytes']:
            self.total_bytes = d['total_bytes']
        elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
            self.total_bytes = d['total_bytes_estimate']

        if 'downloaded_bytes' in d:
            self.downloaded_bytes = d['downloaded_bytes']

        # Calculate speed (bytes per second)
        if 'speed' in d and d['speed']:
            self.speed = d['speed']
        else:
            self.speed = 0

        # Calculate ETA
        if 'eta' in d and d['eta']:
            self.eta = d['eta']
        elif self.speed > 0 and self.total_bytes > 0:
            remaining_bytes = self.total_bytes - self.downloaded_bytes
            self.eta = remaining_bytes / self.speed
        else:
            self.eta = 0

        # Set start time if not set
        if self.start_time is None:
            self.start_time = time.time()

    def _handle_finished(self, d: Dict[str, Any]):
        """Handle finished status"""
        self.status = "finished"
        if 'filename' in d:
            self.filename = d['filename']

        # Set progress to 100%
        if self.total_bytes > 0:
            self.downloaded_bytes = self.total_bytes

    def _handle_error(self, d: Dict[str, Any]):
        """Handle error status"""
        self.status = "error"

    def get_progress_info(self) -> Dict[str, Any]:
        """Get current progress information for GUI updates"""
        with self.lock:
            # Calculate percentage
            if self.total_bytes > 0:
                percentage = (self.downloaded_bytes / self.total_bytes) * 100
            else:
                percentage = 0

            return {
                'status': self.status,
                'filename': self.filename,
                'percentage': percentage,
                'downloaded_bytes': self.downloaded_bytes,
                'total_bytes': self.total_bytes,
                'speed': self.speed,
                'eta': self.eta,
                'speed_str': self._format_speed(self.speed),
                'eta_str': self._format_eta(self.eta),
                'size_str': self._format_size_progress(self.downloaded_bytes, self.total_bytes)
            }

    def _format_speed(self, speed: float) -> str:
        """Format download speed in human-readable format"""
        if speed <= 0:
            return ""

        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        size = speed

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.1f} {units[unit_index]}"

    def _format_eta(self, eta: float) -> str:
        """Format ETA in human-readable format"""
        if eta <= 0:
            return ""

        if eta < 60:
            return f"{int(eta)}s"
        elif eta < 3600:
            minutes = int(eta // 60)
            seconds = int(eta % 60)
            return f"{minutes}m {seconds}s"
        else:
            hours = int(eta // 3600)
            minutes = int((eta % 3600) // 60)
            return f"{hours}h {minutes}m"

    def _format_size_progress(self, downloaded: int, total: int) -> str:
        """Format size progress in human-readable format"""
        if total <= 0:
            return self._format_bytes(downloaded)

        return f"{self._format_bytes(downloaded)} / {self._format_bytes(total)}"

    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes in human-readable format"""
        if bytes_value <= 0:
            return "0 B"

        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = float(bytes_value)

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.1f} {units[unit_index]}"

    def reset(self):
        """Reset progress tracker for new download"""
        with self.lock:
            self.current_info = {}
            self.start_time = None
            self.total_bytes = 0
            self.downloaded_bytes = 0
            self.speed = 0
            self.eta = 0
            self.status = "idle"
            self.filename = ""


class ThreadSafeGUIUpdater:
    """Thread-safe GUI updater for progress updates"""

    def __init__(self, root, update_callback: Callable):
        self.root = root
        self.update_callback = update_callback
        self.update_queue = []
        self.lock = threading.Lock()

    def schedule_update(self, progress_info: Dict[str, Any]):
        """Schedule a GUI update from any thread"""
        with self.lock:
            self.update_queue.append(progress_info)

        # Schedule the update on the main thread
        self.root.after_idle(self._process_updates)

    def _process_updates(self):
        """Process all pending updates on the main thread"""
        with self.lock:
            if self.update_queue:
                # Get the latest update (discard older ones to avoid lag)
                latest_update = self.update_queue[-1]
                self.update_queue.clear()

                # Call the update callback
                self.update_callback(latest_update)


# Example usage and testing
if __name__ == '__main__':
    import tkinter as tk
    from tkinter import ttk

    def test_progress_tracker():
        """Test the progress tracker with a simple GUI"""

        root = tk.Tk()
        root.title("Progress Tracker Test")
        root.geometry("500x200")

        # Create progress bar and labels
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
        progress_bar.pack(pady=20, padx=20, fill='x')

        status_label = ttk.Label(root, text="Status: Idle")
        status_label.pack(pady=5)

        speed_label = ttk.Label(root, text="Speed: ")
        speed_label.pack(pady=5)

        eta_label = ttk.Label(root, text="ETA: ")
        eta_label.pack(pady=5)

        def update_gui(progress_info):
            """Update GUI with progress information"""
            progress_var.set(progress_info['percentage'])
            status_label.config(text=f"Status: {progress_info['status']} - {progress_info['size_str']}")
            speed_label.config(text=f"Speed: {progress_info['speed_str']}")
            eta_label.config(text=f"ETA: {progress_info['eta_str']}")

        # Create GUI updater
        gui_updater = ThreadSafeGUIUpdater(root, update_gui)

        # Create progress tracker
        tracker = ProgressTracker(gui_updater.schedule_update)

        # Simulate download progress
        def simulate_download():
            import random

            total_size = 100_000_000  # 100 MB
            downloaded = 0

            while downloaded < total_size:
                # Simulate download chunk
                chunk_size = random.randint(100_000, 1_000_000)
                downloaded = min(downloaded + chunk_size, total_size)
                speed = random.uniform(1_000_000, 5_000_000)  # 1-5 MB/s

                # Create mock yt-dlp progress dict
                progress_dict = {
                    'status': 'downloading',
                    'filename': 'test_video.mp4',
                    'downloaded_bytes': downloaded,
                    'total_bytes': total_size,
                    'speed': speed,
                    'eta': (total_size - downloaded) / speed if speed > 0 else 0
                }

                tracker.progress_hook(progress_dict)
                time.sleep(0.1)

            # Finished
            tracker.progress_hook({
                'status': 'finished',
                'filename': 'test_video.mp4'
            })

        # Start simulation in separate thread
        sim_thread = threading.Thread(target=simulate_download, daemon=True)
        sim_thread.start()

        root.mainloop()

    test_progress_tracker()