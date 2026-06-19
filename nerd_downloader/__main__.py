"""Entry point: ``python -m nerd_downloader``.

Picks a free local port, starts the Flask server bound to 127.0.0.1 (never
exposed to the network), and opens the browser at the app.
"""

from __future__ import annotations

import os
import socket
import threading
import webbrowser

from . import __app_name__, __version__
from .app import create_app

_PREFERRED_PORTS = (8765, 8766, 8770, 8780, 0)


def _find_port() -> int:
    for port in _PREFERRED_PORTS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return sock.getsockname()[1]
            except OSError:
                continue
    raise RuntimeError("Kein freier Port gefunden.")


def main() -> None:
    port = _find_port()
    url = f"http://127.0.0.1:{port}"

    print(f"\n  🤓  {__app_name__} v{__version__}")
    print(f"  →  {url}")
    print("  Zum Beenden: Strg+C  (oder dieses Fenster schließen)\n")

    if os.environ.get("NERDDL_NO_BROWSER") != "1":
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    app = create_app()
    # threaded=True so the SSE stream and API calls run concurrently.
    app.run(host="127.0.0.1", port=port, threaded=True, use_reloader=False)


if __name__ == "__main__":
    main()
