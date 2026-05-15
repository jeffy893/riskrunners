# Project Crucible: Insuring the Uninsurable
## A Coalition Report on Incentive-Aligned Captive Insurance & Real-Time Fire Risk Data

**Prepared:** 2026-05-07
**For:** Arizona Captive Insurance Association (AZCIA) · Crucible Coalition · Casualty Actuaries of the Desert States
**By:** Jefferson Richards — Richards+ / Linked Trust / AI Trailblazers
**Contact:** jefferson@richards.plus · 520.981.3639 · richards.plus

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Problem: Uninsurable Risk](#2-the-problem-uninsurable-risk)
3. [The Medical Stop-Loss Precedent](#3-the-medical-stop-loss-precedent)
4. [Application to General Contractors](#4-application-to-general-contractors)
5. [The NERIS Fire Data Pipeline](#5-the-neris-fire-data-pipeline)
6. [ISO 31010 Risk Methodology](#6-iso-31010-risk-methodology)
7. [The Captive Feasibility Study](#7-the-captive-feasibility-study)
8. [Actuarial Literature Substantiation](#8-actuarial-literature-substantiation)
9. [Pilot Proposal & Funding Request](#9-pilot-proposal--funding-request)
10. [Call to Action](#10-call-to-action)

---

## 1. Executive Summary

Project Crucible proposes a **data-driven pipeline** that transforms raw fire incident
data into actionable risk reports, enabling captive and standard-market insurers to
underwrite properties that are currently deemed uninsurable.

The model draws on a proven precedent: **Medical Stop-Loss (MSL) captive insurance**,
where employers who invest in employee wellness keep the underwriting profit. We apply
the same behavioral incentive structure to two domains:

1. **General Contractors** installing prefabricated homes — where quality installation
   reduces claims and returns dividends to the GC
2. **Fire-risk communities** — where investment in prevention (informed by NERIS data)
   reduces premiums and expands insurability

The pipeline:

```
IoT / Fire Departments → NERIS API → ISO 31010 Analysis → Risk Reports → Insurers
```

This report requests **pilot funding** to:
- Establish the NERIS API integration for Arizona fire corridors
- Validate the risk scoring model against historical NFIRS data
- Produce the first dynamic risk reports for captive underwriting
- Generate instructional materials for fire department analysts

---

## 2. The Problem: Uninsurable Risk

### 2.1 The Fire Insurance Crisis

Across the American West, homeowners and commercial property owners face a growing
crisis: standard-market insurers are withdrawing from fire-prone areas. The reasons:

- **Stale data**: NFIRS (1973–2025) delivered fire incident data with 6–18 month lag
- **Coarse granularity**: Address-only geolocation, single incident codes, range-based loss estimates
- **Binary classification**: Properties are either "insurable" or "not" — no gradient
- **No behavioral feedback**: Property owners have no mechanism to reduce premiums through prevention

### 2.2 The Construction Insurance Gap

Similarly, General Contractors adopting innovative prefabricated housing techniques
face a "learning curve" risk that standard carriers won't touch:

- New installation methods lack actuarial history
- Standard carriers require 5+ years of loss data before writing coverage
- GCs bear 100% of innovation risk with no profit-sharing upside
- Result: slower adoption of housing solutions during a housing crisis

### 2.3 The Common Thread

Both problems share a root cause: **the absence of a real-time data pipeline that
converts operational behavior into underwriting intelligence.**

---

## 3. The Medical Stop-Loss Precedent

### 3.1 How MSL Captives Work

In a Medical Stop-Loss captive, mid-sized employers:
1. Pay premiums into a shared captive pool
2. Cover "predictable" claims themselves (the retention layer)
3. Use the captive for catastrophic claims (the stop-loss layer)
4. **Keep the unused premium as profit** when claims are low

### 3.2 The Behavioral Shift

When employers discovered they could "keep the change," a documented behavioral
transformation occurred:

- Investment in **wellness programs** increased 3x
- Adoption of **direct primary care** arrangements accelerated
- Demand for **claims transparency** drove new data standards
- Employers became **active risk managers** rather than passive premium payers

### 3.3 Actuarial Validation

The following papers from the North American Actuarial Journal substantiate this model:

| Paper | Relevance |
|-------|-----------|
| Shared Savings Model Risk in the MSSP Program | Quantifies risk in shared-savings arrangements |
| Medicaid Managed Care: Efficiency, Medical Loss Ratio, and Quality | Demonstrates MLR as behavioral metric |
| Medicare Advantage: Medical Loss Ratio, Service Efficiency | Validates efficiency gains from profit-sharing |
| Potential "Savings" of Medicare: ACO Analysis | Shows how accountable care creates optimization |
| Subsidizing Inclusive Insurance to Reduce Poverty | Precedent for expanding coverage through incentives |

### 3.4 The Key Insight

**Financial alignment creates operational optimization.** When the person managing
the risk keeps the leftover money, they manage the risk better than any external
auditor ever could.

---

## 4. Application to General Contractors

### 4.1 The Parallel

| MSL (Health) | GC Captive (Construction) |
|:---|:---|
| Employer pays premium | GC pays premium |
| Employees stay healthy → lower claims | Installations done right → lower claims |
| Employer keeps unused premium | GC keeps underwriting dividend |
| Wellness programs emerge | Quality programs emerge |
| Data drives behavior | Data drives behavior |

### 4.2 The Integral Mass Captive Model

Our feasibility study at **captive.integralmass.com** demonstrates:

- **12 independent GCs** across 3 market segments (Student, Multi-Gen, Rural)
- **Monte Carlo validation**: <1% probability of ruin over 10 years
- **Solvency ratio**: 2.8x expected annual claims
- **Protected Cell Company (PCC)** architecture for scalable growth
- **Compliance**: Arizona Revised Statutes Title 20, Chapter 5, Article 2

### 4.3 The Innovation Insurance Product

Modeled after corporate R&D captives, our "GC Innovation Insurance" covers:
- Construction defects during learning-curve adoption of prefab methods
- Utility integration failures on new site types
- Schedule delays from technique refinement

The GC's incentive: **optimize installation quality → reduce claims → keep the dividend.**

---

## 5. The NERIS Fire Data Pipeline

### 5.1 What Changed in 2026

NFIRS — the 40-year-old national fire reporting system — was decommissioned in
early 2026. Its successor, **NERIS** (National Emergency Response Information System),
is now live with transformative capabilities:

| Attribute | NFIRS (old) | NERIS (new) |
|-----------|:-----------:|:-----------:|
| Data lag | 6–18 months | <24 hours |
| Geospatial | Address only | GIS-native lat/lon |
| API access | None | RESTful (public) |
| Incident types | Single code | Up to 3 tags |
| Property loss | Ranges | Structured fields |
| Response times | Limited | Granular timestamps |
| Cost to fire depts | Varies | $0 |

### 5.2 The Pipeline Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  ~27,000     │     │   NERIS      │     │  ISO 31010   │     │   CAPTIVE &  │
│  Fire & EMS  │────→│   API        │────→│  Risk        │────→│   STANDARD   │
│  Departments │     │  (<24hr lag) │     │  Analysis    │     │   MARKET     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                │
                                                ▼
                                     ┌──────────────────┐
                                     │  DYNAMIC RISK    │
                                     │  SCORES per zone │
                                     │  (replaces PPC)  │
                                     └──────────────────┘
```

### 5.3 Two Classes of Opportunity

**Class 1 — Cooperative Data Partnerships** (department-level, non-aggregated):
- Hyper-local response time analysis for property underwriting
- Suppression system effectiveness for commercial risk classification
- WUI incident density overlaid with policy portfolios

**Class 2 — Public Aggregated API** (free, PII-free, near-real-time):
- Dynamic ISO score modeling using actual incident metrics
- Community Risk Reduction (CRR) data for loss-prevention credits
- Statewide trend analysis for rate-making and catastrophe modeling

### 5.4 The ISO/PPC Connection

Fire department reporting completeness and response performance data in NERIS
**directly factors into ISO Public Protection Classification (PPC) scores** — the
metric driving homeowner and commercial property premiums.

Better data = demonstrable PPC improvement = lower premiums = expanded insurability.

---

## 6. ISO 31010 Risk Methodology

### 6.1 Techniques Applied

Project Crucible uses four ISO 31010 risk assessment techniques to transform raw
NERIS data into underwriting intelligence:

| Technique | ISO Section | Application |
|-----------|:-----------:|-------------|
| Bow Tie Analysis | B.4.2 | Map preventative & reactive controls around fire events |
| FMEA | B.4.3 | Prioritize failure modes by Risk Priority Number |
| Decision Tree | B.9.3 | Quantify ROI of prevention investments |
| Markov Analysis | B.5.9 | Model property risk state transitions over time |

### 6.2 Educational Foundation

The **Street Math** project (street.riskrunners.com) provides accessible primers
on each technique through narrative screenplays. These serve as training materials
for fire department analysts and coalition members who need to understand the
methodology without formal actuarial training.

### 6.3 Detailed Instructions

The companion document **"NERIS Risk Report Generation Guide"** provides:
- Python 3.10 code templates for each analysis technique
- Step-by-step instructions for populating models from NERIS API data
- Output format specifications for underwriter consumption
- Connection to the captive.integralmass.com solvency model

---

## 7. The Captive Feasibility Study

### 7.1 Simulation Results

| Metric | Value | Method |
|--------|:-----:|--------|
| Probability of Ruin | <1% | Monte Carlo (5,000 runs, 10yr) |
| Solvency Ratio | 2.8x | Expected annual claims |
| Initial Capitalization | $1M | 4x regulatory minimum |
| Risk Event Rate | 15% | Validated via queuing simulation |
| GC Count | 12 | Across 3 uncorrelated markets |

### 7.2 Regulatory Compliance

The study demonstrates compliance with Arizona Revised Statutes Title 20, Chapter 5,
Article 2:

- ✅ Risk Distribution: 12+ independent risk units
- ✅ Minimum Capitalization: $1M (4x the $250K minimum)
- ✅ Feasibility Study: Executable codebase with reproducible results
- ✅ PCC Structure: A.R.S. § 20-1098 et seq.

### 7.3 The Bridge to Fire Risk

The same captive architecture that insures GC installation risk can house a
**fire risk cell**:

```
┌─────────────────────────────────────────────────────────┐
│                  INTEGRAL MASS CORE                      │
│    Regulatory Compliance · Reinsurance · Admin          │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
   │ CELL A  │       │ CELL B  │       │ CELL C  │
   │ GC      │       │ FIRE    │       │ Property│
   │ Install │       │ RISK    │       │ Owners  │
   │ Risk    │       │ (NERIS) │       │ Alliance│
   └─────────┘       └─────────┘       └─────────┘
```

Cell B uses NERIS data to dynamically price fire risk for properties that standard
carriers have abandoned — making the uninsurable insurable.

---

## 8. Actuarial Literature Substantiation

The companion document **"Actuarial Literature Map"** classifies 51 peer-reviewed
papers from the North American Actuarial Journal into six research themes:

1. **Medical Stop-Loss & Behavioral Incentives** — Precedent for profit-sharing models
2. **Catastrophe & Fire Risk Modeling** — Geospatial risk scoring methods
3. **Predictive Analytics & Machine Learning** — Computational validation
4. **Underwriting Cycle & Capital Markets** — Financial architecture context
5. **Cyber & Emerging Risk** — IoT pipeline parallels
6. **Insurance Pricing & Fairness** — Expanding coverage, not excluding

Key papers supporting the core thesis:

| Theme | Paper | Connection |
|-------|-------|------------|
| MSL | Shared Savings Model Risk in MSSP | Quantifies shared-savings risk |
| Fire | Wildfire Loss Modeling: Semiparametric | Validates geospatial fire scoring |
| Fire | Storm CAT Bond: Modeling and Valuation | Catastrophe bond pricing for fire |
| ML | Poisson Mixture Deep Learning for Claims | Neural network claims prediction |
| ML | Recurrent Neural Networks for Loss Reserving | Time-series loss modeling |
| Cycle | Drivers of the Underwriting Cycle | When captives fill market gaps |
| Cyber | Spatial Cyber Loss Clusters | Geospatial risk aggregation methods |
| Pricing | The Discriminating (Pricing) Actuary | Fair pricing for expanded access |

---

## 9. Pilot Proposal & Funding Request

### 9.1 Three-Phase Pilot

| Phase | Duration | Deliverable | Budget |
|:-----:|:--------:|-------------|:------:|
| 1 | 3 months | NERIS API integration + Arizona incident mapping | $25,000 |
| 2 | 3 months | ISO 31010 risk analysis + model validation vs. NFIRS history | $35,000 |
| 3 | 6 months | Dynamic risk scoring + first captive cell underwriting | $65,000 |

**Total pilot budget: $125,000**

### 9.2 Phase 1 — Connect (Months 1–3)

- Establish API integration with NERIS aggregated feed for Arizona
- Map NERIS geospatial fields to existing property/policy databases
- Identify 3 target zones: 1 urban, 1 WUI, 1 rural
- Produce baseline incident analysis for each zone
- Deliverable: **Data pipeline operational + baseline report**

### 9.3 Phase 2 — Analyze (Months 4–6)

- Apply ISO 31010 methodology (Bow Tie, FMEA, Decision Tree, Markov)
- Validate risk scores against 45 years of NFIRS historical data (OpenFEMA)
- Calibrate transition matrices for Arizona-specific conditions
- Train fire department analysts using Street Math materials
- Deliverable: **Validated risk model + analyst training guide**

### 9.4 Phase 3 — Underwrite (Months 7–12)

- Deliver dynamic risk scoring to captive Cell B
- Price first policies for previously uninsurable fire-risk properties
- Establish feedback loop: prevention investment → score improvement → premium reduction
- Publish results for AZCIA and broader captive community
- Deliverable: **First policies written + published case study**

### 9.5 Success Metrics

| Metric | Target |
|--------|--------|
| Properties scored | 500+ in 3 Arizona zones |
| Previously uninsurable properties now insurable | 50+ |
| Premium reduction for prevention-investing properties | 15–25% |
| Risk report generation time | <4 hours per zone |
| Fire department analyst training completion | 10+ analysts |

---

## 10. Call to Action

### For AZCIA Members

Project Crucible represents the next evolution of Arizona's captive insurance
leadership. The state that pioneered captive-friendly regulation can now pioneer
**data-driven alternative risk transfer for fire-prone communities.**

**Ask:** Review this proposal and consider sponsoring Phase 1 through the AZCIA
innovation fund or member contributions.

### For Crucible Coalition Members

The NERIS API is live. The feasibility study is validated. The actuarial literature
supports the model. What remains is execution.

**Ask:** Commit to the pilot timeline and identify your organization's role:
- Data partner (fire departments, state fire marshal)
- Technical partner (API integration, risk modeling)
- Capital partner (pilot funding, captive capitalization)
- Distribution partner (connecting uninsured property owners to coverage)

### For Potential Funders

This pilot has dual ROI:
1. **Financial**: First-mover advantage in a market segment (fire-risk captive) that
   doesn't exist yet
2. **Social**: Expanding insurance access to communities facing coverage withdrawal

**Ask:** Fund the $125K pilot. Expected return: operational captive cell within 12
months, with a scalable model applicable to any state with NERIS data access.

---

## Appendices

- **Appendix A:** Actuarial Literature Map (see `literature_map.md`)
- **Appendix B:** NERIS Risk Report Generation Guide (see `NERIS_Risk-Report-Guide.md`)
- **Appendix C:** captive.integralmass.com simulation code (open source)
- **Appendix D:** Street Math ISO 31010 primers (street.riskrunners.com)
- **Appendix E:** NERIS One-Pager (see `neris_onepager.html`)

---

*"If you let the person in charge of the risk keep the leftover money,
they will manage the risk better than any external auditor ever could."*

— Project Crucible thesis, derived from Medical Stop-Loss captive outcomes

---

**Project Crucible** · Richards+ · Linked Trust · AI Trailblazers · University of Arizona Risk Runners
jefferson@richards.plus · 520.981.3639 · richards.plus
