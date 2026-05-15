"""
Project Crucible — CoT Data Package Export for iTAK
Generates a TAK Data Package (.zip) containing CoT events that iTAK
natively displays with full remarks/details when markers are tapped.

CoT (Cursor on Target) is the native message format for TAK applications.
Each fire incident becomes a CoT event with:
  - Geolocation (point)
  - Callsign (incident name)
  - Remarks (full risk report text — visible in iTAK details panel)
  - Type (atom for hostile/friendly/neutral markers)
  - Color coding by incident type
"""

import os
import uuid
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from risk_analysis import generate_risk_report


# CoT type codes for different incident types
# Using "a-h-G" (hostile ground) for all fires — shows as hostile markers (red/diamond)
# The "b-m-p-s-m" type is the MIL-STD-2525 symbol for fire
# Using "b-m-p-s-m--fi" for fire symbol in TAK
COT_TYPE_MAP = {
    "structure_fire": "b-m-p-s-m--fi",
    "wildfire": "b-m-p-s-m--fi",
    "vehicle_fire": "b-m-p-s-m--fi",
    "cooking_fire": "b-m-p-s-m--fi",
    "electrical_fire": "b-m-p-s-m--fi",
    "brush_fire": "b-m-p-s-m--fi",
    "dumpster_fire": "b-m-p-s-m--fi",
    "chimney_fire": "b-m-p-s-m--fi",
}

# ARGB color values for CoT markers — all red/orange for fire
COT_COLOR_MAP = {
    "structure_fire": "-65536",       # Red
    "wildfire": "-33024",             # Orange-red
    "vehicle_fire": "-65536",         # Red
    "cooking_fire": "-65536",         # Red
    "electrical_fire": "-65536",      # Red
    "brush_fire": "-33024",           # Orange-red
    "dumpster_fire": "-65536",        # Red
    "chimney_fire": "-65536",         # Red
}


def _get_incident_type(incident: dict) -> str:
    """Extract primary incident type from incident data."""
    types = incident.get("incident_types", [])
    return types[0] if types else "unknown"


def _get_coordinates(incident: dict) -> tuple:
    """Extract (lat, lon) coordinates from incident GeoJSON point."""
    base = incident.get("base", {})
    point = base.get("point", {})
    geometry = point.get("geometry", {})
    coords = geometry.get("coordinates", [0, 0])
    if len(coords) >= 2:
        return coords[1], coords[0]  # lat, lon (GeoJSON is lon,lat)
    return 0, 0


def _get_incident_name(incident: dict) -> str:
    """Generate a descriptive callsign for the CoT event."""
    incident_type = _get_incident_type(incident)
    type_labels = {
        "structure_fire": "Structure Fire",
        "wildfire": "Wildfire",
        "vehicle_fire": "Vehicle Fire",
        "cooking_fire": "Cooking Fire",
        "electrical_fire": "Electrical Fire",
        "brush_fire": "Brush Fire",
        "dumpster_fire": "Dumpster Fire",
        "chimney_fire": "Chimney Fire",
    }
    label = type_labels.get(incident_type, incident_type.replace("_", " ").title())

    dispatch = incident.get("dispatch", {})
    city = dispatch.get("location", {}).get("city", "")
    timestamp = dispatch.get("timestamp", "")
    date_str = timestamp[:10] if timestamp else ""

    parts = [label]
    if city:
        parts.append(city)
    if date_str:
        parts.append(date_str)
    return " - ".join(parts)


def _generate_remarks_text(incident: dict) -> str:
    """
    Generate a plain-text risk report for the CoT remarks field.
    iTAK displays this text in the details panel when a marker is tapped.
    """
    from risk_analysis import (
        bow_tie_analysis,
        fmea_analysis,
        decision_tree_analysis,
        markov_risk_state,
    )

    bow_tie = bow_tie_analysis(incident)
    fmea = fmea_analysis(incident)
    decision = decision_tree_analysis(incident)
    markov = markov_risk_state(incident)

    # Extract metadata
    incident_type = _get_incident_type(incident)
    type_labels = {
        "structure_fire": "Structure Fire",
        "wildfire": "Wildfire",
        "vehicle_fire": "Vehicle Fire",
        "cooking_fire": "Cooking Fire",
        "electrical_fire": "Electrical Fire",
        "brush_fire": "Brush Fire",
        "dumpster_fire": "Dumpster Fire",
        "chimney_fire": "Chimney Fire",
    }
    type_label = type_labels.get(incident_type, incident_type.replace("_", " ").title())

    dispatch = incident.get("dispatch", {})
    city = dispatch.get("location", {}).get("city", "Unknown")
    address = dispatch.get("location", {}).get("address", "")
    date_str = dispatch.get("timestamp", "Unknown")[:10]
    response_time = dispatch.get("response_time_minutes", 0)

    fire_detail = incident.get("fire_detail", {})
    property_loss = fire_detail.get("property_loss_dollars", 0)

    lines = []
    lines.append("═══════════════════════════════════")
    lines.append("  FIRE RISK REPORT")
    lines.append("  Project Crucible | ISO 31010")
    lines.append("═══════════════════════════════════")
    lines.append("")
    lines.append(f"Type: {type_label}")
    lines.append(f"Location: {city}, AZ")
    if address:
        lines.append(f"Address: {address}")
    lines.append(f"Date: {date_str}")
    lines.append(f"Response Time: {response_time:.1f} min")
    if property_loss:
        lines.append(f"Property Loss: ${property_loss:,.0f}")
    lines.append("")

    # Bow Tie Analysis
    lines.append("───────────────────────────────────")
    lines.append("BOW TIE ANALYSIS")
    lines.append("───────────────────────────────────")
    lines.append(f"Preventative Controls: {bow_tie['preventative_overall']}")
    for name, ctrl in bow_tie["preventative_controls"].items():
        eff = ctrl.get("effectiveness", "N/A")
        display_name = name.replace("_", " ").title()
        lines.append(f"  • {display_name}: {eff}")
    lines.append(f"Reactive Controls: {bow_tie['reactive_overall']}")
    for name, ctrl in bow_tie["reactive_controls"].items():
        eff = ctrl.get("effectiveness", "N/A")
        display_name = name.replace("_", " ").title()
        extra = ""
        if "minutes" in ctrl and ctrl["minutes"]:
            extra = f" ({ctrl['minutes']:.1f} min)"
        elif "units" in ctrl:
            extra = f" ({ctrl['units']} units)"
        lines.append(f"  • {display_name}: {eff}{extra}")
    lines.append("")

    # FMEA
    lines.append("───────────────────────────────────")
    lines.append("FAILURE MODE ANALYSIS (Top 3)")
    lines.append("───────────────────────────────────")
    for i, fm in enumerate(fmea[:3], 1):
        lines.append(f"{i}. {fm['mode']}")
        lines.append(f"   RPN={fm['rpn']} (S={fm['severity']}×O={fm['occurrence']}×D={fm['detection']})")
        lines.append(f"   Cause: {fm['cause']}")
    lines.append("")

    # Decision Tree
    lines.append("───────────────────────────────────")
    lines.append("INVESTMENT DECISION")
    lines.append("⚠ SIMULATED — for demonstration")
    lines.append("───────────────────────────────────")
    lines.append(f"Recommendation: {decision['recommendation']}")
    lines.append(f"Investment Cost: ${decision['investment_cost']:,.0f}")
    lines.append(f"P(fire) without investment: {decision['p_fire_no_investment']:.1%}")
    lines.append(f"P(fire) with investment: {decision['p_fire_with_investment']:.1%}")
    lines.append(f"Expected Annual Savings: ${decision['annual_savings']:,.0f}")
    lines.append("")

    # Markov Risk State
    lines.append("───────────────────────────────────")
    lines.append("RISK CLASSIFICATION (Markov)")
    lines.append("───────────────────────────────────")
    lines.append(f"Current State: {markov['state']}")
    lines.append(f"Risk Score: {markov['risk_score']}/{markov['max_score']} ({markov['normalized_score']:.0%})")
    if markov["contributing_factors"]:
        lines.append("Contributing Factors:")
        for factor in markov["contributing_factors"]:
            lines.append(f"  • {factor}")
    lines.append("")
    lines.append("═══════════════════════════════════")
    lines.append("Project Crucible | Richards+")
    lines.append("Linked Trust | AI Trailblazers")
    lines.append("═══════════════════════════════════")

    return "\n".join(lines)


def _create_cot_event(incident: dict) -> ET.Element:
    """
    Create a single CoT (Cursor on Target) XML event for an incident.

    CoT schema: https://www.mitre.org/sites/default/files/pdf/09_4937.pdf
    """
    lat, lon = _get_coordinates(incident)
    if lat == 0 and lon == 0:
        return None

    incident_type = _get_incident_type(incident)
    cot_type = COT_TYPE_MAP.get(incident_type, "a-h-G")
    callsign = _get_incident_name(incident)
    uid = f"crucible-{uuid.uuid4().hex[:12]}"

    # Timestamps
    now = datetime.utcnow()
    dispatch = incident.get("dispatch", {})
    timestamp_str = dispatch.get("timestamp", "")
    if timestamp_str:
        try:
            event_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            event_time = now
    else:
        event_time = now

    time_fmt = "%Y-%m-%dT%H:%M:%SZ"
    stale_time = event_time + timedelta(days=365)  # Keep markers visible for a year

    # Build CoT event XML
    event = ET.Element("event")
    event.set("version", "2.0")
    event.set("uid", uid)
    event.set("type", cot_type)
    event.set("how", "m-g")  # machine-generated
    event.set("time", event_time.strftime(time_fmt))
    event.set("start", event_time.strftime(time_fmt))
    event.set("stale", stale_time.strftime(time_fmt))

    # Point element
    point = ET.SubElement(event, "point")
    point.set("lat", str(round(lat, 6)))
    point.set("lon", str(round(lon, 6)))
    point.set("hae", "0")  # height above ellipsoid
    point.set("ce", "50")  # circular error (meters)
    point.set("le", "50")  # linear error (meters)

    # Detail element (contains remarks, contact, etc.)
    detail = ET.SubElement(event, "detail")

    # Contact element (callsign shows as the marker label)
    contact = ET.SubElement(detail, "contact")
    contact.set("callsign", callsign)

    # Remarks element (this is what shows in the details panel!)
    remarks = ET.SubElement(detail, "remarks")
    remarks.text = _generate_remarks_text(incident)

    # Color element
    color_val = COT_COLOR_MAP.get(incident_type, "-65536")
    color_elem = ET.SubElement(detail, "color")
    color_elem.set("argb", color_val)

    # UserIcon — use TAK's built-in fire/flame icon
    usericon = ET.SubElement(detail, "usericon")
    usericon.set("iconsetpath", "34ae1613-9645-4222-a9d2-e5f243dea2865/Military/Fire.png")

    # Link to source
    link = ET.SubElement(detail, "link")
    link.set("relation", "p-p")
    link.set("type", "a-f-G")
    link.set("uid", "project-crucible")

    # Archive flag so it persists
    archive = ET.SubElement(detail, "archive")

    return event


def generate_cot_data_package(incidents: list, output_path: str) -> str:
    """
    Generate a TAK Data Package (.zip) containing CoT events.

    A TAK Data Package is a ZIP file with:
    - manifest.xml (describes the package contents)
    - One or more .cot files (CoT event XML)

    iTAK imports these natively and displays all markers with full
    details/remarks accessible by tapping.

    Args:
        incidents: List of incident dicts
        output_path: File path for the output .zip file

    Returns:
        The output file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate all CoT events
    cot_events = []
    for incident in incidents:
        event = _create_cot_event(incident)
        if event is not None:
            cot_events.append(event)

    # Create the data package ZIP
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Write each CoT event as a separate file
        for i, event in enumerate(cot_events):
            event_xml = ET.tostring(event, encoding="unicode", xml_declaration=False)
            event_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + event_xml
            filename = f"cot/event_{i:03d}.cot"
            zf.writestr(filename, event_xml)

        # Write manifest.xml
        manifest = _create_manifest(len(cot_events))
        zf.writestr("manifest.xml", manifest)

        # Write MANIFEST/manifest.xml (some TAK versions look here)
        zf.writestr("MANIFEST/manifest.xml", manifest)

    return output_path


def _create_manifest(event_count: int) -> str:
    """Create the manifest.xml for the data package."""
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    pkg_uid = f"crucible-pkg-{uuid.uuid4().hex[:8]}"

    manifest = ET.Element("MissionPackageManifest")
    manifest.set("version", "2")

    config = ET.SubElement(manifest, "Configuration")
    param_uid = ET.SubElement(config, "Parameter")
    param_uid.set("name", "uid")
    param_uid.set("value", pkg_uid)

    param_name = ET.SubElement(config, "Parameter")
    param_name.set("name", "name")
    param_name.set("value", "Project Crucible - AZ Fire Incidents")

    param_onrecv = ET.SubElement(config, "Parameter")
    param_onrecv.set("name", "onReceiveImport")
    param_onrecv.set("value", "true")

    param_onrecvdel = ET.SubElement(config, "Parameter")
    param_onrecvdel.set("name", "onReceiveDelete")
    param_onrecvdel.set("value", "false")

    contents = ET.SubElement(manifest, "Contents")
    for i in range(event_count):
        content = ET.SubElement(contents, "Content")
        content.set("ignore", "false")
        content.set("zipEntry", f"cot/event_{i:03d}.cot")

        param = ET.SubElement(content, "Parameter")
        param.set("name", "contentType")
        param.set("value", "CoT")

    xml_str = ET.tostring(manifest, encoding="unicode", xml_declaration=False)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str


# Keep the KML export as a fallback option
def generate_kml(incidents: list, output_path: str) -> str:
    """
    Generate a KML file (legacy fallback — use generate_cot_data_package instead).
    """
    from risk_analysis import generate_risk_report as _gen_report
    import html
    import re

    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")

    name_el = ET.SubElement(document, "name")
    name_el.text = "Project Crucible — AZ Fire Incidents"

    folder = ET.SubElement(document, "Folder")
    folder_name = ET.SubElement(folder, "name")
    folder_name.text = "Fire Incidents — Arizona"

    for incident in incidents:
        base = incident.get("base", {})
        point_data = base.get("point", {})
        geometry = point_data.get("geometry", {})
        coords = geometry.get("coordinates", [0, 0])
        if len(coords) < 2 or (coords[0] == 0 and coords[1] == 0):
            continue

        lon, lat = coords[0], coords[1]
        placemark = ET.SubElement(folder, "Placemark")

        pm_name = ET.SubElement(placemark, "name")
        pm_name.text = _get_incident_name(incident)

        description = ET.SubElement(placemark, "description")
        report = _gen_report(incident)
        description.text = f"__CDATA_START__{report}__CDATA_END__"

        point_el = ET.SubElement(placemark, "Point")
        coordinates = ET.SubElement(point_el, "coordinates")
        coordinates.text = f"{lon},{lat},0"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rough_string = ET.tostring(kml, encoding="unicode", xml_declaration=False)

    def _restore_cdata(match):
        escaped_content = match.group(1).strip()
        original_content = html.unescape(escaped_content)
        return f'<![CDATA[\n{original_content}\n]]>'

    rough_string = re.sub(
        r'__CDATA_START__(.*?)__CDATA_END__',
        _restore_cdata,
        rough_string,
        flags=re.DOTALL,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(rough_string)

    return output_path
