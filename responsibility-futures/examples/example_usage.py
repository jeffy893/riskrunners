#!/usr/bin/env python3
"""
Example usage of Cortext.io Integration with Responsibility Futures Engine

This script demonstrates how to process Cortext.io reports and generate
responsibility assessments for entities mentioned in the extracted events.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from cortext_integration import CortextResponsibilityEngine

def run_example():
    """Run example analysis on sample Cortext.io data"""
    
    # Sample Cortext.io data structure (simplified)
    sample_data = {
        "_source": {
            "@timestamp": "2025-12-30T08:20:14.596619",
            "sentences": [
                {
                    "sentence": "Trump said the United States could support another major strike on Iran.",
                    "warm_vector": [0.0, 0.023, 0.0],
                    "cold_vector": [0.0, 0.023, 0.0]
                },
                {
                    "sentence": "Netanyahu said Israel was not seeking a confrontation with Iran.",
                    "warm_vector": [0.0, 0.029, 0.0],
                    "cold_vector": [0.0, 0.029, 0.0]
                },
                {
                    "sentence": "There will be hell to pay, Trump warned.",
                    "warm_vector": [0.0, 0.091, 0.0],
                    "cold_vector": [0.0, 0.0, 0.0]
                }
            ],
            "subjects": ["Trump", "Netanyahu", "Iran", "Israel", "United States"],
            "phen": ["major strike", "confrontation", "hell to pay", "warned"]
        }
    }
    
    # Initialize engine
    engine = CortextResponsibilityEngine()
    
    # Process the sample data
    engine.extract_entities_and_events(sample_data)
    
    # Generate report
    report = engine.generate_responsibility_report()
    
    print("EXAMPLE RESPONSIBILITY FUTURES ANALYSIS")
    print("=" * 50)
    print(f"Entities analyzed: {report['total_entities']}")
    print(f"Events processed: {report['total_events']}")
    print()
    
    print("Responsibility Ratios:")
    print("-" * 50)
    for assessment in report["entity_assessments"]:
        print(f"{assessment['entity']:<15} R={assessment['responsibility_ratio']:6.2f} "
              f"({assessment['risk_level']}) [{assessment['mentions']} mentions]")
        print(f"  Intention: {assessment['intention_score']:6.3f} | "
              f"Negligence: {assessment['negligence_score']:6.3f}")
        print()

if __name__ == "__main__":
    run_example()