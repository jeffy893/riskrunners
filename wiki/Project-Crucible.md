# Project Crucible

[← Home](Home.md)

---

## Overview

Project Crucible is a fire risk analysis pipeline that transforms NERIS (National Emergency Response Information System) incident data into actionable risk reports visualized in TAK (Team Awareness Kit). The project demonstrates how agent-based models, ISO 31010 risk methodology, and geospatial situational awareness converge to make previously uninsurable fire-risk properties insurable.

**Core thesis:** If the math doesn't fit the problem, fit the problem to the math.

---

## The Pipeline

```
IoT / Fire Departments → NERIS API → ISO 31010 Analysis → TAK/iTAK → Decision Makers
```

| Stage | Implementation |
|-------|---------------|
| Data Source | NERIS API (https://api.neris.fsri.org/v1) — fire incidents with geolocation |
| Filter | Arizona (state=AZ), fire incident types |
| Analysis | Bow Tie, FMEA, Decision Tree, Markov classification |
| Output | CoT Data Package (.zip) for iTAK on iPad |
| Visualization | Fire markers with expandable risk reports in remarks |

---

## Agent-Based Model Context

Project Crucible is grounded in the principle that categorizing phenomena into modelable patterns enables inference about conflict resolution and resource allocation.

### Sugarscape — Urban Distribution
Agents competing for scarce resources naturally distribute into concentric patterns mirroring real urban geography. Risk density follows the same pattern — properties in high-competition zones face different risk profiles than those at the periphery.

### Recycling — Incentivizing Remediation
Models how incentive structures drive participation in environmental cleanup (riparian wash remediation). The parallel: if a captive insurance model shares underwriting profit with those who reduce fuel loads, prevention becomes self-sustaining.

### Segregation — Coverage Withdrawal
Schelling's model shows how mild preferences produce dramatic boundary effects. Applied to fire insurance: carrier withdrawal from one zone cascades until entire regions become "uninsurable." The captive model breaks this cycle.

---

## ISO 31010 Risk Analysis

Each fire incident receives four analyses:

| Technique | ISO Section | Application |
|-----------|:-----------:|-------------|
| Bow Tie Analysis | B.4.2 | Preventative & reactive control effectiveness |
| FMEA | B.4.3 | Failure modes ranked by Risk Priority Number |
| Decision Tree | B.9.3 | Investment recommendation (simulated financials) |
| Markov Analysis | B.5.9 | LOW / MODERATE / HIGH risk state classification |

---

## Repository Structure

```
project-crucible/
├── src/
│   ├── config.py              # Configuration, env vars, simulated data fallback
│   ├── neris_client.py        # NERIS API client (OAuth2 + paginated fetch)
│   ├── simulated_data.py      # 40 realistic AZ fire incidents for demo mode
│   ├── risk_analysis.py       # ISO 31010 analyses + report generation
│   ├── tak_export.py          # CoT Data Package + KML export for iTAK
│   ├── main.py                # Orchestrator script
│   └── generate_pdf_report.py # PDF report with ABM context + TAK screenshots
├── context/
│   ├── 2026-03-18_AZCIA-Notes.md
│   ├── 2026-05-02_Crucible-Coalition_Forms_Email-Thread.pdf
│   ├── 2026-05-14_Project-Crucible-Design.md
│   ├── literature_map.md
│   ├── neris_onepager.html
│   ├── NERIS_Risk-Report-Guide.md
│   └── Project-Crucible_Coalition-Report.md
├── images/                    # TAK screenshots + ABM visualizations
├── output/
│   ├── az_fire_incidents.zip  # CoT Data Package for iTAK
│   ├── az_fire_incidents.kml  # KML fallback
│   └── Project-Crucible_TAK-Visualization-Report.pdf
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
cd riskrunners/project-crucible

# Install dependencies
pip install -r requirements.txt

# Run pipeline (simulated data — no API credentials needed)
python3 src/main.py

# Generate PDF report
python3 src/generate_pdf_report.py
```

### Using Real NERIS Data

```bash
export NERIS_CLIENT_ID="your_client_id"
export NERIS_CLIENT_SECRET="your_client_secret"
python3 src/main.py
```

---

## Loading in iTAK (iPad)

1. Transfer `output/az_fire_incidents.zip` to iPad (AirDrop)
2. iTAK → ≡ menu → Data Packages → Import
3. Select the `.zip` file — fire markers appear on map
4. Tap a marker → tap callsign → scroll to **Remarks** for full risk report

---

## The Apex Vision

The iTAK proof of concept establishes the data pipeline. The next evolution is **Apex** — the VisionPro platform for immersive 3D situational awareness:

- **Drones** flown on regular schedules over fire-prone corridors
- **Video streams** combined with NERIS history and IoT sensor data
- **Apex vantage point** — "eyes in the sky" for fire marshals, underwriters, developers, and brush removal services
- **Collaborative remediation** — civic services and insurance industry jointly reducing fire risk

The complete pipeline achieves what the standard market cannot: making previously uninsurable fire-risk properties insurable through continuous, evidence-based risk scoring that rewards prevention.

---

## Connection to Captive Insurance

Project Crucible feeds directly into the [Integral Mass Captive](https://captive.integralmass.com) feasibility study. The same behavioral incentive from Medical Stop-Loss applies:

- **MSL:** Employers invest in wellness → keep underwriting profit
- **Fire Risk:** Communities invest in prevention → get lower premiums
- **GC Captive:** Contractors optimize quality → keep the dividend

---

## Stakeholders

- Arizona Captive Insurance Association (AZCIA)
- Crucible Coalition
- Casualty Actuaries of the Desert States
- Fire departments reporting through NERIS

---

## Links

- [Richards.plus](https://richards.plus)
- [RiskRunners.com](https://riskrunners.com)
- [captive.integralmass.com](https://captive.integralmass.com)
- [street.riskrunners.com](https://street.riskrunners.com) — ISO 31010 primers
- [NERIS](https://neris.fsri.org) — National Emergency Response Information System
- [NERIS API Docs](https://api.neris.fsri.org/v1/docs)

---

*Project Crucible — Insuring the uninsurable through data-driven risk intelligence.*
