"""
Project Crucible — Main Orchestrator
Fetches Arizona fire incident data (real or simulated), runs ISO 31010 risk analysis,
and exports a KML file for visualization in iTAK.

Usage:
    python main.py

Environment Variables (optional):
    NERIS_CLIENT_ID     - NERIS API client ID
    NERIS_CLIENT_SECRET - NERIS API client secret

If credentials are not set, the script uses simulated data for demonstration.
"""

import os
import sys

from config import (
    USE_SIMULATED_DATA,
    DEFAULT_STATE,
    DEFAULT_INCIDENT_TYPES,
    DEFAULT_PAGE_SIZE,
    OUTPUT_DIR,
    OUTPUT_KML_FILENAME,
)
from risk_analysis import (
    bow_tie_analysis,
    fmea_analysis,
    decision_tree_analysis,
    markov_risk_state,
)
from tak_export import generate_cot_data_package, generate_kml


def fetch_incidents() -> list:
    """Fetch incidents from NERIS API or generate simulated data."""
    if USE_SIMULATED_DATA:
        print("=" * 60)
        print("  PROJECT CRUCIBLE — Fire Risk Analysis Pipeline")
        print("  Mode: SIMULATED DATA (no API credentials detected)")
        print("=" * 60)
        print()
        print("[*] Generating simulated Arizona fire incident data...")
        from simulated_data import generate_simulated_incidents
        incidents = generate_simulated_incidents(count=40)
        print(f"[+] Generated {len(incidents)} simulated incidents")
        return incidents
    else:
        print("=" * 60)
        print("  PROJECT CRUCIBLE — Fire Risk Analysis Pipeline")
        print("  Mode: LIVE DATA (NERIS API)")
        print("=" * 60)
        print()
        print("[*] Authenticating with NERIS API...")
        from neris_client import NERISClient
        client = NERISClient()
        client.authenticate()
        print("[+] Authentication successful")

        print(f"[*] Fetching fire incidents for state={DEFAULT_STATE}...")
        incidents = client.list_all_incidents(
            state=DEFAULT_STATE,
            incident_types=DEFAULT_INCIDENT_TYPES,
            page_size=DEFAULT_PAGE_SIZE,
        )
        print(f"[+] Retrieved {len(incidents)} incidents from NERIS API")
        return incidents


def analyze_incidents(incidents: list) -> dict:
    """Run risk analysis on all incidents and collect summary statistics."""
    print()
    print("[*] Running ISO 31010 risk analysis on each incident...")

    stats = {
        "total": len(incidents),
        "by_type": {},
        "risk_states": {"LOW": 0, "MODERATE": 0, "HIGH": 0},
        "invest_recommendations": 0,
        "avg_rpn_top": 0,
    }

    total_top_rpn = 0

    for incident in incidents:
        # Count by type
        inc_type = incident.get("incident_types", ["unknown"])[0]
        stats["by_type"][inc_type] = stats["by_type"].get(inc_type, 0) + 1

        # Markov classification
        markov = markov_risk_state(incident)
        stats["risk_states"][markov["state"]] += 1

        # Decision tree
        decision = decision_tree_analysis(incident)
        if decision["recommendation"] == "INVEST":
            stats["invest_recommendations"] += 1

        # Top FMEA RPN
        fmea = fmea_analysis(incident)
        if fmea:
            total_top_rpn += fmea[0]["rpn"]

    stats["avg_rpn_top"] = total_top_rpn / len(incidents) if incidents else 0

    print(f"[+] Analysis complete for {len(incidents)} incidents")
    return stats


def export_kml(incidents: list) -> str:
    """Export incidents with risk reports to CoT Data Package (.zip) for iTAK."""
    print()
    # Build output path relative to the script's parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)

    # Primary output: CoT Data Package (iTAK native format)
    dp_path = os.path.join(project_dir, OUTPUT_DIR, "az_fire_incidents.zip")
    print(f"[*] Generating CoT Data Package for iTAK...")
    result_path = generate_cot_data_package(incidents, dp_path)
    file_size = os.path.getsize(result_path)
    print(f"[+] Data Package exported: {result_path}")
    print(f"    File size: {file_size / 1024:.1f} KB")

    # Also generate KML as fallback
    kml_path = os.path.join(project_dir, OUTPUT_DIR, OUTPUT_KML_FILENAME)
    generate_kml(incidents, kml_path)
    print(f"[+] KML fallback also exported: {kml_path}")

    return result_path


def print_summary(stats: dict, kml_path: str):
    """Print a summary of the analysis results."""
    print()
    print("=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print()
    print(f"  Total incidents analyzed: {stats['total']}")
    print()
    print("  Incidents by type:")
    for inc_type, count in sorted(stats["by_type"].items(), key=lambda x: x[1], reverse=True):
        label = inc_type.replace("_", " ").title()
        print(f"    {label:.<30} {count}")
    print()
    print("  Risk classification (Markov):")
    print(f"    LOW ........ {stats['risk_states']['LOW']}")
    print(f"    MODERATE ... {stats['risk_states']['MODERATE']}")
    print(f"    HIGH ....... {stats['risk_states']['HIGH']}")
    print()
    print(f"  Investment recommendations: {stats['invest_recommendations']}/{stats['total']}")
    print(f"  Average top FMEA RPN: {stats['avg_rpn_top']:.0f}")
    print()
    print(f"  Output: {kml_path}")
    print()
    print("  To load in iTAK:")
    print("    1. Transfer the .zip file to your iPad (AirDrop, Files, etc.)")
    print("    2. Open iTAK → tap the hamburger menu (≡)")
    print("    3. Go to 'Data Packages' → 'Import'")
    print("    4. Select 'az_fire_incidents.zip'")
    print("    5. Markers appear on the map immediately")
    print("    6. TAP any marker → tap its name/callsign in the popup")
    print("    7. The REMARKS section shows the full risk report")
    print()
    print("=" * 60)
    print("  Project Crucible | Richards+ | Linked Trust | AI Trailblazers")
    print("=" * 60)


def main():
    """Main entry point for the Project Crucible pipeline."""
    try:
        # Step 1: Fetch or generate incident data
        incidents = fetch_incidents()

        if not incidents:
            print("[!] No incidents found. Exiting.")
            sys.exit(1)

        # Step 2: Run risk analysis
        stats = analyze_incidents(incidents)

        # Step 3: Export to KML
        kml_path = export_kml(incidents)

        # Step 4: Print summary
        print_summary(stats, kml_path)

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        raise


if __name__ == "__main__":
    main()
