# YouTube HD/4K Download Guide

## 🚀 Quick Start

### Für einzelne Videos in HD/4K:
```bash
./YouTube\ Downloader.command
# Wähle Option 1 (Video) oder 3 (Batch Video)
```

### Für garantierte HD-Qualität (min. 1080p):
```bash
python download_ultimate.py https://youtube.com/watch?v=xxxxx
```

## 📊 Qualitäts-Garantie

Die aktualisierten Downloader laden **NUR** Videos in HD-Qualität herunter:
- **Minimum**: 1080p (Full HD)
- **Bevorzugt**: 4K (2160p)
- **Abgelehnt**: Alles unter 1080p

## 🔧 Verfügbare Downloader

### 1. **Standard Downloader** (`src/downloader.py`)
- Nutzt automatisch Chrome Cookies
- Versucht beste verfügbare Qualität
- Funktioniert für die meisten Videos

### 2. **Ultimate HD Downloader** (`download_ultimate.py`)
- Multi-Strategie-Ansatz
- 6 verschiedene Download-Methoden
- Garantiert HD oder Fehlermeldung

### 3. **HD-Only Downloader** (`download_hd.py`)
- Lehnt Videos unter 1080p ab
- Zeigt verfügbare Qualitäten an
- Strikte Qualitätskontrolle

## 🍪 Chrome Cookies nutzen

Die Downloader nutzen **automatisch** deine Chrome Cookies für bessere Qualität!

**Voraussetzungen:**
1. Chrome muss installiert sein
2. Du musst in Chrome bei YouTube angemeldet sein
3. Chrome sollte geschlossen sein während des Downloads

## 🔑 PO Token (Optional)

Falls Chrome Cookies nicht ausreichen:

### Token Setup:
```bash
python download_ultimate.py --setup-token
```

### Token generieren:
1. Öffne YouTube in Chrome
2. Öffne Developer Tools (F12)
3. Network Tab → Reload → Suche "player" Request
4. Finde `po_token` im Response
5. Kopiere Token (ohne Präfix)

Details: Siehe `PO_TOKEN_ANLEITUNG.md`

## 📦 Batch Downloads in HD

### Mit dem Hauptprogramm:
```bash
./YouTube\ Downloader.command
# Wähle Option 3 (Batch Video)
# Füge URLs ein
# Tippe 'start' oder 'fertig'
```

### Direkt mit Python:
```bash
python download_ultimate.py --batch url1 url2 url3
```

## ⚠️ Troubleshooting

### Problem: "Nur 360p verfügbar"
**Lösungen:**
1. Stelle sicher, dass du in Chrome bei YouTube angemeldet bist
2. Aktualisiere yt-dlp: `pip install --upgrade yt-dlp`
3. Verwende `download_ultimate.py` - probiert mehrere Strategien

### Problem: "HTTP Error 403"
**Lösungen:**
1. Chrome Cookies werden automatisch genutzt
2. Falls nicht ausreichend: PO Token generieren (siehe oben)
3. VPN verwenden (manche Videos sind region-locked)

### Problem: "Video unavailable"
**Ursachen:**
- Video wurde gelöscht
- Video ist privat
- Video ist in deiner Region nicht verfügbar

## 🎯 Best Practices

1. **Immer in Chrome angemeldet sein**
   - Verbessert Zugang zu HD-Qualität erheblich

2. **Ultimate Downloader für wichtige Videos**
   - Probiert alle möglichen Methoden
   - Höchste Erfolgsrate

3. **Batch Downloads über Nacht**
   - Rate limiting vermeidet Blockierung
   - Große 4K Videos brauchen Zeit

4. **yt-dlp aktuell halten**
   ```bash
   source venv/bin/activate
   pip install --upgrade yt-dlp
   ```

## 📈 Performance

### Erwartete Download-Geschwindigkeiten:
- **1080p**: 5-50 MB/s (50-500 MB Dateigröße)
- **4K**: 10-100 MB/s (500 MB - 2 GB Dateigröße)

### Rate Limiting:
- 2-5 Sekunden Pause zwischen Downloads
- Vermeidet YouTube-Blockierung
- Erhöht Erfolgsrate

## 🆘 Support

Bei Problemen:
1. Überprüfe diese Anleitung
2. Stelle sicher, dass Chrome läuft und du angemeldet bist
3. Verwende `download_ultimate.py` für schwierige Videos
4. Aktualisiere yt-dlp regelmäßig

## 💡 Pro-Tipps

1. **Qualität prüfen vor Batch-Download:**
   ```bash
   python download_hd.py --min-quality 1440 URL
   ```

2. **Spezieller Output-Ordner:**
   ```bash
   python download_ultimate.py --output ~/Desktop/4K-Videos URL
   ```

3. **Nur Audio in bester Qualität:**
   ```bash
   ./YouTube\ Downloader.command
   # Option 2 oder 4 (Audio/Batch Audio)
   # 320kbps MP3 automatisch
   ```

---

**Version**: 2.0 (HD/4K Update)
**Datum**: November 2025
**Minimum Qualität**: 1080p
**Bevorzugte Qualität**: 4K