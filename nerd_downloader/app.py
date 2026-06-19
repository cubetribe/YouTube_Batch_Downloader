"""Flask app for Nerd Downloader.

Routes (all JSON except the SSE stream and the static index):
  GET  /                     -> the single-page UI
  GET  /api/meta             -> app name, version, default folder, format presets
  POST /api/info             -> {url} -> normalized video metadata
  POST /api/download         -> {url, format, output_dir} -> {job_id}
  GET  /api/progress/<id>    -> Server-Sent Events stream of progress
  POST /api/choose-folder    -> native macOS folder picker -> {path}
  POST /api/reveal           -> reveal a path in Finder
"""

from __future__ import annotations

import json
import os
import threading
from urllib.parse import urlparse

from flask import Flask, Response, jsonify, request, send_from_directory

from . import __app_name__, __version__, engine, macos
from .jobs import manager

_STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


def create_app() -> Flask:
    app = Flask(__name__, static_folder=_STATIC_DIR, static_url_path="/static")

    @app.get("/")
    def index() -> Response:
        return send_from_directory(_STATIC_DIR, "index.html")

    @app.get("/api/meta")
    def meta():
        return jsonify(
            {
                "app": __app_name__,
                "version": __version__,
                "default_dir": engine.DEFAULT_OUTPUT_DIR,
                "home": os.path.expanduser("~"),
                "is_mac": macos.IS_MAC,
                "formats": engine.format_presets_for_ui(),
            }
        )

    @app.post("/api/info")
    def info():
        url = (request.get_json(silent=True) or {}).get("url", "")
        ok, error = _validate_url(url)
        if not ok:
            return jsonify({"error": error}), 400
        try:
            return jsonify(engine.extract_info(url.strip()))
        except engine.EngineError as exc:
            return jsonify({"error": exc.user_message}), 502

    @app.post("/api/download")
    def download():
        payload = request.get_json(silent=True) or {}
        url = payload.get("url", "")
        ok, error = _validate_url(url)
        if not ok:
            return jsonify({"error": error}), 400
        fmt = payload.get("format", "best")
        output_dir = payload.get("output_dir") or engine.DEFAULT_OUTPUT_DIR

        job = manager.create()
        thread = threading.Thread(
            target=_run_download,
            args=(job.id, url.strip(), fmt, output_dir),
            daemon=True,
        )
        thread.start()
        return jsonify({"job_id": job.id})

    @app.get("/api/progress/<job_id>")
    def progress(job_id: str):
        if manager.get(job_id) is None:
            return jsonify({"error": "Unbekannter Job."}), 404

        def generate():
            for event in manager.stream(job_id):
                yield f"data: {json.dumps(event)}\n\n"

        return Response(
            generate(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )

    @app.post("/api/choose-folder")
    def choose_folder():
        if not macos.IS_MAC:
            return jsonify({"error": "Native Ordnerauswahl nur auf macOS."}), 400
        default = (request.get_json(silent=True) or {}).get("current") or engine.DEFAULT_OUTPUT_DIR
        path = macos.choose_folder(default=default)
        return jsonify({"path": path, "cancelled": path is None})

    @app.post("/api/reveal")
    def reveal():
        path = (request.get_json(silent=True) or {}).get("path", "")
        return jsonify({"ok": macos.reveal_in_finder(path)})

    return app


def _run_download(job_id: str, url: str, fmt: str, output_dir: str) -> None:
    def cb(event: dict) -> None:
        manager.publish(job_id, {"type": "progress", **event})

    try:
        result = engine.download(url, format_id=fmt, output_dir=output_dir, progress_cb=cb)
        manager.finish(
            job_id,
            {
                "type": "done",
                "filepath": result.get("filepath"),
                "output_dir": result.get("output_dir"),
                "title": result.get("title"),
            },
        )
    except engine.EngineError as exc:
        manager.finish(job_id, {"type": "error", "message": exc.user_message})
    except Exception:  # noqa: BLE001 — never leave the stream hanging
        manager.finish(job_id, {"type": "error", "message": "Unerwarteter Fehler beim Download."})


def _validate_url(url: str) -> tuple[bool, str]:
    if not url or not url.strip():
        return False, "Bitte einen Link einfügen."
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False, "Bitte einen gültigen http(s)-Link einfügen."
    return True, ""
