# Project Crucible — Fire Risk Analysis & iTAK Export

Fetches Arizona fire incident data from the NERIS API, generates ISO 31010 risk reports per incident, and outputs a KML file for visualization in iTAK on iPad.

## Overview

```
NERIS API (or simulated data) → ISO 31010 Risk Analysis → KML → iTAK
```

Each fire incident marker on the map includes a detailed risk report covering:
- **Bow Tie Analysis** — preventative and reactive control effectiveness
- **FMEA** — failure modes ranked by Risk Priority Number
- **Decision Tree** — investment recommendation (simulated financials)
- **Markov Classification** — LOW / MODERATE / HIGH risk state

## Quick Start

```bash
cd 000_coderepo/riskrunners/project-crucible

# Install dependencies
pip install -r requirements.txt

# Run with simulated data (no API credentials needed)
python src/main.py
```

The script generates `output/az_fire_incidents.kml`.

## Using Real NERIS Data

Set environment variables before running:

```bash
export NERIS_CLIENT_ID="your_client_id"
export NERIS_CLIENT_SECRET="your_client_secret"
python src/main.py
```

The script will authenticate via OAuth2 and fetch live Arizona fire incidents.

## Loading KML in iTAK

1. Transfer `output/az_fire_incidents.kml` to your iPad (AirDrop, Files, etc.)
2. Open iTAK
3. Go to **Data Packages** → **Import**
4. Select the `.kml` file
5. Tap any fire marker to expand the full risk report

## Project Structure

```
src/
├── config.py          — Configuration and environment variables
├── neris_client.py    — NERIS API client (OAuth2 + incident fetching)
├── simulated_data.py  — Realistic simulated AZ fire data
├── risk_analysis.py   — ISO 31010 risk analysis (Bow Tie, FMEA, Decision Tree, Markov)
├── tak_export.py      — KML generation for iTAK
└── main.py            — Orchestrator script
```

## Dependencies

- Python 3.10+
- `requests` (for NERIS API calls)
- Standard library `xml.etree.ElementTree` (for KML generation)

## Context

Part of the Project Crucible pipeline:
```
IoT Sensors → NERIS API → Risk Analysis → Risk Reports → Insurers
```

Built for the Arizona Captive Insurance Association and Crucible Coalition.

---

*Project Crucible | Richards+ | Linked Trust | AI Trailblazers*
