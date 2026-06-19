<div align="center">

# 🤓 Nerd Downloader

### Paste. Glotz. Lad runter.

*Der YouTube-Downloader für Leute, die keine Lust auf 47 Werbebanner, „Jetzt App installieren!"-Popups und „Premium für nur 9,99 €/Monat" haben.*

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)
[![Läuft auf meinem Mac](https://img.shields.io/badge/läuft%20auf-meinem%20Mac™-success.svg)](#-schnellstart)
[![Made with Claude Code](https://img.shields.io/badge/gebaut%20mit-Claude%20Code-5436DA.svg)](https://claude.ai/code)

**Kopier den Link → klick aufs 📋 → schau dir das Video an → lad's runter.** Das war's. Kein Account, keine Cloud, keine Sorgen.

</div>

---

> **TL;DR (für die Eiligen):** A tiny, cheeky, fully-local YouTube downloader for macOS.
> Double-click, your browser opens, paste a link, hit download. No accounts, no cloud,
> no shady "download" buttons that install three toolbars. Powered by `yt-dlp`.

## 🎬 Was ist das überhaupt?

Nerd Downloader ist eine kleine Web-App, die **komplett lokal auf deinem Mac** läuft.
Du startest sie per Doppelklick, dein Browser geht auf `http://127.0.0.1:8765`, und ab
da ist es kinderleicht:

1. Auf YouTube den Link **kopieren**
2. In Nerd Downloader oben aufs **📋-Icon** klicken (zack, eingefügt)
3. **„Analysieren"** → Titel, Thumbnail, Dauer & Qualität erscheinen
4. Qualität + Ordner wählen → **„Download starten"** → 🍿

Kein „Datei wird vorbereitet (Position 4.812 in der Warteschlange)". Kein Captcha,
bei dem du Ampeln anklicken musst. Einfach. Lokal. Fertig.

## ✨ Features (a.k.a. die Angeberliste)

- 📋 **Paste-First** — das Icon liest deine Zwischenablage. Strg+C, Klick, fertig.
- 🔎 **Erst gucken, dann laden** — Titel, Thumbnail, Kanal, Dauer & max. Auflösung *vor* dem Download.
- 🎬 **HD bis 4K** — beste Qualität, sauber zu MP4 zusammengeführt (Danke, ffmpeg ❤️).
- 🎵 **MP3 mit 320 kbps** — für die Ohren, die's hören.
- 📁 **Echter macOS-Ordnerdialog** — kein „gib den Pfad manuell ein"-Quatsch. Plus „Im Finder zeigen".
- 📊 **Live-Fortschritt** — Prozent, Tempo, ETA. In Echtzeit. Wie's sein soll.
- 🔒 **Bleibt zuhause** — der Server lauscht **nur** auf `127.0.0.1`. Niemand sonst kommt ran.
- 🧩 **Wächst mit** — `yt-dlp` kann 1000+ Seiten. Heute YouTube, morgen … fast alles.

## 🚀 Schnellstart

1. **`Nerd Downloader.command` doppelklicken.**
2. Beim **allerersten Mal** meckert macOS, weil die App nicht von Apple gesegnet wurde:
   → **Rechtsklick → „Öffnen" → „Öffnen"**. Einmal. Danach nie wieder.
3. Der erste Start richtet sich selbst ein (kurz Geduld + Internet). Dann öffnet sich dein Browser.
4. Paste. Glotz. Lad runter. 🎉

> 🍺 **Für Freunde gedacht?** Es gibt eine fertige ZIP unter
> [Releases](../../releases) — entpacken, doppelklicken, läuft. Die `LIESMICH.txt` erklärt alles.

## 🧰 Voraussetzungen (einmalig, versprochen)

Die App ist Python, kein Zauberstab — sie braucht zwei kostenlose Helfer:

| Brauchst du | Wofür | Befehl |
|-------------|-------|--------|
| **Python 3.10+** | die App selbst | `brew install python` |
| **ffmpeg** | HD/4K zusammenfügen & MP3 | `brew install ffmpeg` |

Kein Homebrew? [Hier entlang](https://brew.sh). Und keine Sorge: Der Launcher prüft das
beim Start und **bietet sogar an, ffmpeg selbst zu installieren**. Bequemer geht's kaum.

## 🛠️ Wie funktioniert der Zauber?

```
   Dein Browser  ──(paste/analyze/download)──►  Flask @ 127.0.0.1
        ▲                                              │
        └──────── Live-Fortschritt (SSE) ◄─── yt-dlp ──┴──► ffmpeg (Merge / MP3)
```

Kurz: ein winziger lokaler Server, eine handgeschriebene Vanilla-JS-Oberfläche (kein
500-MB-`node_modules`-Monster), `yt-dlp` als Motor, ffmpeg fürs Feintuning. Downloads
laufen im Hintergrund-Thread, der Fortschritt tickert per Server-Sent-Events zurück.

| Datei | Job |
|-------|-----|
| `nerd_downloader/__main__.py` | Port suchen, Server starten, Browser aufmachen |
| `nerd_downloader/app.py` | die Routen (`/api/info`, `/download`, `/progress`, …) |
| `nerd_downloader/engine.py` | `yt-dlp`-Magie inkl. Cookie-Fallback |
| `nerd_downloader/jobs.py` | Job- & Fortschritts-Verwaltung (SSE) |
| `nerd_downloader/macos.py` | nativer Ordnerdialog & Finder-Reveal |
| `nerd_downloader/static/` | die UI (HTML/CSS/JS, ganz ohne Build-Schritt) |

## 🙋 FAQ (Frequently Asked Nerd-Questions)

**„Warum nicht einfach eine der 9000 Webseiten benutzen?"**
Weil die zu 90 % aus Werbung, Trackern und „Are you a robot?" bestehen. Hier läuft alles
lokal, niemand sieht deine Links, und es gibt keinen einzigen Banner. 🚫🪧

**„Sammelt ihr meine Daten?"**
Womit denn? Es gibt keinen Server außer dem auf deinem eigenen Mac. Wir wüssten nicht
mal, *dass* es dich gibt. 👻

**„Kann ich damit Netflix rippen?"**
Nein. Und frag nicht nochmal. 😇

**„Warum heißt es Nerd Downloader?"**
Weil's von einem Nerd für Nerds ist. Wenn du das hier liest, bist du wahrscheinlich auch
einer. Willkommen. 🤝

## 🤝 Mitmachen

Open Source, Baby. Pull Requests willkommen, Issues willkommen, freche Kommentare
willkommen. Ideen, die schon rumschwirren:

- 📜 Playlist-Download
- 🗂️ Download-Verlauf
- 💬 Untertitel
- 🌍 noch mehr Quellen (yt-dlp kann ja eh schon so viel)

Schnapp dir [CONTRIBUTING.md](CONTRIBUTING.md) und leg los. Sei nett, schreib Tests,
und mach das `dart analyze`… ähm, `ruff` glücklich.

## ⚖️ Der ernste Teil (kurz, versprochen)

Nerd Downloader ist ein Werkzeug. Wie ein Schraubenzieher — man kann damit Regale bauen
oder Unsinn anstellen. **Lade nur runter, wozu du die Rechte hast.** Wir sind Nerds,
keine Piraten. 🏴‍☠️➡️🚮 Respektiere Urheberrechte und die Nutzungsbedingungen der Plattformen.

## 📟 Bonus: die alte Terminal-CLI

Die ursprünglichen Skripte leben weiter, für die Hardcore-Terminal-Fraktion:

```bash
python3 start.py
```

(Batch-Download, Audio/Video-Menü, das volle Retro-Programm. Siehe `download_*.py`.)

## 📄 Lizenz

[MIT](LICENSE) — nimm's, bau drauf auf, hab Spaß.

<div align="center">

---

*Gebaut mit [Claude Code](https://claude.ai/code) · angetrieben von [yt-dlp](https://github.com/yt-dlp/yt-dlp) · läuft lokal, bleibt lokal* 🤓

</div>
