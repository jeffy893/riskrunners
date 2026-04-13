# Legacy Projects

[← Home](Home.md)

---

Historical implementations and research projects in `legacy/`. These demonstrate foundational concepts and technical breadth across healthcare, education, AI, and simulation domains.

## Dark Campus

`legacy/dark-campus/`

An agent-based model exploring attention distribution on a college campus, inspired by the metaphor of light pollution drowning out stars.

### The Metaphor
City lights drown out the stars — dominant factors (NIL deals, high-visibility groups) obscure the needs of less visible groups (e.g., mathletes needing wellness support). A "dark city" self-imposes bylaws to limit light pollution, enabling everyone to see the stars.

### The Simulation
Models `StudentGroup` agents (Athletes, Mathletes, DramaClub, DebateTeam) competing for campus attention. A "Fairness Policy" bylaw is introduced mid-simulation that taxes high-attention groups and redistributes to high-need groups.

Key parameters:
- 55 agents across 4 group types
- Athletes: high visibility (0.5–0.8), low need (0.1–0.4)
- Mathletes: low visibility (0.05–0.2), high need (0.7–1.0)
- Bylaw activates at step 50 of 100, with 15% tax rate

**Output:** `campus_attention_model_output_v2.csv` for Tableau analysis
**Visualization:** `dark-campus-dash.twb` (Tableau workbook)

---

## Family FHIR

`legacy/family-fhir/`

A "Family Charter" concept that translates insurance policy exclusions into actionable behavioral bylaws for high-net-worth families.

### Three-Phase Process
1. **Audit** — Consolidate insurance portfolio into structured dataset
2. **Risk Matrix** — Identify and quantify Value at Risk per behavior (e.g., $5M primary residence at risk from missing flood insurance)
3. **Family Charter** — Convert exclusions into plain-language family rules

Example bylaw: "The Classic Car is not to be driven more than 2,500 miles/year, as this would void insurance coverage on a $250,000 asset."

---

## Humanitarian Gambit

`legacy/humanitarian-gambit/`

A game theory simulation exploring how international debt priority structures could be altered through humanitarian burden-sharing.

### The Core Mechanism: Priority Swap
"Responsibility to Protect implies Right to Collect" — any country that accepts refugees from a debtor nation gains senior priority status on that nation's natural resources.

### The Lithium Gambit Scenario
- Country C1 (Salara): $10B lithium reserves, politically unstable
- Country B1 (EastBloc): $6B senior debt
- Country A1 (WestFed): $5B junior debt (out of the money)
- 100,000 refugees at $25K each = $2.5B hosting cost

Under the Priority Swap, WestFed spends $2.5B on refugees to secure full $5B repayment — a net $2.5B profit.

### Three Dark Equilibria
1. **Predatory Humanitarianism** — Junior creditors incentivized to destabilize source nations
2. **Credit Market Collapse** — Senior lenders stop lending to unstable nations
3. **Human Collateral** — Source nations weaponize population displacement for debt restructuring

**Run:** `python3.10 simulation.py`
**Output:** `simulation_results.png` — Multi-panel visualization dashboard

---

## AI Trailblazers

`legacy/ai-trailblazers/Jan2026-hackathon/`

Hackathon materials from January 2026, bridging the gap between AI-literate and non-literate communities. Led by Aaron Eden and Maria Eden.

Files:
- `ai-trailblazers-hackathon.xml` — Project structure
- `hackathon-resources.csv` — Resource list
- `hackathon-tasks.csv` — Task breakdown
