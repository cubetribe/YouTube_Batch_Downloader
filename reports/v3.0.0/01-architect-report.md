# v3.0.0 — Nerd Downloader (Architecture Brief)

**Type:** Feature / Rebrand — turn the existing CLI YouTube downloader into a local
web app called **Nerd Downloader**.

## User story (acceptance)
Auf YouTube Link kopieren → im Browser auf das **Einfügen-Icon oben** klicken →
Link wird eingefügt & analysiert → Video-Infos erscheinen (Titel, Thumbnail,
Dauer, Qualität) → Zielordner wählen → **Download**. Läuft lokal auf dem Mac.

## Decisions
- **Form factor:** Local web app (chosen by user). Double-click launcher starts a
  local server; UI opens in the browser at `http://127.0.0.1:8765`.
- **Backend:** Flask (pure-Python — no Rust/build toolchain, safe on the repo's
  Python 3.14 venv). Bound to `127.0.0.1` only — never network-exposed.
- **Engine:** Thin wrapper around `yt-dlp` reusing the existing project's hard-won
  resilience: try **without** browser cookies first, then retry **with** Chrome
  cookies. HD/4K via `bestvideo+bestaudio` merged to mp4 (ffmpeg); MP3 via
  `FFmpegExtractAudio`.
- **Live progress:** download runs in a daemon thread; `yt-dlp` progress hooks push
  events onto a per-job queue; the browser consumes them over Server-Sent Events.
- **Frontend:** vanilla JS + CSS, no build step (robust, "runs forever").
- **macOS niceties:** native folder picker + "Reveal in Finder" via `osascript`
  (possible because the server is local).

## Extensibility
`yt-dlp` already supports 1000+ sites, so "perspektivisch auch andere Dinge"
(other sources) works without engine changes. New quality presets are one entry in
`FORMAT_PRESETS`.

## Module map
```
nerd_downloader/
  __init__.py     app name + version
  __main__.py     port pick + browser open + run server
  app.py          Flask routes (/, /api/meta|info|download|progress|choose-folder|reveal)
  engine.py       yt-dlp: extract_info() + download() with cookie fallback
  jobs.py         JobManager: per-job event queues + SSE bridge + TTL reaping
  macos.py        osascript folder picker + Finder reveal (degrades off-Mac)
  static/         index.html, app.js, styles.css
Nerd Downloader.command   double-click launcher (venv + deps + run)
```

## Out of scope (v3.0.0)
Batch/playlist queue UI, download history, subtitle download, auth, packaging as a
signed `.app`. The legacy CLI scripts remain untouched.
