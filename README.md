# Home Assistant Integration - Hydrop

Home Assistant integration for connecting Hydrop water meters via the Hydrop Cloud API.

[![Static Badge](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://github.com/hacs/integration)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/simatec/ha-hydrop/total?style=for-the-badge)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/simatec/ha-hydrop?style=for-the-badge)

![GitHub Release Date](https://img.shields.io/github/release-date-pre/simatec/ha-hydrop?style=for-the-badge&label=Latest%20Beta%20Release) [![GitHub Release](https://img.shields.io/github/v/release/simatec/ha-hydrop?include_prereleases&style=for-the-badge)](https://github.com/simatec/ha-hydrop/releases)

![GitHub Release Date](https://img.shields.io/github/release-date/simatec/ha-hydrop?style=for-the-badge&label=Latest%20Release) [![GitHub Release](https://img.shields.io/github/v/release/simatec/ha-hydrop?style=for-the-badge)](https://github.com/simatec/ha-hydrop/releases)

---

## Description

This integration connects Hydrop water meters to Home Assistant via the official Hydrop Cloud API. Water consumption is displayed as a sensor with the unit `m³` and supports Home Assistant's energy management.

### Features

- 📊 Read the current water meter reading in m³
- 🔄 Automatic updates every 5 minutes
- 💧 Full integration into the Home Assistant energy dashboard
- 🌐 Connection via the Hydrop Cloud API with API key authentication
- 🌍 Support for German and English


---

## Installation

### HACS (recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=simatec&repository=ha-hydrop&category=Integration)

1. Open HACS in Home Assistant
2. Click **Custom Repositories**
3. Enter `https://github.com/simatec/ha-hydrop` as the repository, Category: **Integration**
4. Search for and install the **Hydrop** integration
5. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/hydrop` folder from this repository
2. Copy it to the `custom_components` directory in your Home Assistant configuration
3. Restart Home Assistant

---

## Configuration

After installation, set up the integration via the user interface:

1. **Settings** → **Devices & Services** → **Add Integration**
2. Search for **Hydrop**
3. Enter the following data:

| Field | Description |
|------|-------------|
| **Display Name** | The name of the sensor in Home Assistant (e.g., “Water Meter”) |
| **Device Name** | The device name from the Hydrop Portal |
| **API Key** | The API key from the Hydrop Portal |

The credentials are automatically validated against the Hydrop API during setup.

---

## Sensor Attributes

The sensor provides the following data:

| Attribute | Description |
|----------|-------------|
| `state` | Current meter reading in m³ |
| `timestamp` | Timestamp of the last measurement |
| `meterValue` | Meter reading from the last measurement |

---

## API

This integration uses the official Hydrop API:

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
