# Flagship Platforms

[← Home](Home.md)

---

RiskRunners has three flagship platform projects, each with detailed project plans, prompt libraries, and working prototypes.

## 1. RiskRunners Platform Integration

**Timeline:** 90 days | **Budget:** $75K | **Location:** `platforms/01_riskrunners-integration/`

A unified platform integrating LinguaLint AI, the Lean Dream Prolog engine, and Agentic Procurement into a comprehensive risk analysis ecosystem.

### Components

#### Agentic Procurement (`agentic-procurement/`)
Automated procurement decision-making powered by AWS Bedrock Claude.

Key files:
- `ask_claude.py` — Claude API integration
- `evaluate_purchase.py` — Purchase evaluation logic
- `compliance_validator.py` — Compliance checking
- `simulation.py` — Procurement simulation
- `resilience_auditor.py` — Supply chain resilience auditing
- `stress_tester.py` — Stress testing procurement pipelines
- `master_auditor.py` — Orchestrates full audit workflows
- `html_report_generator.py` / `visual_report_generator.py` — Report output

#### Lean Dream (`lean-dream/`)
Prolog-based reasoning engine that converts public company risk factors (from 10-K filings on riskrunners.com) into queryable predicate calculus.

Sector-specific analysis directories:
- `housing/` — Housing nonprofit digital twins, PLM/ERP/CRM optimization
- `oil/` — Oil sector risk factor analysis
- `semiconductors/` — Taiwan blockade speculation, WOLFspeed analysis
- `persist/` — Persisted predicate calculus risk networks

The workflow:
1. Choose an archetypal company
2. Process risk factors into Prolog scripts (via Gemini 2.5 Pro)
3. Generate insightful queries
4. Document learned conditionals

---

## 2. Schrodinger's Fish Simulation Platform

**Timeline:** 75 days | **Budget:** $60K | **Location:** `platforms/02_schrodingers-fish/`

Agent-based simulation exploring antifragile social networks, value exchange, and posterity-focused decision-making. Inspired by Taleb's antifragility theory, Sugarscape models, and quantum mechanics metaphors.

### Core Simulation (`fish.py`)
Models agents with playbooks for value-creating operations, social pruning logic based on reciprocity, and wealthcare/healthcare KPIs. Outputs to CSV for Tableau visualization.

### Sub-Projects

#### Economic Overture (`economic-overture/`)
Quantitative behavioral economics analysis using Prospect Theory and agent-based modeling. Implements "The Dignity Arbitrage" framework.

Key models:
- `espresso_art_ecosystem.py` — Distressed social ecosystem modeling
- `solidarity_short.py` / `solidarity_short_detailed.py` — Contrarian social strategy
- `coming_in_hot_model.py` — Velocity override of loss aversion
- `vulnerability_arbitrage_analysis.py` — Trust building through authenticity
- `captive_audience_prospect_theory.py` — Kahneman/Tversky applied to social dynamics
- `market_exit_report_generator.py` — Dashboard and HTML report generation

#### Sugarscapes (`sugarscapes/`)
NetLogo implementations of classic Sugarscape models plus a custom "Sugar Oracle" simulation.

- `Sugarscape 1 Immediate Growback.nlogo`
- `Sugarscape 2 Constant Growback.nlogo`
- `Sugarscape 3 Wealth Distribution.nlogo`
- `sugar-oracle.py` — Candy consumption and insurance coverage simulation (FHIR/Prolog-inspired policy logic)
- `tableau-sugar-oracle.twb` — Tableau workbook for visualization

---

## 3. Actuarial Risk Assessment Platform

**Timeline:** 85 days | **Budget:** $68K

Production-ready actuarial platform with ISO 31000 compliance, parametric insurance, and exam preparation tools. This platform draws from the `actuarial-tools/` directory and the project plan in `projects/03_Actuarial_Risk_Assessment_Platform.csv`.

Planned features:
- ISO 31000 risk identification, analysis, and evaluation framework
- FM/P exam integration with numerical methods
- PFMEA (Process Failure Mode and Effects Analysis) for underwriting cycles
- Parametric insurance engine with IoT sensor integration
- NLP compliance checking for business rules

---

## Project Plans

All three platforms have structured project plans in `projects/`:

| Project | Plan CSV | Prompts CSV | Hours |
|---------|----------|-------------|-------|
| Platform Integration | `01_RiskRunners_Platform_Integration.csv` | `01_..._Prompts.csv` | ~500+ |
| Schrodinger's Fish | `02_Schrodingers_Fish_Simulation.csv` | `02_..._Prompts.csv` | ~400+ |
| Actuarial Risk Assessment | `03_Actuarial_Risk_Assessment_Platform.csv` | `03_..._Prompts.csv` | ~500+ |

Combined: 1,400+ hours of structured work with 134 AI-assisted development prompts.
