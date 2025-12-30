#!/usr/bin/env python3
"""
Cortext.io Integration for Responsibility Futures Engine

Processes Cortext.io JSON reports to calculate Responsibility Ratios (R = I/N)
for entities mentioned in extracted event data.
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class CortextEntity:
    """Entity extracted from Cortext.io analysis"""
    name: str
    mention_count: int = 0
    warm_vector_sum: List[float] = None
    cold_vector_sum: List[float] = None
    
    def __post_init__(self):
        if self.warm_vector_sum is None:
            self.warm_vector_sum = [0.0, 0.0, 0.0]
        if self.cold_vector_sum is None:
            self.cold_vector_sum = [0.0, 0.0, 0.0]

@dataclass
class ResponsibilityEvent:
    """Event processed from Cortext.io sentence data"""
    sentence: str
    timestamp: str
    entities: List[str]
    warm_vector: List[float]
    cold_vector: List[float]
    concepts: List[str]

class CortextResponsibilityEngine:
    """
    Responsibility Futures Engine integrated with Cortext.io Event Code Extractor
    
    Converts Cortext.io extracted events into Responsibility Ratio calculations
    using warm/cold vectors as proxies for Intention/Negligence assessment.
    """
    
    def __init__(self):
        self.entities: Dict[str, CortextEntity] = {}
        self.events: List[ResponsibilityEvent] = []
    
    def load_cortext_report(self, json_file_path: str) -> Dict[str, Any]:
        """Load and parse Cortext.io JSON report"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_entities_and_events(self, cortext_data: Dict[str, Any]) -> None:
        """Extract entities and events from Cortext.io data structure"""
        source = cortext_data.get('_source', {})
        sentences = source.get('sentences', [])
        subjects = source.get('subjects', [])
        concepts = source.get('phen', [])  # phenomena as concepts
        timestamp = source.get('@timestamp', datetime.now().isoformat())
        
        # Initialize entities from subjects
        for subject in subjects:
            if subject not in self.entities:
                self.entities[subject] = CortextEntity(name=subject)
        
        # Process sentences as events
        for sentence_data in sentences:
            sentence = sentence_data.get('sentence', '')
            warm_vector = sentence_data.get('warm_vector', [0.0, 0.0, 0.0])
            cold_vector = sentence_data.get('cold_vector', [0.0, 0.0, 0.0])
            
            # Find entities mentioned in this sentence
            mentioned_entities = [
                entity for entity in subjects 
                if entity.lower() in sentence.lower()
            ]
            
            # Update entity statistics
            for entity_name in mentioned_entities:
                entity = self.entities[entity_name]
                entity.mention_count += 1
                for i in range(3):
                    entity.warm_vector_sum[i] += warm_vector[i]
                    entity.cold_vector_sum[i] += cold_vector[i]
            
            # Create event
            event = ResponsibilityEvent(
                sentence=sentence,
                timestamp=timestamp,
                entities=mentioned_entities,
                warm_vector=warm_vector,
                cold_vector=cold_vector,
                concepts=[c for c in concepts if c.lower() in sentence.lower()]
            )
            self.events.append(event)
    
    def calculate_intention_score(self, entity: CortextEntity) -> float:
        """
        Calculate Intention (I) based on warm vectors
        
        Warm vectors represent: Positivity, Engagement, Optimism
        Higher warm vectors indicate intentional, positive actions
        """
        if entity.mention_count == 0:
            return 0.0
        
        # Average warm vector across all mentions
        avg_warm = [w / entity.mention_count for w in entity.warm_vector_sum]
        
        # Weighted sum: Positivity(0.4) + Engagement(0.4) + Optimism(0.2)
        intention_score = (avg_warm[0] * 0.4 + avg_warm[1] * 0.4 + avg_warm[2] * 0.2) * 100
        
        return max(intention_score, 0.1)  # Minimum floor to avoid zero
    
    def calculate_negligence_score(self, entity: CortextEntity) -> float:
        """
        Calculate Negligence (N) based on cold vectors
        
        Cold vectors represent: Negativity, Risk, Uncertainty
        Higher cold vectors indicate negligent or harmful actions
        """
        if entity.mention_count == 0:
            return 1.0
        
        # Average cold vector across all mentions
        avg_cold = [c / entity.mention_count for c in entity.cold_vector_sum]
        
        # Weighted sum: Negativity(0.5) + Risk(0.3) + Uncertainty(0.2)
        negligence_score = (avg_cold[0] * 0.5 + avg_cold[1] * 0.3 + avg_cold[2] * 0.2) * 100
        
        return max(negligence_score, 0.1)  # Minimum floor to avoid zero
    
    def calculate_responsibility_ratio(self, entity_name: str) -> Dict[str, Any]:
        """
        Calculate R = Intention / Negligence for an entity
        
        Returns comprehensive responsibility assessment
        """
        if entity_name not in self.entities:
            return {"error": f"Entity '{entity_name}' not found"}
        
        entity = self.entities[entity_name]
        intention = self.calculate_intention_score(entity)
        negligence = self.calculate_negligence_score(entity)
        
        responsibility_ratio = intention / negligence
        
        # Risk assessment based on ratio
        if responsibility_ratio > 10:
            risk_level = "Very Low"
        elif responsibility_ratio > 5:
            risk_level = "Low"
        elif responsibility_ratio > 2:
            risk_level = "Moderate"
        elif responsibility_ratio > 1:
            risk_level = "High"
        else:
            risk_level = "Very High"
        
        return {
            "entity": entity_name,
            "mentions": entity.mention_count,
            "intention_score": round(intention, 3),
            "negligence_score": round(negligence, 3),
            "responsibility_ratio": round(responsibility_ratio, 3),
            "risk_level": risk_level,
            "avg_warm_vector": [round(w / entity.mention_count, 3) for w in entity.warm_vector_sum],
            "avg_cold_vector": [round(c / entity.mention_count, 3) for c in entity.cold_vector_sum]
        }
    
    def generate_responsibility_report(self) -> Dict[str, Any]:
        """Generate comprehensive responsibility report for all entities"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_entities": len(self.entities),
            "total_events": len(self.events),
            "entity_assessments": []
        }
        
        # Calculate responsibility ratios for all entities
        for entity_name in self.entities:
            assessment = self.calculate_responsibility_ratio(entity_name)
            if "error" not in assessment:
                report["entity_assessments"].append(assessment)
        
        # Sort by responsibility ratio (highest first)
        report["entity_assessments"].sort(
            key=lambda x: x["responsibility_ratio"], 
            reverse=True
        )
        
        return report

def main():
    """Main execution function"""
    if len(sys.argv) != 2:
        print("Usage: python cortext_integration.py <cortext_report.json>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    try:
        # Initialize engine
        engine = CortextResponsibilityEngine()
        
        # Load and process Cortext.io report
        cortext_data = engine.load_cortext_report(json_file)
        engine.extract_entities_and_events(cortext_data)
        
        # Generate responsibility report
        report = engine.generate_responsibility_report()
        
        # Output results
        print("=" * 60)
        print("RESPONSIBILITY FUTURES ANALYSIS")
        print("Powered by Cortext.io Event Code Extractor")
        print("=" * 60)
        print(f"Analysis Date: {report['timestamp']}")
        print(f"Total Entities: {report['total_entities']}")
        print(f"Total Events: {report['total_events']}")
        print()
        
        print("TOP RESPONSIBILITY RATIOS:")
        print("-" * 60)
        for i, assessment in enumerate(report["entity_assessments"][:10], 1):
            print(f"{i:2d}. {assessment['entity']:<20} "
                  f"R={assessment['responsibility_ratio']:6.2f} "
                  f"({assessment['risk_level']}) "
                  f"[{assessment['mentions']} mentions]")
        
        # Save detailed report
        output_file = json_file.replace('.json', '_responsibility_analysis.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed report saved to: {output_file}")
        
    except Exception as e:
        print(f"Error processing Cortext.io report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()