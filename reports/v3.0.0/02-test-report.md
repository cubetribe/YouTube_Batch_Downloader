# v3.0.0 — Test Report (E2E, real browser)

Verified the full user story against the running Flask server (`http://127.0.0.1:8765`)
with Playwright, using a tiny always-available public video ("Me at the zoo", 19s).

## Results

| Step | Result |
|------|--------|
| Page loads, brand + version (v3.0.0) render | ✅ |
| `GET /api/meta` returns app/version/formats/default dir | ✅ |
| Type link → **Analysieren** → `POST /api/info` | ✅ title/uploader/thumbnail/duration/max-height |
| Info card renders (thumb, "240p" badge, "jawed", duration) | ✅ |
| 5 quality presets in dropdown | ✅ best / 2160p / 1080p / 720p / audio |
| Folder field defaults to `~/Downloads`, presets shown | ✅ |
| **Download starten** → SSE progress 0→100% | ✅ live percent + speed/ETA |
| Completion → "Fertig ✓", "„Me at the zoo" gespeichert." | ✅ |
| File on disk (`Me at the zoo.mp4`, 475,990 bytes, merged mp4) | ✅ |
| Console errors / warnings | ✅ 0 |
| Responsive: desktop (1280), tablet (768), mobile (390) | ✅ stacks cleanly |

Engine-level download test (separate, to a temp dir) also confirmed the video+audio
merge via ffmpeg and the cookie-fallback path (first strategy = no cookies, succeeded).

## Artifacts (local, gitignored)
`nerddl-01-desktop-empty.png`, `nerddl-02-desktop-info.png`, `nerddl-03-desktop-done.png`,
`nerddl-04-tablet-done.png`, `nerddl-05-mobile-done.png` in repo root.

## Known cosmetic items folded into the fix pass
- Duration badge showed raw seconds ("19") instead of "0:19".
- `yt-dlp` printed its own progress bar to stdout despite `quiet=True` (cosmetic, server log only).
