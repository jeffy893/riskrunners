# Responsibility Futures Engine - [Cortext.io](https://cortext.io) Integration

> **"Quantifying responsibility through AI-extracted event analysis"** - Converting Cortext.io Event Code data into actionable Responsibility Ratios with rich visualizations.

A Python implementation of the **Responsibility Futures** algorithm that processes [Cortext.io Event Code Extractor](https://github.com/jeffy893/cortext.io) JSON reports to calculate **Responsibility Ratios (R = I/N)** for entities mentioned in extracted events, complete with **HTML reports** and **PNG visualizations**.

## 🎨 New: Enhanced Reporting & Visualizations

The engine now generates comprehensive **HTML reports** and **PNG visualizations** that provide:

- 📊 **Interactive Dashboard**: Responsibility matrix with risk assessment scatter plots
- 🌡️ **Vector Analysis**: Warm/cold vector heatmaps for intention/negligence patterns  
- 📈 **Statistical Summaries**: Distribution analysis and correlation insights
- 🏆 **Entity Rankings**: Top performers with detailed metrics tables
- 📱 **Responsive Design**: Mobile-friendly reports with modern styling

### Quick Start - Enhanced Workflow

```bash
# Run complete analysis with visualizations (easiest)
./run_analysis.sh

# Or run manually
python src/enhanced_workflow.py

# Process specific file
python src/enhanced_workflow.py --input /path/to/extraction_file.json

# List available reports
python src/enhanced_workflow.py --list
```

## 🔗 Integration with Cortext.io

This engine serves as the **downstream analytics layer** for Cortext.io's Event Code Extractor:

1. **Cortext.io** extracts events, entities, and sentiment vectors from natural language text
2. **Responsibility Futures Engine** processes the JSON output to calculate responsibility metrics
3. **Enhanced Report Generator** creates rich HTML reports and PNG visualizations
4. **Account Ninja** (future integration) uses R-scores for financial and social capital assessment

### Data Flow Pipeline

```
Text Input → Cortext.io NLP → JSON Events → Responsibility Engine → HTML Reports + PNG Charts
```

## 📖 The Core Philosophy

The algorithm quantifies responsibility using the principle that **responsibility is measurable** through the relationship between **Intention (I)** and **Negligence (N)**:

$\text{RESPONSIBILITY} (R) = \frac{\text{INTENTION} (I)}{\text{NEGLIGENCE} (N)}$

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

### 4. Enhanced Visualization Generation
- **Responsibility Matrix**: Multi-panel dashboard with scatter plots, bar charts, and pie charts
- **Vector Analysis**: Heatmaps showing warm/cold vector patterns for top entities
- **Statistical Summary**: Distribution analysis, correlations, and box plots
- **HTML Report**: Comprehensive report with embedded visualizations and methodology

## 🚀 Usage

### Enhanced Workflow (Recommended)

```bash
# Complete workflow with HTML reports and PNG visualizations
./run_analysis.sh

# Windows users
run_analysis.bat

# Manual execution
python src/enhanced_workflow.py
```

### Individual Components

```bash
# Step 1: Process Cortext.io report
python src/cortext_integration.py /path/to/cortext_report.json

# Step 2: Generate HTML report and PNG visualizations
python src/report_generator.py /path/to/responsibility_analysis.json
```

### Programmatic Usage

```python
from src.cortext_integration import CortextResponsibilityEngine
from src.report_generator import ResponsibilityReportGenerator

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

# Generate enhanced visualizations
generator = ResponsibilityReportGenerator('responsibility_analysis.json')
generated_files = generator.generate_all_reports()
```

### Example Output

```
🚀 Starting Enhanced Responsibility Futures Workflow
============================================================
📄 Found latest Cortext.io report: extraction_20251230_082034.json
🔬 Running responsibility analysis...
✅ Responsibility analysis completed

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

🎨 Generating responsibility matrix visualization...
🌡️ Generating vector analysis visualization...
📈 Generating statistical summary...
📄 Generating HTML report...

✅ Report generation completed successfully!
📋 Generated files:
   • html_report: responsibility_report_20251230_143022.html
   • matrix_plot: responsibility_matrix_20251230_143022.png
   • vector_plot: vector_analysis_20251230_143022.png
   • stats_plot: statistical_summary_20251230_143022.png

🌐 View the complete report:
   file:///path/to/responsibility_report_20251230_143022.html
```

## 📂 Project Structure

```
responsibility-futures/
├── src/
│   ├── cortext_integration.py    # Main integration engine
│   ├── report_generator.py       # NEW: HTML/PNG report generator
│   ├── enhanced_workflow.py      # NEW: Complete workflow manager
│   ├── responsibility-futures.py # Original algorithm
│   └── responsibility-index.py   # Core logic implementation
├── output/                       # NEW: Generated reports directory
├── examples/
│   └── example_usage.py         # Usage demonstrations
├── docs/
│   ├── 2019-10-31_Responsibility-Futures.pdf
│   └── 2025-12-06_Responsibility-Future_on_Solidarity.md
├── run_analysis.sh              # NEW: Easy execution script (Unix)
├── run_analysis.bat             # NEW: Easy execution script (Windows)
└── requirements.txt             # Updated with visualization dependencies
```

## 📊 Generated Visualizations

### 1. Responsibility Matrix Dashboard
- **Risk Assessment Scatter Plot**: Intention vs Negligence with risk level coloring
- **Top Entities Bar Chart**: Horizontal bars showing highest responsibility ratios
- **Risk Distribution Pie Chart**: Breakdown of entities by risk level
- **Visibility Bubble Chart**: Mentions vs R-ratio with intention score sizing

### 2. Vector Analysis Heatmaps
- **Warm Vectors**: Positivity, Engagement, Optimism patterns for top entities
- **Cold Vectors**: Negativity, Risk, Uncertainty indicators with color coding

### 3. Statistical Summary
- **R-Ratio Distribution**: Histogram with mean/median indicators
- **Correlation Analysis**: Intention vs Negligence scatter with correlation coefficient
- **Mention Distribution**: Frequency analysis of entity visibility
- **Risk Level Box Plots**: Score distributions segmented by risk categories

### 4. HTML Report Features
- **Responsive Design**: Mobile-friendly layout with modern CSS
- **Interactive Elements**: Hover effects and smooth transitions
- **Comprehensive Tables**: Top 20 entities with detailed metrics
- **Methodology Section**: Clear explanation of calculations and risk levels
- **Summary Statistics**: Key metrics dashboard with visual cards

## 🔄 Integration Ecosystem

### Current Integration
- **Input**: Cortext.io JSON reports with extracted events and sentiment vectors
- **Processing**: Responsibility Futures algorithm with warm/cold vector analysis
- **Visualization**: HTML reports with embedded PNG charts and interactive elements
- **Output**: Entity responsibility assessments, risk classifications, and visual analytics

### Future Integrations
- **Account Ninja**: Financial decision-making based on R-scores
- **Family RM**: Governance dashboards with responsibility tracking
- **iMASS Ecosystem**: Manufacturing and shared services responsibility metrics

## 🎯 Use Cases with Enhanced Reporting

### 1. Political Risk Assessment
- Process news articles through Cortext.io
- Generate visual responsibility dashboards for political figures
- Track reputation trends with statistical analysis
- Share professional HTML reports with stakeholders

### 2. Corporate Governance
- Analyze 10-K filings and earnings calls via Cortext.io
- Create executive responsibility scorecards with visualizations
- Support ESG reporting with comprehensive analytics
- Generate board-ready presentations

### 3. Social Media Analysis
- Extract events from social media content using Cortext.io
- Visualize responsibility patterns for public figures
- Monitor reputation shifts with trend analysis
- Create shareable infographic-style reports

### 4. Contract and Partnership Evaluation
- Process legal documents and communications through Cortext.io
- Generate visual responsibility profiles for potential partners
- Support due diligence with comprehensive risk assessment dashboards
- Create professional reports for investment committees

## 📊 Technical Advantages

- **Rich Visualizations**: Professional-grade charts using matplotlib and seaborn
- **Responsive HTML**: Mobile-friendly reports with modern design
- **Zero External Dependencies**: Core functionality remains dependency-free
- **Cortext.io Native**: Designed specifically for Cortext.io JSON format
- **Scalable Processing**: Handles large event datasets efficiently
- **Risk Classification**: Automatic risk level assignment with visual indicators
- **Comprehensive Output**: Detailed reports with embedded analytics and methodology

## 🔬 Research Foundation

Based on "Stockholm Forgiveness of Responsibility: A Futures Market" (2019) and integrated with modern NLP event extraction through Cortext.io's Event Code framework, now enhanced with professional data visualization and reporting capabilities.

---

**Ready to quantify responsibility with rich visualizations?** Process your first Cortext.io report and discover the responsibility patterns hidden in your text data through interactive dashboards and comprehensive analytics.