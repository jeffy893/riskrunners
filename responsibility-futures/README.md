# Responsibility Futures Engine - Cortext.io Integration

> **"Quantifying responsibility through AI-extracted event analysis"** - Converting Cortext.io Event Code data into actionable Responsibility Ratios.

A Python implementation of the **Responsibility Futures** algorithm that processes [Cortext.io Event Code Extractor](https://github.com/jeffy893/cortext.io) JSON reports to calculate **Responsibility Ratios (R = I/N)** for entities mentioned in extracted events.

## 🔗 Integration with Cortext.io

This engine serves as the **downstream analytics layer** for Cortext.io's Event Code Extractor:

1. **Cortext.io** extracts events, entities, and sentiment vectors from natural language text
2. **Responsibility Futures Engine** processes the JSON output to calculate responsibility metrics
3. **Account Ninja** (future integration) uses R-scores for financial and social capital assessment

### Data Flow Pipeline

```
Text Input → Cortext.io NLP → JSON Events → Responsibility Engine → R-Score Dashboard
```

## 📖 The Core Philosophy

The algorithm quantifies responsibility using the principle that **responsibility is measurable** through the relationship between **Intention (I)** and **Negligence (N)**:

$$\text{RESPONSIBILITY} (R) = \frac{\text{INTENTION} (I)}{\text{NEGLIGENCE} (N)}$$

### Cortext.io Vector Mapping

- **Intention (I)**: Derived from **warm vectors** (Positivity, Engagement, Optimism)
- **Negligence (N)**: Derived from **cold vectors** (Negativity, Risk, Uncertainty)

This creates a **quantifiable social credit system** that moves beyond traditional FICO scores to measure "social and scope capital."

## ⚙️ How It Works with Cortext.io

### 1. Input Processing
The engine accepts Cortext.io JSON reports containing:
- **Sentences** with warm/cold sentiment vectors
- **Subjects** (extracted entities)
- **Phenomena** (extracted concepts)
- **Timestamps** and metadata

### 2. Entity Analysis
For each entity mentioned in the events:
- **Mention frequency** across all sentences
- **Average warm vector** (intention indicators)
- **Average cold vector** (negligence indicators)
- **Contextual concepts** associated with the entity

### 3. Responsibility Calculation
- **Intention Score**: Weighted sum of warm vectors (Positivity×0.4 + Engagement×0.4 + Optimism×0.2)
- **Negligence Score**: Weighted sum of cold vectors (Negativity×0.5 + Risk×0.3 + Uncertainty×0.2)
- **R-Ratio**: I/N with risk level classification

## 🚀 Usage

### Basic Integration

```bash
# Process a Cortext.io report
python src/cortext_integration.py /path/to/cortext_report.json
```

### Programmatic Usage

```python
from src.cortext_integration import CortextResponsibilityEngine

# Initialize engine
engine = CortextResponsibilityEngine()

# Load Cortext.io report
cortext_data = engine.load_cortext_report('extraction_20251230_082034.json')
engine.extract_entities_and_events(cortext_data)

# Calculate responsibility for specific entity
trump_assessment = engine.calculate_responsibility_ratio('Trump')
print(f"Trump R-Score: {trump_assessment['responsibility_ratio']}")

# Generate full report
report = engine.generate_responsibility_report()
```

### Example Output

```
RESPONSIBILITY FUTURES ANALYSIS
Powered by Cortext.io Event Code Extractor
============================================================
Analysis Date: 2025-12-30T08:20:14.596619
Total Entities: 95
Total Events: 24

TOP RESPONSIBILITY RATIOS:
------------------------------------------------------------
 1. Netanyahu           R=  8.45 (Low)      [12 mentions]
 2. Israel              R=  6.23 (Low)      [18 mentions]
 3. Trump               R=  4.12 (Moderate) [15 mentions]
 4. Hamas               R=  2.87 (Moderate) [8 mentions]
 5. Iran                R=  1.94 (High)     [9 mentions]
```

## 📂 Project Structure

```
responsibility-futures/
├── src/
│   ├── cortext_integration.py    # Main integration engine
│   ├── responsibility-futures.py # Original algorithm
│   └── responsibility-index.py   # Core logic implementation
├── examples/
│   └── example_usage.py         # Usage demonstrations
├── docs/
│   ├── 2019-10-31_Responsibility-Futures.pdf
│   └── 2025-12-06_Responsibility-Future_on_Solidarity.md
└── requirements.txt             # Dependencies
```

## 🔄 Integration Ecosystem

### Current Integration
- **Input**: Cortext.io JSON reports with extracted events and sentiment vectors
- **Processing**: Responsibility Futures algorithm with warm/cold vector analysis
- **Output**: Entity responsibility assessments and risk classifications

### Future Integrations
- **Account Ninja**: Financial decision-making based on R-scores
- **Family RM**: Governance dashboards with responsibility tracking
- **iMASS Ecosystem**: Manufacturing and shared services responsibility metrics

## 🎯 Use Cases with Cortext.io

### 1. Political Risk Assessment
- Process news articles through Cortext.io
- Calculate responsibility ratios for political figures
- Track reputation and reliability over time

### 2. Corporate Governance
- Analyze 10-K filings and earnings calls via Cortext.io
- Generate responsibility scores for executives and companies
- Support ESG and compliance monitoring

### 3. Social Media Analysis
- Extract events from social media content using Cortext.io
- Calculate responsibility metrics for public figures
- Monitor reputation and influence patterns

### 4. Contract and Partnership Evaluation
- Process legal documents and communications through Cortext.io
- Generate responsibility profiles for potential partners
- Support due diligence and risk assessment

## 📊 Technical Advantages

- **Zero External Dependencies**: Pure Python implementation
- **Cortext.io Native**: Designed specifically for Cortext.io JSON format
- **Scalable Processing**: Handles large event datasets efficiently
- **Risk Classification**: Automatic risk level assignment based on R-ratios
- **Comprehensive Output**: Detailed JSON reports with entity assessments

## 🔬 Research Foundation

Based on "Stockholm Forgiveness of Responsibility: A Futures Market" (2019) and integrated with modern NLP event extraction through Cortext.io's Event Code framework.

---

**Ready to quantify responsibility?** Process your first Cortext.io report and discover the responsibility patterns hidden in your text data.