# Home Assistant Integration - Hydrop

Home Assistant Integration zur Einbindung von Hydrop Wasserzählern über die Hydrop Cloud API.

[![Static Badge](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://github.com/hacs/integration)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/simatec/ha-hydrop/total?style=for-the-badge)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/simatec/ha-hydrop?style=for-the-badge)

![GitHub Release Date](https://img.shields.io/github/release-date-pre/simatec/ha-hydrop?style=for-the-badge&label=Latest%20Beta%20Release) [![GitHub Release](https://img.shields.io/github/v/release/simatec/ha-hydrop?include_prereleases&style=for-the-badge)](https://github.com/simatec/ha-hydrop/releases)

![GitHub Release Date](https://img.shields.io/github/release-date/simatec/ha-hydrop?style=for-the-badge&label=Latest%20Release) [![GitHub Release](https://img.shields.io/github/v/release/simatec/ha-hydrop?style=for-the-badge)](https://github.com/simatec/ha-hydrop/releases)

---

## Beschreibung

Diese Integration bindet Hydrop-Wasserzähler über die offizielle Hydrop Cloud API in Home Assistant ein. Der Wasserverbrauch wird als Sensor mit der Einheit `m³` dargestellt und unterstützt die Home Assistant Energie-Verwaltung.

### Funktionen

- 📊 Auslesen des aktuellen Wasserzähler-Stands in m³
- 🔄 Automatische Aktualisierung alle 5 Minuten
- 💧 Vollständige Integration in das Home Assistant Energie-Dashboard
- 🌐 Anbindung über die Hydrop Cloud API mit API-Key Authentifizierung
- 🌍 Unterstützung für Deutsch und Englisch

---

## Installation

### HACS (empfohlen)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=simatec&repository=ha-hydrop&category=Integration)

1. HACS in Home Assistant öffnen
2. Auf **Benutzerdefinierte Repositories** klicken
3. `https://github.com/simatec/ha-hydrop` als Repository eintragen, Kategorie: **Integration**
4. Integration **Hydrop** suchen und installieren
5. Home Assistant neu starten

### Manuelle Installation

1. Den Ordner `custom_components/hydrop` aus diesem Repository herunterladen
2. In das Verzeichnis `custom_components` der Home Assistant Konfiguration kopieren
3. Home Assistant neu starten

---

## Konfiguration

Nach der Installation die Integration über die Benutzeroberfläche einrichten:

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. Nach **Hydrop** suchen
3. Folgende Daten eingeben:

| Feld | Beschreibung |
|------|-------------|
| **Anzeigename** | Der Name des Sensors in Home Assistant (z.B. "Wasserzähler") |
| **Gerätename** | Der Gerätename aus dem Hydrop Portal |
| **API-Key** | Der API-Key aus dem Hydrop Portal |

Die Zugangsdaten werden beim Einrichten automatisch gegen die Hydrop API validiert.

---

## Sensor-Attribute

Der erzeugte Sensor stellt folgende Daten bereit:

| Attribut | Beschreibung |
|----------|-------------|
| `state` | Aktueller Zählerstand in m³ |
| `timestamp` | Zeitstempel der letzten Messung |
| `meterValue` | Zählerstand der letzten Messung |

---

## API

Diese Integration nutzt die offizielle Hydrop API:

```
GET https://api.hydrop-systems.com/sensors/ID/{device_name}/newest
Header: apikey: {api_key}
```

---

## Lizenz

The MIT License (MIT)

Copyright (c) 2026 simatec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
