#!/usr/bin/env python3.10
"""
Project Crucible — PDF Report Generator
Generates a visual report combining agent-based model context with
NERIS fire incident TAK visualizations for the Crucible Coalition.

Requires: reportlab (pip install reportlab)
"""

import os
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether,
)


# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")


def get_styles():
    """Create custom paragraph styles for the report."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=26,
        textColor=HexColor("#c0392b"),
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        textColor=HexColor("#333333"),
        alignment=TA_CENTER,
        spaceAfter=20,
    ))
    styles.add(ParagraphStyle(
        name="SectionHead",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=HexColor("#1a1a2e"),
        spaceBefore=16,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="SubSectionHead",
        parent=styles["Heading3"],
        fontSize=11,
        leading=14,
        textColor=HexColor("#c0392b"),
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=13,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="Caption",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=HexColor("#555555"),
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="Footer",
        parent=styles["Normal"],
        fontSize=7.5,
        leading=10,
        textColor=HexColor("#666666"),
        alignment=TA_CENTER,
    ))
    return styles


def add_image(story, filename, caption, width=5.5*inch):
    """Add an image with caption to the story, handling missing files gracefully."""
    img_path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(img_path):
        img = Image(img_path, width=width)
        img.hAlign = "CENTER"
        # Maintain aspect ratio
        from reportlab.lib.utils import ImageReader
        ir = ImageReader(img_path)
        iw, ih = ir.getSize()
        aspect = ih / iw
        img._height = width * aspect
        # Cap height to avoid overflow
        max_height = 4.5 * inch
        if img._height > max_height:
            img._height = max_height
            img._width = max_height / aspect
        story.append(img)
    else:
        styles = get_styles()
        story.append(Paragraph(f"<i>[Image not found: {filename}]</i>", styles["Caption"]))
    styles = get_styles()
    story.append(Paragraph(caption, styles["Caption"]))


def build_report():
    """Build the full PDF report."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "Project-Crucible_TAK-Visualization-Report.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )

    styles = get_styles()
    story = []

    # ─── TITLE PAGE ───
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph(
        '<a href="https://richards.plus" color="blue">Richards.plus</a>'
        ' · '
        '<a href="https://riskrunners.com" color="blue">RiskRunners.com</a>',
        styles["ReportSubtitle"],
    ))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Project Crucible", styles["ReportTitle"]))
    story.append(Paragraph(
        "Visualizing Agent-Based Risk Models in TAK<br/>"
        "From Simulation to Situational Awareness",
        styles["ReportSubtitle"],
    ))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        f"Prepared: {date.today().strftime('%B %d, %Y')}<br/>"
        "For: Arizona Captive Insurance Association · Crucible Coalition<br/>"
        'By: Jefferson Richards — <a href="https://richards.plus" color="blue">Richards.plus</a>'
        ' · <a href="https://riskrunners.com" color="blue">RiskRunners.com</a>',
        styles["ReportSubtitle"],
    ))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "<i>\"If the math doesn't fit the problem, fit the problem to the math.\"</i>",
        styles["ReportSubtitle"],
    ))
    story.append(PageBreak())

    # ─── SECTION 1: AGENT-BASED MODELS IN TAK ───
    story.append(Paragraph("1. Agent-Based Models as Tactical Intelligence", styles["SectionHead"]))
    story.append(Paragraph(
        "Agent-based models (ABMs) simulate how autonomous actors — people, vehicles, resources, "
        "risks — interact within an environment according to simple rules. The emergent behavior "
        "of these systems reveals patterns that are invisible at the individual level but critical "
        "for decision-making at the strategic level.",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "The principle is straightforward: <b>if the math doesn't fit the problem, fit the problem "
        "to the math.</b> By categorizing real-world phenomena into modelable patterns — diffusion, "
        "segregation, resource competition, incentive response — we can infer how to resolve "
        "conflicts and allocate resources before they become crises.",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "TAK (Team Awareness Kit) provides the visualization layer that transforms these abstract "
        "models into actionable situational awareness. When an agent-based model's output is "
        "rendered on a geospatial map that operators already use for tactical coordination, "
        "the gap between simulation and decision collapses.",
        styles["BodyText2"],
    ))

    # ─── SUGARSCAPE ───
    story.append(Paragraph("1.1 Sugarscape — Urban Population Distribution", styles["SubSectionHead"]))
    story.append(Paragraph(
        "The Sugarscape model demonstrates how agents competing for a scarce resource (sugar) "
        "naturally distribute themselves into patterns that mirror real urban geography. In the "
        "center — where resources are concentrated — agents cluster and compete intensely. At the "
        "edges, they reach equilibrium and spread out.",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "Applied to Winnipeg's concentric urban structure, this model shows how population density, "
        "resource competition, and spatial equilibrium emerge from simple behavioral rules. The "
        "insurance implication: risk density follows the same concentric pattern. Properties in "
        "high-competition zones face different risk profiles than those at the periphery.",
        styles["BodyText2"],
    ))
    add_image(story, "Sugarscape-Winnipeg-People-Distribution.png",
              "Figure 1: Sugarscape model applied to Winnipeg — agents cluster in resource-rich centers, "
              "spread to equilibrium at edges. Population distribution emerges from simple competition rules.")

    # ─── RECYCLING ───
    story.append(Paragraph("1.2 Recycling — Incentivizing Environmental Remediation", styles["SubSectionHead"]))
    story.append(Paragraph(
        "This agent-based model explores how to incentivize participation in environmental "
        "cleanup projects — specifically, riparian wash remediation inspired by watershed "
        "management nonprofits. Agents respond to incentive structures: when the reward for "
        "collecting and processing waste exceeds the effort cost, participation cascades through "
        "the network.",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "The parallel to fire risk is direct: brush removal services, vegetation management "
        "contractors, and community volunteers all respond to incentive signals. If a captive "
        "insurance model shares underwriting profit with those who reduce fuel loads, the same "
        "cascade effect applies — prevention becomes self-sustaining.",
        styles["BodyText2"],
    ))
    add_image(story, "Recycling-Agent-Based-Model.png",
              "Figure 2: Recycling agent-based model — incentive structures drive participation "
              "in environmental remediation. Applicable to brush removal and fire fuel management.")

    # ─── SEGREGATION ───
    story.append(Paragraph("1.3 Segregation — Redistricting and Risk Boundaries", styles["SubSectionHead"]))
    story.append(Paragraph(
        "Schelling's segregation model demonstrates how mild individual preferences produce "
        "dramatic macro-level separation. Inspired by the recent Virginia redistricting case "
        "that reached the Supreme Court, this visualization shows how boundary-drawing — whether "
        "political districts or insurance coverage zones — creates emergent patterns of inclusion "
        "and exclusion.",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "For fire insurance, the segregation model reveals how coverage withdrawal from one zone "
        "cascades: as carriers exit, remaining properties face higher premiums, driving more "
        "withdrawal, until entire regions become \"uninsurable.\" The captive model breaks this "
        "cycle by creating a self-insuring collective that doesn't flee from risk — it manages it.",
        styles["BodyText2"],
    ))
    add_image(story, "Segregation-Agent-Based-Model.png",
              "Figure 3: Segregation model — mild preferences produce dramatic boundary effects. "
              "Parallels insurance coverage withdrawal patterns in fire-prone regions.")

    story.append(PageBreak())

    # ─── SECTION 2: NERIS FIRE DATA IN iTAK ───
    story.append(Paragraph("2. NERIS Fire Incidents — Proof of Concept in iTAK", styles["SectionHead"]))
    story.append(Paragraph(
        "The agent-based models above establish the theoretical foundation. The NERIS fire "
        "incident visualization demonstrates the <b>operational pipeline</b>: real fire data, "
        "transformed through ISO 31010 risk analysis, rendered as tactical markers in iTAK "
        "that operators can act on immediately.",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "Each fire marker on the map contains a complete risk report — Bow Tie analysis of "
        "preventative and reactive controls, Failure Mode analysis with Risk Priority Numbers, "
        "investment decision modeling, and Markov risk state classification. This is the "
        "minimum viable product for the pipeline:",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "<b>IoT Sensors → NERIS API → ISO 31010 Analysis → TAK Visualization → Decision Makers</b>",
        styles["BodyText2"],
    ))

    # NERIS images
    story.append(Paragraph("2.1 Fire Incident Map — Arizona", styles["SubSectionHead"]))
    add_image(story, "NERIS-fire-incident-1.png",
              "Figure 4: Arizona fire incidents visualized in iTAK. Each marker represents a fire "
              "incident with geolocation from NERIS data. Tap to expand the full risk report.")

    story.append(Paragraph("2.2 Risk Report Details", styles["SubSectionHead"]))
    story.append(Paragraph(
        "When an operator taps a fire marker, the details panel reveals the complete ISO 31010 "
        "risk assessment: Bow Tie control effectiveness, FMEA failure modes ranked by RPN, "
        "and Markov risk classification. This transforms raw incident data into actionable "
        "intelligence for underwriters, fire marshals, and prevention planners.",
        styles["BodyText2"],
    ))
    add_image(story, "NERIS-fire-incident-risk-report.png",
              "Figure 5: Risk report expanded in iTAK — Bow Tie analysis, FMEA failure modes, "
              "and Markov risk classification visible in the marker details panel.")

    story.append(Paragraph("2.3 Investment Decision Modeling", styles["SubSectionHead"]))
    story.append(Paragraph(
        "The decision tree component models the expected value of prevention investment. "
        "While financial parameters are simulated for this proof of concept, the methodology "
        "is sound: compare the expected loss without investment against the cost of investment "
        "plus reduced expected loss. When real property values and historical loss data are "
        "integrated, this becomes a quantitative tool for capital allocation.",
        styles["BodyText2"],
    ))
    add_image(story, "NERIS-fire-incident-investment-decisions.png",
              "Figure 6: Investment decision analysis — simulated financial modeling demonstrates "
              "the decision tree methodology for fire prevention resource allocation.")

    story.append(PageBreak())

    # ─── SECTION 3: VISION ───
    story.append(Paragraph("3. The Apex Vantage Point — From TAK to VisionPro", styles["SectionHead"]))
    story.append(Paragraph(
        "This iTAK proof of concept establishes the data pipeline. The next evolution is "
        "<b>Apex</b> — the VisionPro platform that transforms two-dimensional map markers into "
        "immersive, three-dimensional situational awareness for the stakeholders who need it most:",
        styles["BodyText2"],
    ))

    # Stakeholder table
    stakeholder_data = [
        ["Stakeholder", "Current Pain", "Apex Capability"],
        ["Fire Marshals", "Paper reports, stale data", "Real-time 3D incident overlay with risk scores"],
        ["Insurance Underwriters", "Binary insurable/not decisions", "Gradient risk visualization by zone"],
        ["Real Estate Developers", "Unknown fire exposure", "Pre-development risk assessment in situ"],
        ["Brush Removal Services", "No prioritization data", "Drone-informed fuel load mapping"],
    ]
    table = Table(stakeholder_data, colWidths=[1.6*inch, 2.2*inch, 3.0*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), HexColor("#f5f5f5")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("3.1 The Drone-Augmented Pipeline", styles["SubSectionHead"]))
    story.append(Paragraph(
        "The inference extends naturally: drones flown on regular schedules over fire-prone "
        "corridors provide a continuous video stream that, combined with NERIS incident history "
        "and IoT sensor data, creates a living risk model. From the Apex vantage point — "
        "\"eyes in the sky\" — civic services and the insurance industry can collaboratively:",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "• <b>Remediate</b> — identify and prioritize fuel load reduction zones<br/>"
        "• <b>Mitigate</b> — validate prevention investments with before/after imagery<br/>"
        "• <b>Insure</b> — price risk dynamically based on observed conditions, not stale tables<br/>"
        "• <b>Allocate</b> — direct fire prevention resources to highest-RPN zones first",
        styles["BodyText2"],
    ))

    story.append(Paragraph("3.2 Insuring the Uninsurable", styles["SubSectionHead"]))
    story.append(Paragraph(
        "The complete pipeline — from IoT sensors through NERIS data through ISO 31010 analysis "
        "through TAK/Apex visualization — achieves what the standard market cannot: it makes "
        "previously uninsurable fire-risk properties insurable by replacing binary classification "
        "with continuous, evidence-based risk scoring that rewards prevention.",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "Just as Medical Stop-Loss captives transformed employers from passive premium payers "
        "into active health optimizers, this pipeline transforms property owners and communities "
        "from passive fire victims into active risk managers — with the financial incentive of "
        "keeping the underwriting profit when prevention works.",
        styles["BodyText2"],
    ))

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "═══════════════════════════════════════════════════════════",
        styles["Footer"],
    ))
    story.append(Paragraph(
        'Project Crucible · <a href="https://richards.plus" color="blue">Richards.plus</a>'
        ' · <a href="https://riskrunners.com" color="blue">RiskRunners.com</a><br/>'
        "jefferson@richards.plus · 520.981.3639",
        styles["Footer"],
    ))

    # Build PDF
    doc.build(story)
    print(f"[+] PDF report generated: {output_path}")
    print(f"    Size: {os.path.getsize(output_path) / 1024:.1f} KB")
    return output_path


if __name__ == "__main__":
    print("=" * 60)
    print("  PROJECT CRUCIBLE — PDF Report Generator")
    print("=" * 60)
    print()
    build_report()
