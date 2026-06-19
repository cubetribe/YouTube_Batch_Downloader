"""Small macOS integrations driven from the local backend.

Because the server runs on the same Mac as the browser, we can offer a real
native folder picker and "Reveal in Finder" — niceties a normal web app can't.
All of these degrade gracefully on non-macOS systems.
"""

from __future__ import annotations

import os
import subprocess
import sys
from typing import Optional

IS_MAC = sys.platform == "darwin"


def choose_folder(prompt: str = "Zielordner wählen", default: Optional[str] = None) -> Optional[str]:
    """Open a native folder chooser. Returns the POSIX path, or None if cancelled.

    The AppleScript contains no user-supplied data, so there is no injection
    surface here.
    """
    if not IS_MAC:
        return None
    default = default or os.path.expanduser("~/Downloads")
    script = (
        'set defaultFolder to POSIX file "{default}"\n'
        'try\n'
        '  set chosen to choose folder with prompt "{prompt}" default location defaultFolder\n'
        '  return POSIX path of chosen\n'
        'on error number -128\n'  # user cancelled
        '  return ""\n'
        'end try'
    ).format(default=_escape(default), prompt=_escape(prompt))
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=300,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    path = result.stdout.strip()
    return path or None


def reveal_in_finder(path: str) -> bool:
    """Reveal a file (or open a folder) in Finder. Returns True on success.

    The target must resolve to a location inside the user's home directory or a
    mounted volume under ``/Volumes``; anything else is refused. This guard both
    hardens the feature and keeps untrusted input from reaching ``open``.
    """
    if not IS_MAC or not path:
        return False
    target = os.path.realpath(os.path.expanduser(path))
    home = os.path.realpath(os.path.expanduser("~"))
    if not (
        target == home
        or target.startswith(home + os.sep)
        or target.startswith("/Volumes/")
    ):
        return False
    if not os.path.exists(target):
        return False
    args = ["open", "-R", target] if os.path.isfile(target) else ["open", target]
    try:
        subprocess.run(args, check=False, timeout=10)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _escape(value: str) -> str:
    """Escape a string for safe embedding inside an AppleScript double-quoted literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')
