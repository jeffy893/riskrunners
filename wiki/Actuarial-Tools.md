# Actuarial Tools

[← Home](Home.md)

---

Professional actuarial science tools, exam preparation materials, and risk modeling frameworks. Located in `actuarial-tools/`.

## Exam Preparation

### FM Exam (Financial Mathematics)
`Actuary_FM_EXAM/`

Organized into:
- **FM_EXAM_BREAKDOWN** — Topic-by-topic breakdown of the FM exam
- **FM_FORMULAS** — Formula sheets and reference material
- **FM_RESOURCES** — Study guides and external resources
- **FM_SAMPLE_EXAMS** — Practice exams
- **FM_TEST_SOLUTIONS** — Worked solutions
- **FM_TEXTS** — Textbook materials

### P Exam (Probability)
`Actuary_P_EXAM/`

Organized into:
- **P_EXAM_BREAKDOWN** — Topic breakdown
- **P_FORMULAS** — Probability formula sheets
- **P_RESOURCES** — Study resources
- **P_SAMPLE_EXAMS** — Practice exams
- **P_TEXTS** — Textbook materials

### FM/P Testing Tools
`fmptests/`

Python implementations for core actuarial calculations:
- `annuity/annuity.py` — Annuity calculations
- `annuity/perpetuity.py` — Perpetuity calculations
- `bond/bond.py` — Bond pricing
- `interest/accumulation.py` — Accumulation functions
- `interest/basicInterest.py` — Simple and compound interest

---

## Financial Modeling

`finance/`

### Reference Scripts (`ref/`)
- `fin412.py` — Finance 412 course reference implementations
- `tvm.py` — Time value of money utilities

### Stock Analysis (`stocks/`)
- JSON data files for stocks: AAPL, BA, BX, CG, FDX, GD, IBM, INTC, KKR, LIT, LMT, NOC, RTN
- `portfolio.py` / `portfolio_archive.py` — Portfolio construction and covariance analysis
- `index2018May.py` / `indexCurve2018.py` — Index curve generation
- `loadIndexJson.py` — JSON data loader

### Time Value of Money (`tvm/`)
- `bond.py` — Bond pricing and yield calculations
- `duration_single_cf.py` / `duration_mult_cf.py` — Duration calculations
- `cash_flows.csv` / `rr_cf.csv` — Cash flow datasets

---

## ISO 31000 Risk Data Model

`ISO_RISK_DATA_MODEL/`

A complete ISO 31000-compliant risk assessment framework implemented as 17 interrelated CSV files:

| File | Purpose |
|------|---------|
| `SCOPE.csv` | Risk management scope definition |
| `POLICY_OBJECTIVES.csv` | Policy objectives and goals |
| `CONTEXT_SUMMARY.csv` | Organizational context |
| `CONTEXT_STAKEHOLDER.csv` | Stakeholder analysis |
| `GOVERNANCE_FUNCTION.csv` | Governance structure |
| `ACCOUNTABLE.csv` | Accountability assignments |
| `RISK_IDEN.csv` | Risk identification |
| `RISK_ANALYSIS.csv` | Risk analysis |
| `RISK_EVAL.csv` | Risk evaluation |
| `RISK_CRITERIA.csv` | Risk criteria definitions |
| `RISK_TREATMENT.csv` | Risk treatment plans |
| `RISK_QUESTION.csv` | Risk assessment questions |
| `RISK_SUMMARY.csv` | Risk summary dashboard |
| `EVENT_SUMMARY.csv` | Event tracking |
| `COMMUNICATIONS.csv` | Communication plans |
| `PERFORMANCE_MEASURES.csv` | Performance metrics |
| `SEMANTIC_RISK.csv` | Semantic risk categorization |

---

## Research

`research/`

### Parametric Insurance (`parametric_insurance.txt`)
Explores how claims departments interact with parametric insurance models, the relationship between negligence/intention and claim payoffs, and the connection to Responsibility Futures. Covers index triggers, adverse/perverse basis risk, blockchain smart contracts, and insurance-linked securities.

### Intangible Goods Insurance (`intangiblegoods_insurance.txt`)
Analysis of insuring intangible assets (IP, goodwill, software, trademarks, data). Covers the gap between tangible (60% covered) and intangible (16% covered) asset insurance, brand valuation methods, patent insurance, cyber insurance, and data as a fungible asset.

### IoT Data Sources (`iot_data_sources.txt`)
Curated list of Kaggle datasets for IoT-driven actuarial modeling: crowd counting, temperature/humidity sensors, and IoT device captures.

---

## Language References

`lang-ref/`

Reference materials for actuarial programming:
- `prob/` — Probability implementations
- `python/` — Python reference scripts
- `rlang/` — R language reference
- `tensor/` — TensorFlow reference
