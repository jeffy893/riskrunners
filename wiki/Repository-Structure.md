# Repository Structure

[← Home](Home.md)

---

## Top-Level Layout

```
riskrunners/
├── actuarial-tools/       # Exam prep, financial math, ISO risk data, research
├── legacy/                # Historical projects and proof-of-concepts
├── models/                # Standalone simulation models
├── platforms/             # Flagship platform implementations
├── project-crucible/      # NERIS fire data → ISO 31010 → iTAK/VisionPro
├── projects/              # Project plans (CSV) and prompt libraries
├── responsibility-futures/# R = I/N engine with Cortext.io integration
├── street-math/           # ISO 31010 screenplays
├── UA-RiskRunners-Presentation/  # University of Arizona talk materials
├── wiki/                  # This wiki
├── CODEOWNERS             # @jeffy893
├── LICENSE                # MIT
└── README.md              # Main repo overview
```

---

## Detailed Breakdown

### `actuarial-tools/`
```
actuarial-tools/
├── Actuary_FM_EXAM/          # Financial Mathematics exam prep
│   ├── FM_EXAM_BREAKDOWN/
│   ├── FM_FORMULAS/
│   ├── FM_RESOURCES/
│   ├── FM_SAMPLE_EXAMS/
│   ├── FM_TEST_SOLUTIONS/
│   └── FM_TEXTS/
├── Actuary_P_EXAM/           # Probability exam prep
│   ├── P_EXAM_BREAKDOWN/
│   ├── P_FORMULAS/
│   ├── P_RESOURCES/
│   ├── P_SAMPLE_EXAMS/
│   └── P_TEXTS/
├── finance/
│   ├── ref/                  # fin412.py, tvm.py
│   ├── stocks/               # Stock JSON data (AAPL, BA, IBM, etc.) + portfolio scripts
│   └── tvm/                  # Time value of money: bond.py, duration, cash flows
├── fmptests/
│   ├── annuity/              # annuity.py, perpetuity.py
│   ├── bond/                 # bond.py
│   └── interest/             # accumulation.py, basicInterest.py
├── ISO_RISK_DATA_MODEL/      # 17 CSV files implementing ISO 31000
├── lang-ref/                 # Language references (Python, R, probability, TensorFlow)
├── Numerical_Methods/        # Random sampling methods
├── research/                 # Parametric insurance, intangible goods, IoT data sources
└── README.md
```

### `platforms/`
```
platforms/
├── 01_riskrunners-integration/
│   ├── agentic-procurement/  # AWS Bedrock Claude procurement automation
│   └── lean-dream/           # Prolog-based risk factor reasoning
│       ├── housing/
│       ├── oil/
│       ├── persist/
│       └── semiconductors/
├── 02_schrodingers-fish/
│   ├── economic-overture/    # Behavioral economics + Prospect Theory models
│   ├── sugarscapes/          # NetLogo Sugarscape simulations + Sugar Oracle
│   ├── fish.py               # Core simulation
│   └── simulation_output.csv
└── README.md
```

### `responsibility-futures/`
```
responsibility-futures/
├── src/
│   ├── cortext_integration.py    # Cortext.io JSON processing
│   ├── enhanced_workflow.py      # Complete workflow manager
│   ├── report_generator.py       # HTML/PNG report generation
│   ├── responsibility-futures.py # Original algorithm
│   └── responsibility-index.py   # Core R = I/N logic
├── docs/                         # Research papers and theory
├── examples/                     # example_usage.py
├── run_analysis.sh               # Unix execution script
├── run_analysis.bat              # Windows execution script
└── requirements.txt
```

### `projects/`
```
projects/
├── 01_RiskRunners_Platform_Integration.csv         # 90-day project plan
├── 01_RiskRunners_Platform_Integration_Prompts.csv  # AI dev prompts
├── 02_Schrodingers_Fish_Simulation.csv             # 75-day project plan
├── 02_Schrodingers_Fish_Simulation_Prompts.csv
├── 03_Actuarial_Risk_Assessment_Platform.csv       # 85-day project plan
├── 03_Actuarial_Risk_Assessment_Platform_Prompts.csv
└── README.md
```

### `legacy/`
```
legacy/
├── ai-trailblazers/          # AI mentorship hackathon (Jan 2026)
├── dark-campus/              # Campus attention model (ABM + Tableau)
├── family-fhir/              # Insurance behavioral bylaws / Family Charter
└── humanitarian-gambit/      # Game theory: debt priority + refugee dynamics
```

### `models/`
```
models/
├── capital-lifecycle/        # S-curve life capital model (Python + matplotlib)
├── linguistics/              # French subjunctive and cultural analysis
└── pickleball/               # Ladder league simulation (Python + Tableau)
```

### `project-crucible/`
```
project-crucible/
├── src/
│   ├── config.py              # Configuration, env vars, simulated data fallback
│   ├── neris_client.py        # NERIS API client (OAuth2 + paginated fetch)
│   ├── simulated_data.py      # Realistic AZ fire incidents for demo mode
│   ├── risk_analysis.py       # ISO 31010 analyses (Bow Tie, FMEA, Decision Tree, Markov)
│   ├── tak_export.py          # CoT Data Package + KML export for iTAK
│   ├── main.py                # Orchestrator script
│   └── generate_pdf_report.py # PDF report with ABM context + TAK screenshots
├── context/                   # Research notes, coalition reports, NERIS one-pager
├── images/                    # TAK screenshots + ABM visualizations
├── output/                    # Generated .zip (CoT), .kml, and .pdf
├── requirements.txt
└── README.md
```
