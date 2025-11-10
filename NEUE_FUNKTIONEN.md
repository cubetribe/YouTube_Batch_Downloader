# 🎉 Neue Funktionen - YouTube HD/4K Downloader v2.0

## 🚀 Start des Programms

Doppelklicke auf:
```
YouTube HD Downloader.command
```

## 📋 Hauptmenü - Alle Optionen

### 📹 EINZELNE DOWNLOADS:
1. **Video herunterladen (HD/4K)**
   - Lädt einzelnes Video in bester Qualität
   - Minimum 1080p, bevorzugt 4K
   - Nutzt automatisch Chrome-Cookies

2. **Audio herunterladen (MP3 320kbps)**
   - Extrahiert Audio in höchster Qualität
   - 320kbps MP3 Format

### 📦 BATCH DOWNLOADS:
3. **Batch Download - Videos (HD/4K)**
   - Mehrere Videos auf einmal
   - Alle in HD/4K Qualität
   - Unterstützt:
     - Direkte URL-Eingabe
     - Mehrfaches Copy-Paste
     - Datei-Import (`file` eingeben)
   - Befehle:
     - `start` / `fertig` - Download starten
     - `clear` - URLs löschen
     - `show` - URLs anzeigen

4. **Batch Download - Audios (MP3)**
   - Mehrere Audios auf einmal
   - Alle in 320kbps MP3

### 🔧 ERWEITERTE OPTIONEN:
5. **Ultimate HD Downloader**
   - Multi-Strategie-Ansatz
   - 6 verschiedene Download-Methoden
   - Für schwierige Videos
   - Probiert automatisch alle Möglichkeiten

6. **HD-Only Download**
   - Strikte Qualitätskontrolle
   - LEHNT Videos unter 1080p AB
   - Zeigt verfügbare Qualitäten
   - Gut für Qualitäts-Überprüfung

7. **PO Token Setup**
   - Für noch bessere Qualität
   - Hilft bei geschützten Videos
   - Einfache Schritt-für-Schritt-Anleitung

## 🎯 Batch-Download Funktionen

### URL-Eingabe Methoden:

1. **Einzeln eingeben:**
   ```
   >>> https://youtube.com/watch?v=xxx
   >>> https://youtube.com/watch?v=yyy
   ```

2. **Mehrere auf einmal (Copy-Paste):**
   ```
   >>> https://youtube.com/watch?v=xxx
   https://youtube.com/watch?v=yyy
   https://youtube.com/watch?v=zzz
   ```

3. **Aus Datei laden:**
   ```
   >>> file
   Pfad zur Textdatei: /path/to/urls.txt
   ```

4. **Gemischter Text (filtert URLs automatisch):**
   ```
   >>> Hier sind meine Videos:
   https://youtube.com/watch?v=xxx und
   noch eins https://youtube.com/watch?v=yyy
   ```

### Batch-Befehle:
- `start` / `fertig` - Download starten
- `clear` - Alle URLs löschen
- `show` - Bisherige URLs anzeigen
- `file` - URLs aus Datei laden

## ✨ Qualitäts-Features

### Automatische HD-Qualität:
- ✅ **Minimum**: 1080p (Full HD)
- ✅ **Bevorzugt**: 4K (2160p)
- ✅ **Unterstützt**: 8K wenn verfügbar
- ❌ **Abgelehnt**: 720p und niedriger

### Chrome-Cookie Integration:
- Automatische Nutzung
- Kein manueller Export nötig
- Bessere Qualität garantiert
- Voraussetzung: In Chrome bei YouTube angemeldet

## 🛠️ Direkte Python-Nutzung

### Für Power-User:

```bash
# Ultimate Downloader (beste Erfolgsrate)
python download_ultimate.py https://youtube.com/watch?v=xxx

# HD-Only (lehnt niedrige Qualität ab)
python download_hd.py https://youtube.com/watch?v=xxx

# Batch mit Ultimate
python download_ultimate.py --batch url1 url2 url3

# PO Token Setup
python download_ultimate.py --setup-token
```

## 📁 Download-Speicherort

Alle Downloads landen in:
```
~/Downloads/
```

Format der Dateinamen:
- Videos: `Videotitel.mp4`
- Mit Qualität: `Videotitel [1080p].mp4`
- Audio: `Videotitel.mp3`

## 🔍 URL-Erkennung

Das Programm erkennt automatisch:
- Standard YouTube URLs: `https://www.youtube.com/watch?v=xxx`
- Kurz-URLs: `https://youtu.be/xxx`
- Embedded URLs: `https://www.youtube.com/embed/xxx`
- URLs mit Zeitstempel und Parametern

## 💡 Tipps

1. **Für beste Qualität:**
   - Immer in Chrome bei YouTube angemeldet sein
   - Ultimate Downloader für schwierige Videos nutzen

2. **Für Batch-Downloads:**
   - URLs vorher in Textdatei sammeln
   - `file` Befehl nutzen für große Listen

3. **Bei Problemen:**
   - Option 5 (Ultimate) probieren
   - yt-dlp updaten (passiert automatisch beim Start)
   - PO Token generieren (Option 7)

## 🚨 Fehlerbehebung

### "Nur 360p verfügbar"
→ Verwende Option 5 (Ultimate Downloader)

### "HTTP Error 403"
→ Option 7 für PO Token Setup

### "Video unavailable"
→ Video gelöscht oder privat

### "Format not available"
→ Ultimate Downloader probieren

## 📊 Unterstützte Qualitäten

- 8K (4320p) ✅
- 4K (2160p) ✅
- 1440p ✅
- 1080p ✅
- 720p ❌ (wird abgelehnt)
- 480p ❌ (wird abgelehnt)
- 360p ❌ (wird abgelehnt)

---

**Version 2.0** - HD/4K Update
**Minimum Qualität**: 1080p
**Automatisch**: Chrome-Cookies, beste Qualität