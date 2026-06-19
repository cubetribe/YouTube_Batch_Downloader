"""yt-dlp engine: metadata extraction and downloads with live progress.

Two public entry points:
  * ``extract_info(url)``  -> normalized dict describing the video
  * ``download(url, ...)`` -> runs the download, streaming progress to a callback

Both use the same resilience strategy the CLI version learned the hard way:
try **without** browser cookies first (YouTube often returns a complete format
list that way), then retry **with** Chrome cookies if the first attempt fails.
"""

from __future__ import annotations

import os
import shutil
from typing import Callable, Optional

import yt_dlp

DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Downloads")

# Realistic desktop UA — helps YouTube hand back the full HD/4K format list.
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# Download quality presets exposed in the UI. Each maps to a yt-dlp format
# selector; ``postprocessors`` is optional (used for audio extraction).
FORMAT_PRESETS: dict[str, dict] = {
    # Selectors prefer separate video+audio (merged to mp4); the final bare
    # fallbacks prefer an mp4 container so a low-tier video doesn't silently
    # land as webm when the user asked for "best/4K".
    "best": {
        "label": "Beste Qualität (bis 4K)",
        "selector": "bestvideo*+bestaudio/best[ext=mp4]/best",
        "merge": "mp4",
    },
    "2160p": {
        "label": "4K (2160p) bevorzugt",
        "selector": (
            "bestvideo[height>=2160]+bestaudio/"
            "bestvideo[height>=1080]+bestaudio/best[ext=mp4]/best"
        ),
        "merge": "mp4",
    },
    "1080p": {
        "label": "Full HD (1080p)",
        "selector": (
            "bestvideo[height<=1080]+bestaudio/"
            "best[height<=1080][ext=mp4]/best[height<=1080]/best"
        ),
        "merge": "mp4",
    },
    "720p": {
        "label": "HD (720p)",
        "selector": (
            "bestvideo[height<=720]+bestaudio/"
            "best[height<=720][ext=mp4]/best[height<=720]/best"
        ),
        "merge": "mp4",
    },
    "audio": {
        "label": "Nur Audio (MP3, 320 kbps)",
        "selector": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
    },
}


class EngineError(Exception):
    """Raised when both cookie strategies fail. ``message`` is user-friendly."""


def format_presets_for_ui() -> list[dict]:
    """Return the presets as an ordered list of ``{id, label}`` for the frontend."""
    return [{"id": key, "label": preset["label"]} for key, preset in FORMAT_PRESETS.items()]


def _base_opts() -> dict:
    return {
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,  # we stream progress to the browser, not the terminal
        "retries": 5,
        "fragment_retries": 5,
        "ignoreerrors": False,  # fail loudly so the cookie fallback can kick in
        "http_headers": {
            "User-Agent": _USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    }


# Cookie strategies, tried in order. Empty dict = no browser cookies.
_STRATEGIES: list[tuple[str, dict]] = [
    ("ohne Browser-Cookies", {}),
    ("mit Chrome-Cookies", {"cookiesfrombrowser": ("chrome", None, None, None)}),
]


def _fmt_duration(seconds: Optional[float]) -> str:
    if not seconds:
        return ""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _normalize_info(info: dict) -> dict:
    """Reduce yt-dlp's huge info dict to what the UI actually needs."""
    heights = sorted(
        {
            f.get("height")
            for f in (info.get("formats") or [])
            if isinstance(f, dict) and f.get("height")
        },
        reverse=True,
    )
    thumb = info.get("thumbnail")
    if not thumb:
        thumbs = info.get("thumbnails") or []
        if thumbs:
            thumb = thumbs[-1].get("url")
    return {
        "id": info.get("id"),
        "title": info.get("title") or "Unbekannter Titel",
        "uploader": info.get("uploader") or info.get("channel") or "",
        "duration": info.get("duration"),
        # Format ourselves for a consistent M:SS / H:MM:SS (yt-dlp sometimes
        # returns bare seconds like "19").
        "duration_string": _fmt_duration(info.get("duration")) or info.get("duration_string") or "",
        "thumbnail": thumb,
        "webpage_url": info.get("webpage_url") or info.get("original_url"),
        "extractor": info.get("extractor_key") or info.get("extractor"),
        "is_live": bool(info.get("is_live")),
        "view_count": info.get("view_count"),
        "upload_date": info.get("upload_date"),
        "max_height": heights[0] if heights else None,
        "available_heights": heights,
    }


def extract_info(url: str) -> dict:
    """Fetch metadata for ``url`` without downloading. Raises ``EngineError``."""
    last_error: Optional[Exception] = None
    for label, cookie_opts in _STRATEGIES:
        opts = {**_base_opts(), "skip_download": True, **cookie_opts}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            if info is None:
                raise EngineError("Keine Video-Informationen gefunden.")
            # Playlists/channels: take the first entry so the UI has something.
            if info.get("_type") == "playlist" and info.get("entries"):
                entries = [e for e in info["entries"] if e]
                if entries:
                    info = entries[0]
            return _normalize_info(info)
        except Exception as exc:  # noqa: BLE001 — fall through to next strategy
            last_error = exc
    raise EngineError(_friendly_error(last_error))


def download(
    url: str,
    *,
    format_id: str = "best",
    output_dir: Optional[str] = None,
    progress_cb: Optional[Callable[[dict], None]] = None,
) -> dict:
    """Download ``url`` and return ``{filepath, output_dir, title}``.

    ``progress_cb`` receives normalized progress dicts (see ``_make_hook``).
    Raises ``EngineError`` if every strategy fails.
    """
    preset = FORMAT_PRESETS.get(format_id) or FORMAT_PRESETS["best"]
    out_dir = _resolve_output_dir(output_dir)

    # ffmpeg is required to merge HD/4K video+audio and to extract MP3. Fail
    # early with an actionable message instead of deep inside yt-dlp.
    if (preset.get("merge") or preset.get("postprocessors")) and shutil.which("ffmpeg") is None:
        raise EngineError("ffmpeg fehlt — bitte installieren: brew install ffmpeg")

    base = {
        **_base_opts(),
        "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
        "format": preset["selector"],
    }
    if preset.get("merge"):
        base["merge_output_format"] = preset["merge"]
    if preset.get("postprocessors"):
        base["postprocessors"] = preset["postprocessors"]

    last_error: Optional[Exception] = None
    for label, cookie_opts in _STRATEGIES:
        # Fresh capture + hooks per attempt so a partial earlier attempt can't
        # leak a stale filepath/title into a later successful one.
        captured: dict = {"filepath": None, "title": None}
        opts = {
            **base,
            **cookie_opts,
            "progress_hooks": [_make_hook(progress_cb, captured)],
            "postprocessor_hooks": [_make_pp_hook(captured)],
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
            captured["title"] = (info or {}).get("title") or captured["title"]
            if not captured["filepath"] and info:
                # Best-effort final path when hooks didn't capture it.
                req = info.get("requested_downloads") or []
                if req and req[0].get("filepath"):
                    captured["filepath"] = req[0]["filepath"]
            return {
                "filepath": captured["filepath"],
                "output_dir": out_dir,
                "title": captured["title"],
            }
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if progress_cb:
                progress_cb({"status": "retry", "message": f"Versuch {label} fehlgeschlagen."})
    raise EngineError(_friendly_error(last_error))


def _resolve_output_dir(output_dir: Optional[str]) -> str:
    path = os.path.abspath(os.path.expanduser((output_dir or DEFAULT_OUTPUT_DIR).strip()))
    os.makedirs(path, exist_ok=True)
    if not os.path.isdir(path):
        raise EngineError(f"Zielordner ist kein Verzeichnis: {path}")
    return path


def _make_hook(progress_cb, captured) -> Callable[[dict], None]:
    def hook(d: dict) -> None:
        status = d.get("status")
        if status == "finished":
            captured["filepath"] = d.get("filename") or captured["filepath"]
        if not progress_cb:
            return
        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes") or 0
            percent = (downloaded / total * 100) if total else None
            progress_cb(
                {
                    "status": "downloading",
                    "percent": percent,
                    "downloaded": downloaded,
                    "total": total,
                    "speed": d.get("speed"),
                    "eta": d.get("eta"),
                    "filename": os.path.basename(d.get("filename") or ""),
                }
            )
        elif status == "finished":
            progress_cb(
                {
                    "status": "processing",
                    "message": "Download fertig — verarbeite Datei…",
                    "filename": os.path.basename(d.get("filename") or ""),
                }
            )

    return hook


def _make_pp_hook(captured) -> Callable[[dict], None]:
    def pp_hook(d: dict) -> None:
        if d.get("status") == "finished":
            info = d.get("info_dict") or {}
            path = info.get("filepath") or d.get("filename")
            if path:
                captured["filepath"] = path

    return pp_hook


def _friendly_error(exc: Optional[Exception]) -> str:
    text = str(exc) if exc else "Unbekannter Fehler."
    low = text.lower()
    if (
        "sign in to confirm" in low
        or "age-restricted" in low
        or "age restricted" in low
        or "inappropriate for some users" in low
    ):
        return "Video ist altersbeschränkt oder verlangt Anmeldung."
    if "private" in low:
        return "Dieses Video ist privat."
    if "unavailable" in low or "removed" in low:
        return "Video ist nicht verfügbar oder wurde entfernt."
    if "unsupported url" in low or "is not a valid url" in low:
        return "Diese URL wird nicht unterstützt."
    if "ffmpeg" in low:
        return "ffmpeg fehlt — wird für Zusammenführen/Audio benötigt."
    # Trim yt-dlp's noisy prefix for display.
    cleaned = text.replace("ERROR: ", "").strip()
    return cleaned[:300] if cleaned else "Download fehlgeschlagen."
