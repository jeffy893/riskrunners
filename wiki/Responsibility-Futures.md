# Responsibility Futures

[← Home](Home.md)

---

Located in `responsibility-futures/`. A Python engine that quantifies responsibility through AI-extracted event analysis, integrated with [Cortext.io](https://cortext.io).

## Core Philosophy

Responsibility is measurable through the relationship between Intention and Negligence:

```
R = I / N

Where:
  I (Intention) = Derived from warm vectors (Positivity, Engagement, Optimism)
  N (Negligence) = Derived from cold vectors (Negativity, Risk, Uncertainty)
```

This creates a quantifiable responsibility index that moves beyond traditional credit scores to measure "social and scope capital."

## How It Works

### Data Pipeline
```
Text Input → Cortext.io NLP → JSON Events → Responsibility Engine → HTML Reports + PNG Charts
```

1. **Input Processing** — Accepts Cortext.io JSON reports containing sentences with warm/cold sentiment vectors, extracted subjects and phenomena
2. **Entity Analysis** — Calculates mention frequency, average warm/cold vectors, and contextual concepts per entity
3. **Responsibility Calculation**
   - Intention Score: `Positivity × 0.4 + Engagement × 0.4 + Optimism × 0.2`
   - Negligence Score: `Negativity × 0.5 + Risk × 0.3 + Uncertainty × 0.2`
   - R-Ratio with risk level classification (Low / Moderate / High)
4. **Visualization** — Generates responsibility matrix dashboards, vector heatmaps, statistical summaries, and HTML reports

## Quick Start

```bash
# Complete workflow
./run_analysis.sh

# Or manually
python src/enhanced_workflow.py

# Process a specific file
python src/enhanced_workflow.py --input /path/to/extraction_file.json
```

## Source Files

| File | Purpose |
|------|---------|
| `src/cortext_integration.py` | Main engine — loads Cortext.io JSON, extracts entities, calculates R-ratios |
| `src/report_generator.py` | HTML/PNG report generation with matplotlib and seaborn |
| `src/enhanced_workflow.py` | Complete workflow manager |
| `src/responsibility-futures.py` | Original algorithm implementation |
| `src/responsibility-index.py` | Core R = I/N logic |
| `examples/example_usage.py` | Usage demonstrations |

## Theoretical Foundation

### The Solidarity Index
Based on "Stockholm Forgiveness of Responsibility: A Futures Market" (2019). Key concepts from the `docs/` folder:

- **Shorting the Solidarity Index** — When joining a community, an individual borrows trust ("innocent until proven guilty") and aims to buy back into the position through proven reliability
- **Dignity as a Call Option** — Internal threshold of self-worth; the right to exit on your own terms
- **Esteem as a Put Option** — External reputation; the right to cash in on social capital
- **Delta Minimization** — The system rewards predictable behavior aligned with the Hegemonic Standard, not maximum R-scores. Over-performance (martyrdom) is penalized just like under-performance
- **Rationality as Forgiveness** — If behavior can be modeled and hedged, it becomes rationalized and forgivable

### Risk Classification
| R-Ratio Range | Risk Level |
|---------------|------------|
| R > 5.0 | Low Risk |
| 2.0 < R ≤ 5.0 | Moderate Risk |
| R ≤ 2.0 | High Risk |

## Generated Visualizations

1. **Responsibility Matrix Dashboard** — Risk scatter plot, top entities bar chart, risk distribution pie, visibility bubbles
2. **Vector Analysis Heatmaps** — Warm/cold vector patterns per entity
3. **Statistical Summary** — R-ratio distribution, correlation analysis, mention frequency, risk-level box plots
4. **HTML Report** — Responsive, mobile-friendly report with embedded charts

## Integration Ecosystem

- **Upstream:** Cortext.io Event Code Extractor
- **Downstream (planned):** Account Ninja (financial decisions from R-scores), Family RM (governance dashboards), iMASS (manufacturing responsibility metrics)

## Dependencies

```
matplotlib
seaborn
numpy
pandas
```
