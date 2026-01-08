import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

# ==========================================
# PART 1: DATA STRUCTURES (The Event Code)
# ==========================================

class Entity:
    def __init__(self, name: str, attributes: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.name = name
        self.attributes = attributes  # e.g., {'credit': 700, 'health': 100}

class Event:
    def __init__(self, name: str, timestamp: datetime, subjects: List[Entity], 
                 concepts: List[str], primes: Dict[str, float]):
        self.name = name
        self.timestamp = timestamp
        self.subjects = subjects
        self.concepts = concepts
        self.primes = primes  # Quantitative data, e.g., {'speed': 65, 'force': 1000}

# ==========================================
# PART 2: THE LOGIC (Appendix Implementation)
# ==========================================

class RiskEngine:
    """
    Implements the Responsibility Futures logic:
    R = Intention / Negligence
    """

    def __init__(self):
        self.risk_level = 0
        self.responsibility_score = 0.0

    # --- Negligence Logic (The Stick) ---
    # Path: Duty -> Breach -> Causation -> Damages -> Negligence

    def has_duty(self, entity_a: Entity, entity_b: Entity, event: Event) -> bool:
        """
        Duty(x, y, e) = x and y and e
        Checks if a valid relationship/contract exists between entities for this event.
        """
        # Logic: Do they have a prior agreement or social contract?
        # For simulation, we assume 'True' if both exist in the event subjects.
        return entity_a in event.subjects and entity_b in event.subjects

    def has_breach(self, entity_a: Entity, event: Event, duty_exists: bool) -> bool:
        """
        Breach(Duty)
        Checks if the entity failed to act according to the duty (missing attributes/actions).
        """
        if not duty_exists:
            return False
        
        # Example: Did they fail to maintain a threshold?
        # In your paper: "Not all attributes exist anymore"
        # Implementation: Check for missing required 'prime' values in event.
        required_primes = ['safety_check', 'communication'] 
        for req in required_primes:
            if req not in event.primes:
                return True # Breach occurred
        return False

    def has_causation(self, entity_a: Entity, event: Event, breach_occurred: bool) -> bool:
        """
        Causation(Breach)
        Checks if the entity was the driver of the breach.
        Paper Logic: b - b != 0 (Change in state implies action/causation)
        """
        if not breach_occurred:
            return False
        
        # Check if entity was active (e.g., velocity > 0, output > 0)
        return event.primes.get('activity_level', 0) > 0

    def has_damages(self, victim: Entity, event: Event, causation_confirmed: bool) -> bool:
        """
        Damages(Causation)
        Checks if the victim suffered loss.
        Paper Logic: Loss of attributes.
        """
        if not causation_confirmed:
            return False
        
        # Check for negative impact
        return event.primes.get('financial_loss', 0) > 0 or event.primes.get('physical_harm', 0) > 0

    # --- Intention Logic (The Carrot) ---
    # Inverse Path: NonDuty -> NonBreach -> NonCausation -> NonDamages

    def calculate_intention_score(self, entity: Entity, history: List[Event]) -> float:
        """
        Determines the 'I' in R = I/N.
        Based on the Appendix Risk Levels.
        """
        intention_points = 0
        
        for event in history:
            # Step 1: Check Risk Level 1 (NonDuty)
            # "If there are no duties... we set them to highest risk level"
            # Here we reward taking on duties.
            duties = [s for s in event.subjects if s != entity]
            if not duties:
                continue # No duty, no points
            
            intention_points += 1 # Point for having a duty (Engagement)

            # Step 2: Check Risk Level 2 (NonBreach)
            # "If a person has duties but no breaches..."
            breach = self.has_breach(entity, event, duty_exists=True)
            if not breach:
                intention_points += 5 # High reward for reliability
                continue

            # Step 3: Check Risk Level 3 (NonCausation)
            # "Breach exists, but they were not the cause"
            causation = self.has_causation(entity, event, breach_occurred=True)
            if not causation:
                intention_points += 2 # Reward for being a bystander rather than perpetrator
                continue
                
            # If caused damages, point deduction
            damages = self.has_damages(entity, event, causation_confirmed=True) # Check self-harm or external
            if damages:
                intention_points -= 10

        return float(intention_points)

    # --- The Master Calculation ---

    def calculate_responsibility_future(self, entity: Entity, history: List[Event]) -> float:
        """
        R = I / N
        Returns the Responsibility Ratio.
        """
        # Calculate I (Intention)
        I = self.calculate_intention_score(entity, history)
        
        # Calculate N (Negligence Count)
        N = 0
        for event in history:
            # Determine if this specific event was negligent
            # (Duty + Breach + Causation + Damages)
            others = [s for s in event.subjects if s != entity]
            for other in others:
                if self.has_duty(entity, other, event):
                    if self.has_breach(entity, event, True):
                        if self.has_causation(entity, event, True):
                            if self.has_damages(other, event, True):
                                N += 1
        
        # Avoid division by zero (The "Mercy" Constant)
        if N == 0:
            N = 0.1 
            
        R = I / N
        return round(R, 2)

# ==========================================
# PART 3: USAGE EXAMPLE (For Testing)
# ==========================================

if __name__ == "__main__":
    # 1. Setup Entities
    giant = Entity("The Giant", {'strength': 100, 'hydration': 50})
    midget = Entity("The Midget", {'navigation': 100, 'hydration': 50})

    # 2. Simulate an Event (The Desert Journey)
    # Scenario: Midget navigates well (Intention), but Giant falls (Accident/No Breach)
    journey_event = Event(
        name="Desert Crossing",
        timestamp=datetime.now(),
        subjects=[giant, midget],
        concepts=["Survival", "Transport"],
        primes={
            'safety_check': 1,      # Protocol followed
            'communication': 1,     # Protocol followed
            'activity_level': 10,   # High effort
            'financial_loss': 0     # No damages
        }
    )

    # 3. Calculate Risk
    engine = RiskEngine()
    
    # Calculate R-Score for the Giant
    r_score = engine.calculate_responsibility_future(giant, [journey_event])
    
    print(f"Entity: {giant.name}")
    print(f"Responsibility Future Score (R): {r_score}")
    # Output should be high because I is positive and N is near zero.