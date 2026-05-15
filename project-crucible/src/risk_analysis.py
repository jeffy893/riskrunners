"""
Project Crucible — ISO 31010 Risk Analysis
Implements Bow Tie, FMEA, Decision Tree, and Markov risk classification
for fire incident data from the NERIS API.
"""

from typing import Optional


def bow_tie_analysis(incident: dict) -> dict:
    """
    Perform a Bow Tie Analysis (ISO 31010 B.4.2) on a single incident.

    Evaluates preventative controls (left side) and reactive controls (right side)
    around the fire loss event.

    Returns:
        Dict with preventative_controls and reactive_controls effectiveness ratings.
    """
    # Evaluate preventative controls
    preventative = {}

    # Smoke detector effectiveness
    smoke_alarm = incident.get("smoke_alarm", {})
    alarm_status = smoke_alarm.get("status", "undetermined")
    if alarm_status == "present_operated":
        preventative["smoke_detector"] = {"present": True, "operated": True, "effectiveness": "HIGH"}
    elif alarm_status == "present_did_not_operate":
        preventative["smoke_detector"] = {"present": True, "operated": False, "effectiveness": "LOW"}
    elif alarm_status == "not_present":
        preventative["smoke_detector"] = {"present": False, "operated": False, "effectiveness": "NONE"}
    else:
        preventative["smoke_detector"] = {"present": None, "operated": None, "effectiveness": "UNDETERMINED"}

    # Fire alarm system
    fire_alarm = incident.get("fire_alarm", {})
    if fire_alarm.get("present") and fire_alarm.get("operated"):
        preventative["fire_alarm"] = {"effectiveness": "HIGH"}
    elif fire_alarm.get("present") and not fire_alarm.get("operated"):
        preventative["fire_alarm"] = {"effectiveness": "LOW"}
    else:
        preventative["fire_alarm"] = {"effectiveness": "NONE"}

    # Building code compliance (inferred from suppression presence)
    suppression = incident.get("fire_suppression") or {}
    if suppression.get("performance") == "operated_effectively":
        preventative["building_codes"] = {"effectiveness": "HIGH"}
    elif suppression.get("performance") == "failed":
        preventative["building_codes"] = {"effectiveness": "LOW"}
    elif suppression.get("performance") == "not_present":
        preventative["building_codes"] = {"effectiveness": "MODERATE"}
    else:
        preventative["building_codes"] = {"effectiveness": "UNDETERMINED"}

    # Evaluate reactive controls
    reactive = {}

    # Fire department response time
    dispatch = incident.get("dispatch", {})
    response_time = dispatch.get("response_time_minutes", 0)
    if response_time > 0:
        if response_time <= 5:
            reactive["fd_response"] = {"minutes": response_time, "effectiveness": "HIGH"}
        elif response_time <= 8:
            reactive["fd_response"] = {"minutes": response_time, "effectiveness": "MODERATE"}
        else:
            reactive["fd_response"] = {"minutes": response_time, "effectiveness": "LOW"}
    else:
        reactive["fd_response"] = {"minutes": None, "effectiveness": "UNDETERMINED"}

    # Suppression system as reactive control
    if suppression.get("performance") == "operated_effectively":
        reactive["suppression_system"] = {"effectiveness": "HIGH"}
    elif suppression.get("performance") == "failed":
        reactive["suppression_system"] = {"effectiveness": "FAILED"}
    else:
        reactive["suppression_system"] = {"effectiveness": "NOT_AVAILABLE"}

    # Unit response depth (mutual aid)
    unit_responses = dispatch.get("unit_responses", [])
    if len(unit_responses) >= 4:
        reactive["mutual_aid"] = {"units": len(unit_responses), "effectiveness": "HIGH"}
    elif len(unit_responses) >= 2:
        reactive["mutual_aid"] = {"units": len(unit_responses), "effectiveness": "MODERATE"}
    else:
        reactive["mutual_aid"] = {"units": len(unit_responses), "effectiveness": "LOW"}

    # Calculate overall effectiveness scores
    prev_scores = {"HIGH": 3, "MODERATE": 2, "LOW": 1, "NONE": 0, "UNDETERMINED": 1}
    react_scores = {"HIGH": 3, "MODERATE": 2, "LOW": 1, "FAILED": 0, "NOT_AVAILABLE": 0, "UNDETERMINED": 1}

    prev_total = sum(prev_scores.get(c.get("effectiveness", "UNDETERMINED"), 1) for c in preventative.values())
    prev_max = len(preventative) * 3
    prev_pct = (prev_total / prev_max * 100) if prev_max > 0 else 0

    react_total = sum(react_scores.get(c.get("effectiveness", "UNDETERMINED"), 1) for c in reactive.values())
    react_max = len(reactive) * 3
    react_pct = (react_total / react_max * 100) if react_max > 0 else 0

    if prev_pct >= 66:
        prev_overall = "HIGH"
    elif prev_pct >= 33:
        prev_overall = "MODERATE"
    else:
        prev_overall = "LOW"

    if react_pct >= 66:
        react_overall = "HIGH"
    elif react_pct >= 33:
        react_overall = "MODERATE"
    else:
        react_overall = "LOW"

    return {
        "threat": _get_incident_type_label(incident),
        "preventative_controls": preventative,
        "preventative_overall": prev_overall,
        "reactive_controls": reactive,
        "reactive_overall": react_overall,
    }


def fmea_analysis(incident: dict) -> list:
    """
    Perform Failure Mode & Effects Analysis on a single incident.

    Calculates Risk Priority Numbers (RPN = Severity × Occurrence × Detection)
    for relevant failure modes based on incident data.

    Returns:
        List of failure mode dicts sorted by RPN descending.
    """
    failure_modes = []

    fire_detail = incident.get("fire_detail", {})
    suppression = incident.get("fire_suppression") or {}
    dispatch = incident.get("dispatch", {})
    smoke_alarm = incident.get("smoke_alarm", {})
    weather = incident.get("weather", {})

    # 1. Suppression system failure
    severity = 9
    if suppression.get("performance") == "failed":
        occurrence = 8
    elif suppression.get("performance") == "not_present":
        occurrence = 6
    elif suppression.get("performance") == "operated_effectively":
        occurrence = 2
    else:
        occurrence = 5
    detection = 4  # Periodic inspections
    failure_modes.append({
        "mode": "Suppression system failure",
        "cause": "Maintenance lapse or system absence",
        "effect": "Uncontrolled fire spread",
        "severity": severity,
        "occurrence": occurrence,
        "detection": detection,
        "rpn": severity * occurrence * detection,
    })

    # 2. Delayed dispatch / response
    response_time = dispatch.get("response_time_minutes", 8)
    severity = 7
    if response_time > 12:
        occurrence = 7
    elif response_time > 8:
        occurrence = 5
    elif response_time > 5:
        occurrence = 3
    else:
        occurrence = 2
    detection = 3  # CAD systems provide tracking
    failure_modes.append({
        "mode": "Delayed emergency response",
        "cause": "Distance, traffic, or dispatch delay",
        "effect": "Extended fire duration and spread",
        "severity": severity,
        "occurrence": occurrence,
        "detection": detection,
        "rpn": severity * occurrence * detection,
    })

    # 3. Detection failure (smoke alarm)
    severity = 8
    if smoke_alarm.get("status") == "not_present":
        occurrence = 7
    elif smoke_alarm.get("status") == "present_did_not_operate":
        occurrence = 6
    elif smoke_alarm.get("status") == "present_operated":
        occurrence = 2
    else:
        occurrence = 5
    detection = 5  # Occupant awareness varies
    failure_modes.append({
        "mode": "Fire detection failure",
        "cause": "Missing or malfunctioning smoke alarm",
        "effect": "Delayed occupant notification and evacuation",
        "severity": severity,
        "occurrence": occurrence,
        "detection": detection,
        "rpn": severity * occurrence * detection,
    })

    # 4. Weather-driven fire spread (Arizona-specific)
    wind_speed = weather.get("wind_speed_mph", 10)
    humidity = weather.get("humidity_pct", 20)
    severity = 8
    if wind_speed > 25 and humidity < 15:
        occurrence = 8
    elif wind_speed > 15 or humidity < 20:
        occurrence = 5
    else:
        occurrence = 3
    detection = 6  # Weather monitoring exists but fire behavior is unpredictable
    failure_modes.append({
        "mode": "Weather-accelerated spread",
        "cause": "High winds and low humidity",
        "effect": "Rapid fire growth beyond initial containment",
        "severity": severity,
        "occurrence": occurrence,
        "detection": detection,
        "rpn": severity * occurrence * detection,
    })

    # 5. Electrical ignition
    severity = 8
    if fire_detail.get("heat_source") == "electrical":
        occurrence = 7
    else:
        occurrence = 4
    detection = 5  # Inspections are periodic
    failure_modes.append({
        "mode": "Electrical ignition source",
        "cause": "Aging infrastructure or overloaded circuits",
        "effect": "Fire initiation in concealed spaces",
        "severity": severity,
        "occurrence": occurrence,
        "detection": detection,
        "rpn": severity * occurrence * detection,
    })

    # Sort by RPN descending
    failure_modes.sort(key=lambda x: x["rpn"], reverse=True)
    return failure_modes


def decision_tree_analysis(incident: dict) -> dict:
    """
    Decision Tree Analysis (ISO 31010 B.9.3) for fire prevention investment.

    Uses SIMULATED financial data to demonstrate the methodology.
    All dollar amounts are for demonstration purposes only.

    Returns:
        Dict with investment recommendation and expected values.
    """
    # SIMULATED financial parameters (clearly marked)
    fire_detail = incident.get("fire_detail", {})
    property_loss = fire_detail.get("property_loss_dollars", 250000)

    # Base investment cost varies by incident type
    incident_type = _get_incident_type(incident)
    if incident_type in ("structure_fire", "electrical_fire"):
        investment_cost = 50000
    elif incident_type == "wildfire":
        investment_cost = 75000
    else:
        investment_cost = 30000

    # Estimate fire probability based on incident characteristics
    dispatch = incident.get("dispatch", {})
    response_time = dispatch.get("response_time_minutes", 8)
    suppression = incident.get("fire_suppression") or {}

    # Base probability (simulated)
    p_fire_no_invest = 0.15

    # Adjust based on response time (longer response = higher risk)
    if response_time > 10:
        p_fire_no_invest += 0.05
    elif response_time < 5:
        p_fire_no_invest -= 0.03

    # Adjust based on suppression presence
    if suppression.get("performance") == "not_present":
        p_fire_no_invest += 0.05

    p_fire_no_invest = max(0.05, min(0.40, p_fire_no_invest))

    # Investment reduces probability by 40-60% (literature-based estimate)
    reduction_factor = 0.55
    p_fire_with_invest = p_fire_no_invest * (1 - reduction_factor)

    # Calculate expected values
    ev_no_invest = -(p_fire_no_invest * property_loss)
    ev_invest = -investment_cost - (p_fire_with_invest * property_loss)

    annual_savings = ev_no_invest - ev_invest  # Positive means investing saves money

    recommendation = "INVEST" if annual_savings > 0 else "DO NOT INVEST"

    return {
        "simulated": True,
        "disclaimer": "SIMULATED — for demonstration purposes",
        "investment_cost": investment_cost,
        "p_fire_no_investment": round(p_fire_no_invest, 3),
        "p_fire_with_investment": round(p_fire_with_invest, 3),
        "avg_loss_estimate": property_loss,
        "ev_no_invest": round(ev_no_invest, 2),
        "ev_invest": round(ev_invest, 2),
        "annual_savings": round(annual_savings, 2),
        "recommendation": recommendation,
    }


def markov_risk_state(incident: dict) -> dict:
    """
    Markov State Classification for incident location risk level.

    Classifies the incident location as LOW, MODERATE, or HIGH risk
    based on available incident data indicators.

    States: LOW → MODERATE → HIGH (with transitions based on data)

    Returns:
        Dict with current risk state and contributing factors.
    """
    # Score accumulator (higher = higher risk)
    risk_score = 0
    factors = []

    # Factor 1: Response time
    dispatch = incident.get("dispatch", {})
    response_time = dispatch.get("response_time_minutes", 8)
    if response_time > 10:
        risk_score += 3
        factors.append(f"Slow response time ({response_time:.1f} min)")
    elif response_time > 7:
        risk_score += 2
        factors.append(f"Moderate response time ({response_time:.1f} min)")
    else:
        risk_score += 1

    # Factor 2: Suppression system status
    suppression = incident.get("fire_suppression") or {}
    if suppression.get("performance") == "failed":
        risk_score += 3
        factors.append("Suppression system failed")
    elif suppression.get("performance") == "not_present":
        risk_score += 2
        factors.append("No suppression system present")
    elif suppression.get("performance") == "operated_effectively":
        risk_score += 0
    else:
        risk_score += 1

    # Factor 3: Smoke alarm status
    smoke_alarm = incident.get("smoke_alarm", {})
    if smoke_alarm.get("status") == "not_present":
        risk_score += 2
        factors.append("No smoke alarm present")
    elif smoke_alarm.get("status") == "present_did_not_operate":
        risk_score += 2
        factors.append("Smoke alarm present but did not operate")
    elif smoke_alarm.get("status") == "present_operated":
        risk_score += 0

    # Factor 4: Property loss severity
    fire_detail = incident.get("fire_detail", {})
    loss = fire_detail.get("property_loss_dollars", 0)
    if loss > 500000:
        risk_score += 3
        factors.append(f"High property loss (${loss:,.0f})")
    elif loss > 100000:
        risk_score += 2
        factors.append(f"Moderate property loss (${loss:,.0f})")
    else:
        risk_score += 1

    # Factor 5: Fire spread extent
    spread = fire_detail.get("fire_spread", "")
    if spread == "beyond_building":
        risk_score += 3
        factors.append("Fire spread beyond building")
    elif spread == "confined_to_building":
        risk_score += 2
    elif spread in ("confined_to_floor", "confined_to_room"):
        risk_score += 1

    # Factor 6: Weather conditions (Arizona-specific)
    weather = incident.get("weather", {})
    if weather.get("wind_speed_mph", 0) > 20 and weather.get("humidity_pct", 50) < 15:
        risk_score += 2
        factors.append("Extreme fire weather conditions")
    elif weather.get("temperature_f", 70) > 100 and weather.get("humidity_pct", 50) < 20:
        risk_score += 1
        factors.append("Hot/dry conditions")

    # Classify into Markov states
    max_possible = 16  # Maximum risk score
    normalized = risk_score / max_possible

    if normalized >= 0.6:
        state = "HIGH"
    elif normalized >= 0.35:
        state = "MODERATE"
    else:
        state = "LOW"

    return {
        "state": state,
        "risk_score": risk_score,
        "max_score": max_possible,
        "normalized_score": round(normalized, 3),
        "contributing_factors": factors,
    }


def generate_risk_report(incident: dict) -> str:
    """
    Generate a complete HTML risk report for a single incident.

    Combines Bow Tie, FMEA, Decision Tree, and Markov analyses into
    a formatted HTML string suitable for embedding in KML descriptions.
    iTAK renders this HTML when a user taps on a map marker.

    Returns:
        HTML string with the full risk report.
    """
    # Run all analyses
    bow_tie = bow_tie_analysis(incident)
    fmea = fmea_analysis(incident)
    decision = decision_tree_analysis(incident)
    markov = markov_risk_state(incident)

    # Extract incident metadata
    incident_type = _get_incident_type_label(incident)
    dispatch = incident.get("dispatch", {})
    location_city = dispatch.get("location", {}).get("city", "Unknown")
    dispatch_date = dispatch.get("timestamp", "Unknown")
    if dispatch_date != "Unknown":
        dispatch_date = dispatch_date[:10]  # Just the date portion

    # Build HTML report
    html_parts = []

    html_parts.append(f'<h3>Fire Risk Report &mdash; {location_city}</h3>')
    html_parts.append(f'<p><b>Incident:</b> {incident_type} | <b>Date:</b> {dispatch_date}</p>')
    html_parts.append('<hr/>')

    # Bow Tie section
    html_parts.append('<h4>Bow Tie Analysis</h4>')
    html_parts.append(f'<p>Preventative Controls: {bow_tie["preventative_overall"]}</p>')
    html_parts.append(f'<p>Reactive Controls: {bow_tie["reactive_overall"]}</p>')

    # Detail preventative controls
    prev_details = []
    for name, ctrl in bow_tie["preventative_controls"].items():
        eff = ctrl.get("effectiveness", "N/A")
        prev_details.append(f"{_format_control_name(name)}: {eff}")
    if prev_details:
        html_parts.append(f'<p><small>{" | ".join(prev_details)}</small></p>')

    html_parts.append('<hr/>')

    # FMEA section (top 3)
    html_parts.append('<h4>Failure Mode Analysis (Top 3)</h4>')
    html_parts.append('<ul>')
    for fm in fmea[:3]:
        html_parts.append(
            f'<li>{fm["mode"]}: RPN={fm["rpn"]} '
            f'(S={fm["severity"]} × O={fm["occurrence"]} × D={fm["detection"]})</li>'
        )
    html_parts.append('</ul>')
    html_parts.append('<hr/>')

    # Decision Tree section
    html_parts.append('<h4>Investment Decision (Simulated)</h4>')
    html_parts.append(f'<p><em>{decision["disclaimer"]}</em></p>')
    html_parts.append(f'<p>Recommendation: <b>{decision["recommendation"]}</b></p>')
    html_parts.append(f'<p>Expected Annual Savings: ${decision["annual_savings"]:,.0f}</p>')
    html_parts.append(
        f'<p><small>Investment: ${decision["investment_cost"]:,.0f} | '
        f'P(fire) without: {decision["p_fire_no_investment"]:.1%} | '
        f'P(fire) with: {decision["p_fire_with_investment"]:.1%}</small></p>'
    )
    html_parts.append('<hr/>')

    # Markov Risk Classification
    html_parts.append('<h4>Risk Classification</h4>')
    html_parts.append(f'<p>Current State: <b>{markov["state"]}</b> '
                      f'(score: {markov["risk_score"]}/{markov["max_score"]})</p>')
    if markov["contributing_factors"]:
        html_parts.append('<p><small>Factors: ' + '; '.join(markov["contributing_factors"]) + '</small></p>')

    html_parts.append('<hr/>')
    html_parts.append('<p><small><em>Generated by Project Crucible | ISO 31010 Risk Assessment</em></small></p>')

    return '\n'.join(html_parts)


# --- Helper functions ---

def _get_incident_type(incident: dict) -> str:
    """Extract the primary incident type string."""
    types = incident.get("incident_types", [])
    return types[0] if types else "unknown"


def _get_incident_type_label(incident: dict) -> str:
    """Get a human-readable label for the incident type."""
    type_str = _get_incident_type(incident)
    labels = {
        "structure_fire": "Structure Fire",
        "wildfire": "Wildfire",
        "vehicle_fire": "Vehicle Fire",
        "cooking_fire": "Cooking Fire",
        "electrical_fire": "Electrical Fire",
        "brush_fire": "Brush Fire",
        "dumpster_fire": "Dumpster Fire",
        "chimney_fire": "Chimney Fire",
    }
    return labels.get(type_str, type_str.replace("_", " ").title())


def _format_control_name(name: str) -> str:
    """Format a control name for display."""
    return name.replace("_", " ").title()
