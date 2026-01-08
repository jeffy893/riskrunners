import random

class Entity:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.intention_score = 0
        self.negligence_score = 0

class Event:
    def __init__(self, timestamp, description, data=None):
        self.timestamp = timestamp
        self.description = description
        self.data = data or {}
        # States of the event lifecycle (from Appendix)
        self.has_duty = False
        self.is_breached = False
        self.is_caused = False
        self.has_damages = False

class ResponsibilityContract:
    def __init__(self, objective_r, tolerance, max_payout):
        self.objective_r = objective_r  # The "Policy Objective" R value
        self.tolerance = tolerance      # Acceptable variance
        self.max_payout = max_payout    # Maximum reward (Dignity/Esteem cap)

    def evaluate_event(self, event, entity):
        """
        Simulates the logical determination of Negligence vs Intention
        based on the Appendix logic flow:
        Negligence(Damages(Causation(Breach(Duty))))
        """
        # Step 1: Duty - Was there an obligation?
        # Logic: "Duty(x, y, e) = x AND y AND e"
        if event.has_duty:
            
            # Step 2: Breach - Was the duty failed?
            if event.is_breached:
                
                # Step 3: Causation - Did this entity cause it?
                # Logic: "a - b != 0" (Difference in state caused by entity)
                if event.is_caused:
                    
                    # Step 4: Damages - Was there a loss of attributes?
                    if event.has_damages:
                        # Full Negligence Sequence Complete
                        entity.negligence_score += 1
                        return "Negligence"
                    else:
                        # Caused breach but no damages (Near Miss)
                        # Still counts towards Intention in some frameworks, 
                        # but here we might treat it as neutral or partial risk.
                        pass
                else:
                    # Breached but not caused by entity (Force Majeure)
                    entity.intention_score += 0.5 # Partial credit for presence
            else:
                # Duty exists and was NOT breached (Success)
                # This is the primary driver of Intention (I)
                entity.intention_score += 1
                return "Intention"
        
        return "Neutral"

    def calculate_r_index(self, entity):
        """
        Calculates R = Intention / Negligence
        Handles division by zero by setting a floor for N.
        """
        # Smoothing N to avoid infinity; assumes everyone has base exposure of 1
        n_val = max(entity.negligence_score, 1) 
        
        r_actual = entity.intention_score / n_val
        return r_actual

    def calculate_payoff(self, entity):
        """
        The Delta Minimization Function.
        Rewards predictability (Low Delta).
        """
        r_actual = self.calculate_r_index(entity)
        
        # The Delta: Difference between Actual and Objective
        delta = abs(r_actual - self.objective_r)
        
        # Payout Logic: Linear decay based on Delta
        # If Delta is 0, Payout is Max.
        # If Delta > Tolerance, Payout becomes 0 (or negative/fine).
        
        if delta <= self.tolerance:
            # Simple linear hedge formula
            payout = self.max_payout * (1 - (delta / self.tolerance))
        else:
            payout = 0 
            # In a strict market, this could be negative (margin call on Solidarity)

        return {
            "Entity": entity.name,
            "R_Actual": round(r_actual, 2),
            "R_Objective": self.objective_r,
            "Delta": round(delta, 2),
            "Payout": round(payout, 2),
            "Status": "Hedge Successful" if payout > 0 else "Liquidation"
        }

# --- SIMULATION ---

# 1. Setup the Contract (The "Hegemonic Standard")
# We expect a ratio of 5:1 (5 Intentional acts per 1 Negligent act)
contract = ResponsibilityContract(objective_r=5.0, tolerance=2.0, max_payout=1000)

# 2. Create an Entity (The "Short Seller" of Solidarity)
user = Entity("New_User_01", "Service_Provider")

# 3. Simulate a workflow of events
events = []

# Scenario: User performs well mostly, but slips up occasionally.
for i in range(20):
    e = Event(i, f"Transaction_{i}")
    e.has_duty = True
    
    # 80% chance of success (Intention), 20% chance of issue
    if random.random() > 0.2:
        e.is_breached = False 
    else:
        e.is_breached = True
        e.is_caused = True
        e.has_damages = True # Full negligence flow

    events.append(e)

# 4. Process Events
for e in events:
    contract.evaluate_event(e, user)

# 5. Settle the Contract
result = contract.calculate_payoff(user)

print("--- Responsibility Future Settlement ---")
print(f"Intention Score (I): {user.intention_score}")
print(f"Negligence Score (N): {user.negligence_score}")
print("-" * 30)
for k, v in result.items():
    print(f"{k}: {v}")