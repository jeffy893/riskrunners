# NERIS Fire Data → Risk Report Generation Guide

*Project Crucible — Prepared 2026-05-07*
*For: Arizona Captive Insurance Association, Crucible Coalition, Fire Department Analysts*

---

## Executive Summary

This guide provides step-by-step instructions for generating actuarial-grade risk
reports from NERIS (National Emergency Response Information System) fire incident data.
The output feeds directly into the Project Crucible underwriting pipeline:

```
IoT Sensors → NERIS API → Risk Analysis (this guide) → Risk Reports → Insurers
```

The goal: **make previously uninsurable fire-risk properties insurable** by providing
granular, near-real-time risk data that replaces the outdated NFIRS annual bulk approach.

---

## Prerequisites

| Requirement | Source |
|-------------|--------|
| NERIS API access | neris.fsri.org (free for verified research orgs) |
| Python 3.10+ | python.org |
| ISO 31010:2019 reference | Available via ANSI or ISO store |
| Street Math primers | street.riskrunners.com (Bow Tie, Decision Tree, Markov) |
| Historical baseline | OpenFEMA NFIRS data (1980–2025) |

---

## Step 1: Data Acquisition from NERIS API

### 1.1 Connect to the NERIS Public API

```python
import requests
from datetime import datetime, timedelta

NERIS_BASE_URL = "https://api.neris.fsri.org/v1"  # Placeholder — confirm with FSRI

def fetch_incidents(state: str = "AZ", days_back: int = 90) -> list:
    """
    Fetch recent fire incidents for a given state.
    Returns list of incident records with geospatial and loss data.
    """
    params = {
        "state": state,
        "start_date": (datetime.now() - timedelta(days=days_back)).isoformat(),
        "end_date": datetime.now().isoformat(),
        "incident_type": "fire",
        "format": "json"
    }
    response = requests.get(f"{NERIS_BASE_URL}/incidents", params=params)
    response.raise_for_status()
    return response.json()["incidents"]
```

### 1.2 Key Fields to Extract

| NERIS Field | Use in Risk Report |
|-------------|-------------------|
| `geospatial.lat`, `geospatial.lon` | Property-level risk scoring |
| `timestamps.dispatch`, `timestamps.arrival` | Response time analysis |
| `property_loss.amount` | Severity distribution fitting |
| `suppression_system.performance` | Mitigation credit calculation |
| `incident_type_tags[]` | Multi-hazard classification |
| `location.property_use` | Occupancy-based risk class |

---

## Step 2: Bow Tie Analysis (ISO 31010 B.4.2)

> **Primer:** street.riskrunners.com/screenplay_bow_tie_analysis.html

A Bow Tie maps the **threat** (center), **preventative controls** (left), and
**reactive controls** (right) around a fire loss event.

### 2.1 Structure

```
PREVENTATIVE CONTROLS          THREAT EVENT          REACTIVE CONTROLS
─────────────────────         ─────────────         ─────────────────
• Building codes              │             │       • Sprinkler activation
• Vegetation mgmt             │  STRUCTURE  │       • FD response time
• Electrical inspection       │    FIRE     │       • Mutual aid
• Smoke detectors             │             │       • Evacuation plan
• WUI buffer zones            │             │       • Salvage operations
─────────────────────         ─────────────         ─────────────────
```

### 2.2 Populating from NERIS Data

```python
def build_bow_tie(incidents: list) -> dict:
    """
    Analyze incidents to populate bow tie control effectiveness.
    """
    bow_tie = {
        "threat": "Structure Fire",
        "preventative_controls": {},
        "reactive_controls": {}
    }

    # Preventative: detector presence vs. fire occurrence
    detector_present = sum(1 for i in incidents if i.get("detector_present"))
    detector_activated = sum(1 for i in incidents if i.get("detector_activated"))
    bow_tie["preventative_controls"]["smoke_detector"] = {
        "presence_rate": detector_present / len(incidents) if incidents else 0,
        "activation_rate": detector_activated / detector_present if detector_present else 0,
        "effectiveness": "HIGH" if detector_activated / max(detector_present, 1) > 0.85 else "MODERATE"
    }

    # Reactive: response time distribution
    response_times = []
    for i in incidents:
        ts = i.get("timestamps", {})
        if ts.get("dispatch") and ts.get("arrival"):
            delta = (ts["arrival"] - ts["dispatch"]).total_seconds() / 60
            response_times.append(delta)

    if response_times:
        import statistics
        bow_tie["reactive_controls"]["fd_response"] = {
            "mean_minutes": statistics.mean(response_times),
            "median_minutes": statistics.median(response_times),
            "p90_minutes": sorted(response_times)[int(0.9 * len(response_times))],
            "effectiveness": "HIGH" if statistics.median(response_times) < 6 else "LOW"
        }

    return bow_tie
```

### 2.3 Output for Underwriters

The bow tie analysis produces a **Control Effectiveness Score** for each property
zone. Properties in zones with HIGH preventative AND HIGH reactive controls qualify
for standard-market placement. Properties with LOW on either side are candidates for
the captive's alternative risk transfer.

---

## Step 3: Failure Mode & Effects Analysis (FMEA)

> **Related primer:** street.riskrunners.com/screenplay_ishikawa_fishbone_analysis.html

### 3.1 FMEA Table for Fire Risk

| Failure Mode | Cause | Effect | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN |
|-------------|-------|--------|:---:|:---:|:---:|:---:|
| Suppression system failure | Maintenance lapse | Uncontrolled spread | 9 | 3 | 4 | 108 |
| Delayed dispatch | CAD system error | Extended response | 7 | 2 | 3 | 42 |
| WUI encroachment | Development creep | Structure exposure | 8 | 5 | 6 | 240 |
| Electrical ignition | Aging infrastructure | Fire initiation | 8 | 4 | 5 | 160 |
| Inadequate water supply | Hydrant spacing | Suppression failure | 9 | 3 | 4 | 108 |

### 3.2 Calculating RPN from NERIS Data

```python
def calculate_rpn(incidents: list, zone_id: str) -> list:
    """
    Calculate Risk Priority Numbers for failure modes in a given zone.
    Uses NERIS incident history to calibrate Occurrence and Detection scores.
    """
    zone_incidents = [i for i in incidents if i.get("zone") == zone_id]
    total = len(zone_incidents) if zone_incidents else 1

    failure_modes = []

    # Suppression system failure
    suppression_failures = sum(
        1 for i in zone_incidents
        if i.get("suppression_system", {}).get("performance") == "failed"
    )
    severity = 9
    occurrence = min(10, int((suppression_failures / total) * 30) + 1)
    detection = 4  # Inspections exist but are periodic
    failure_modes.append({
        "mode": "Suppression system failure",
        "severity": severity,
        "occurrence": occurrence,
        "detection": detection,
        "rpn": severity * occurrence * detection
    })

    # Add more failure modes following same pattern...
    return failure_modes
```

---

## Step 4: Decision Tree for Resource Allocation (ISO 31010 B.9.3)

> **Primer:** street.riskrunners.com/screenplay_decision_tree_analysis.html

### 4.1 Decision: Allocate Fire Prevention Resources

```
                    [DECISION: Invest in Zone X Prevention?]
                   /                                        \
          YES ($50K/yr)                              NO ($0)
         /            \                            /          \
   Fire occurs    No fire                   Fire occurs    No fire
   P=0.05         P=0.95                    P=0.15         P=0.85
   Loss=$200K     Loss=$0                   Loss=$500K     Loss=$0
   EV=-$10K       EV=$0                     EV=-$75K       EV=$0
         \            /                            \          /
      EV(YES) = -$50K + (-$10K + $0)         EV(NO) = -$75K + $0
             = -$60K                                = -$75K

      → INVEST: Expected savings of $15K/year
```

### 4.2 Parameterizing from NERIS

```python
def decision_tree_invest(zone_incidents: list, investment_cost: float) -> dict:
    """
    Build a decision tree for fire prevention investment using NERIS data.
    """
    n = len(zone_incidents) if zone_incidents else 1

    # Current fire probability (without investment)
    fires = sum(1 for i in zone_incidents if "fire" in i.get("incident_type_tags", []))
    p_fire_current = fires / n

    # Estimated reduction from prevention (literature suggests 40-60%)
    reduction_factor = 0.60
    p_fire_with_investment = p_fire_current * (1 - reduction_factor)

    # Average loss from NERIS property_loss field
    losses = [i.get("property_loss", {}).get("amount", 0) for i in zone_incidents if i.get("property_loss")]
    avg_loss = sum(losses) / len(losses) if losses else 250_000

    ev_no_invest = -(p_fire_current * avg_loss)
    ev_invest = -investment_cost - (p_fire_with_investment * avg_loss)

    return {
        "invest": {
            "cost": investment_cost,
            "p_fire": p_fire_with_investment,
            "expected_loss": p_fire_with_investment * avg_loss,
            "ev": ev_invest
        },
        "no_invest": {
            "cost": 0,
            "p_fire": p_fire_current,
            "expected_loss": p_fire_current * avg_loss,
            "ev": ev_no_invest
        },
        "recommendation": "INVEST" if ev_invest > ev_no_invest else "DO NOT INVEST",
        "annual_savings": ev_invest - ev_no_invest
    }
```

---

## Step 5: Markov State Model for Property Risk Classification

> **Primer:** street.riskrunners.com/screenplay_markov_analysis.html

### 5.1 Property Risk States

```
    ┌──────────┐    deterioration    ┌──────────┐    incident    ┌──────────┐
    │  LOW     │ ──────────────────→ │ MODERATE │ ────────────→  │  HIGH    │
    │  RISK    │                     │  RISK    │                │  RISK    │
    └──────────┘ ←────────────────── └──────────┘ ←────────────  └──────────┘
                    mitigation                      remediation
```

### 5.2 Transition Matrix from NERIS History

```python
import numpy as np

def build_transition_matrix(property_history: list) -> np.ndarray:
    """
    Build a Markov transition matrix from property incident history.

    States: 0=Low Risk, 1=Moderate Risk, 2=High Risk
    """
    # Count transitions between states over time periods
    transitions = np.zeros((3, 3))

    for i in range(len(property_history) - 1):
        current_state = property_history[i]["risk_state"]
        next_state = property_history[i + 1]["risk_state"]
        transitions[current_state][next_state] += 1

    # Normalize rows to get probabilities
    row_sums = transitions.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1  # avoid division by zero
    matrix = transitions / row_sums

    return matrix


def predict_risk_state(current_state: int, matrix: np.ndarray, years: int = 5) -> np.ndarray:
    """
    Predict probability distribution over risk states after N years.
    """
    state_vector = np.zeros(3)
    state_vector[current_state] = 1.0

    for _ in range(years):
        state_vector = state_vector @ matrix

    return state_vector
```

### 5.3 Underwriting Application

The steady-state distribution tells insurers what proportion of properties in a zone
will be in each risk class over time. This directly informs:
- **Premium setting** (higher premiums for zones trending toward HIGH)
- **Loss reserves** (capital allocation based on expected state distribution)
- **Prevention ROI** (how mitigation investments shift the transition matrix)

---

## Step 6: Generating the Final Risk Report

### 6.1 Report Structure

```python
def generate_risk_report(zone_id: str, incidents: list) -> str:
    """
    Generate a complete risk report for a geographic zone.
    """
    bow_tie = build_bow_tie(incidents)
    fmea = calculate_rpn(incidents, zone_id)
    decision = decision_tree_invest(incidents, investment_cost=50_000)

    report = f"""
# Fire Risk Report — Zone {zone_id}
Generated: {date.today().isoformat()}
Data Source: NERIS API (last 90 days)

## 1. Bow Tie Analysis
- Preventative Control Effectiveness: {bow_tie['preventative_controls']}
- Reactive Control Effectiveness: {bow_tie['reactive_controls']}

## 2. Failure Mode Analysis (Top 3 by RPN)
{chr(10).join(f"- {fm['mode']}: RPN={fm['rpn']}" for fm in sorted(fmea, key=lambda x: x['rpn'], reverse=True)[:3])}

## 3. Investment Decision
- Recommendation: {decision['recommendation']}
- Annual Expected Savings: ${abs(decision['annual_savings']):,.0f}

## 4. Risk Classification
- Current State: [from Markov model]
- 5-Year Projection: [from transition matrix]

## 5. Underwriting Recommendation
[Based on combined analysis above]
"""
    return report
```

---

## Connection to Project Crucible Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROJECT CRUCIBLE DATA PIPELINE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  IoT Sensors ──→ NERIS API ──→ THIS GUIDE ──→ Risk Reports ──→ Insurers│
│  (fire depts)    (real-time)   (ISO 31010)    (per-zone)     (captive  │
│                                                               + market) │
│                                                                         │
│  Parallel to Medical Stop-Loss:                                         │
│  Health Data ──→ Claims API ──→ Wellness ──→ Loss Reports ──→ Employers │
│  (hospitals)     (real-time)   Programs     (per-group)     (keep the  │
│                                                              savings)   │
└─────────────────────────────────────────────────────────────────────────┘
```

The same behavioral incentive applies:
- In **MSL**: Employers who invest in wellness keep the underwriting profit
- In **Fire Risk**: Communities that invest in prevention get lower premiums
- In **GC Captive**: Contractors who optimize quality keep the dividend

---

## References

- NERIS Framework Schema: github.com/ulfsri/neris-framework
- ISO 31010:2019 Risk Assessment Techniques
- Street Math (ISO 31010 primers): street.riskrunners.com
- captive.integralmass.com (Monte Carlo solvency model)
- OpenFEMA NFIRS Historical Data: www.fema.gov/about/openfema/data-sets

---

*Prepared by Project Crucible — Richards+ / Linked Trust / AI Trailblazers*
*Contact: jefferson@richards.plus | 520.981.3639*
