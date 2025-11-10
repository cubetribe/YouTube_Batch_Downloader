# YouTube PO Token Anleitung

## Was ist ein PO Token?

Ein **PO Token (Proof of Origin Token)** ist ein Authentifizierungstoken, das YouTube seit 2024 für bestimmte Downloads erfordert. Ohne diesen Token können viele Videos nur in niedriger Qualität oder gar nicht heruntergeladen werden.

## Warum brauche ich einen PO Token?

YouTube hat diese Sicherheitsmaßnahme eingeführt, um automatisierte Downloads zu erschweren. Mit einem PO Token umgehst du folgende Probleme:

- ❌ **HTTP Error 403** - Zugriff verweigert
- ❌ **Niedrige Qualität** - Nur 360p oder weniger verfügbar
- ❌ **Android Client Fehler** - "android client https formats require a GVS PO Token"

## Methode 1: Browser Developer Tools (Empfohlen)

### Chrome / Edge / Brave

1. **YouTube öffnen und anmelden**
   - Gehe zu https://www.youtube.com
   - Melde dich mit deinem Google-Account an

2. **Developer Tools öffnen**
   - Windows/Linux: `F12` oder `Strg + Shift + I`
   - Mac: `Cmd + Option + I`

3. **Network Tab aktivieren**
   - Klicke auf den "Network" Tab
   - Aktiviere "Preserve log" (Checkbox)

4. **YouTube Video laden**
   - Öffne ein beliebiges YouTube Video
   - Warte bis es vollständig geladen ist

5. **Nach PO Token suchen**
   - Im Network Tab: Filtere nach "player" oder "watch"
   - Klicke auf einen der Requests
   - Gehe zum "Response" oder "Headers" Tab
   - Suche mit `Cmd+F` (Mac) oder `Strg+F` (Windows) nach:
     - `po_token`
     - `poToken`
     - `gvs+`

6. **Token kopieren**
   - Der Token sieht so aus: `MnQ3ajdvc0JIQVBUc0t3YjQ4RGd...` (sehr lang)
   - Kopiere NUR den Token-String (ohne Anführungszeichen)

### Firefox

1. Gleiche Schritte wie oben, aber:
   - Developer Tools: `F12` oder `Strg + Shift + I` (Windows/Linux)
   - Der Network Tab heißt "Netzwerkanalyse"

## Methode 2: Browser Extension

### "EditThisCookie" Extension

1. **Extension installieren**
   - Chrome: Chrome Web Store → "EditThisCookie"
   - Firefox: Add-ons → "Cookie-Editor"

2. **YouTube öffnen und anmelden**

3. **Cookies anzeigen**
   - Klicke auf das Extension-Icon
   - Suche nach Cookies mit Namen wie:
     - `VISITOR_INFO1_LIVE`
     - `VISITOR_PRIVACY_METADATA`

4. **Storage Inspector nutzen**
   - Öffne Developer Tools → Storage/Application
   - Local Storage → youtube.com
   - Suche nach `yt-player-headers-readable`

## Methode 3: Mobile App (Android)

### Mit ADB (Android Debug Bridge)

1. **USB-Debugging aktivieren**
   - Einstellungen → Entwickleroptionen → USB-Debugging

2. **ADB installieren**
   ```bash
   # Mac
   brew install android-platform-tools

   # Windows
   # Download von https://developer.android.com/studio/releases/platform-tools
   ```

3. **YouTube App Traffic mitschneiden**
   ```bash
   adb shell
   # Installiere einen Proxy wie mitmproxy
   # Analysiere den Traffic nach po_token
   ```

## Token im Downloader verwenden

### Automatische Konfiguration

```bash
# Token Setup starten
python src/downloader_enhanced.py --setup-token

# Token eingeben wenn gefragt
```

### Manuelle Konfiguration

1. **Config-Datei erstellen**
   ```bash
   # Mac/Linux
   nano ~/.yt_downloader_config.json
   ```

2. **Token einfügen**
   ```json
   {
     "po_token": "DEIN_TOKEN_HIER"
   }
   ```

3. **Datei speichern**
   - Nano: `Ctrl+X`, dann `Y`, dann `Enter`

## Troubleshooting

### Token funktioniert nicht?

1. **Token läuft ab**
   - PO Tokens sind nur temporär gültig (meist 1-2 Stunden)
   - Generiere regelmäßig einen neuen Token

2. **Falsches Format**
   - Entferne Präfixe wie `android.gvs+` oder `gvs+`
   - Verwende nur den reinen Token-String

3. **Account-spezifisch**
   - Token sind an deinen Google-Account gebunden
   - Verwende den Token nur mit dem Account, mit dem du ihn generiert hast

### Alternative Lösungen

Wenn der PO Token nicht funktioniert, versucht der Enhanced Downloader automatisch:

1. **Verschiedene Player Clients**
   - Android Client
   - Web Client
   - iOS Client

2. **Browser Cookies**
   - Chrome Cookies werden automatisch versucht

3. **Niedrige Qualität**
   - Als letzter Fallback: 360p oder weniger

## Sicherheitshinweise

⚠️ **WICHTIG:**
- Teile deinen PO Token **NIEMALS** öffentlich
- Der Token ist wie ein temporäres Passwort
- Generiere regelmäßig neue Tokens
- Lösche alte Tokens aus Config-Dateien

## Weiterführende Informationen

- [yt-dlp PO Token Wiki](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide)
- [YouTube API Changes](https://github.com/yt-dlp/yt-dlp/issues/10128)
- [Token Generation Scripts](https://github.com/yt-dlp/yt-dlp/tree/master/devscripts)

## Support

Bei Problemen:
1. Stelle sicher, dass du die neueste Version verwendest
2. Generiere einen frischen Token
3. Überprüfe die Fehlermeldungen im verbose Modus
4. Erstelle ein Issue auf GitHub mit anonymisierten Logs