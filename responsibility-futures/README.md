# Responsibility Futures Risk Engine (Account Ninja)

This repository contains the core logic for the **Account Ninja** simulation engine. [cite_start]It is a Python implementation of the "Responsibility Futures" algorithm derived from the manuscript *Stockholm Forgiveness of Responsibility: A Futures Market*[cite: 1, 2].

The engine calculates a **Responsibility Ratio ($R$)** for an entity based on historical event data, quantifying the relationship between **Intention ($I$)** and **Negligence ($N$)**.

## 📖 The Core Philosophy

[cite_start]The algorithm is based on the principle that responsibility is a quantifiable metric determined by how negligent and intentional an entity was, is, and will be[cite: 26].

The core formula driving this engine is:

$$\text{RESPONSIBILITY} (R) = \frac{\text{INTENTION} (I)}{\text{NEGLIGENCE} (N)}$$

[cite_start][cite: 50]

[cite_start]This model moves beyond simple financial credit scores (FICO) to measure "social and scope capital" [cite: 138][cite_start], allowing users to "lock in" their reliability for future agreements[cite: 146].

## ⚙️ How It Works

The `RiskEngine` class processes a history of **Events** to generate a score. [cite_start]It utilizes the "Event Code" notation proposed in the source text: `{[Timestamps], [Subjects], [Concepts], [Primes]}`[cite: 949].

### 1\. Determining Negligence ($N$)

[cite_start]Negligence is calculated using the standard legal order of operations defined in the Appendix [cite: 932-936, 948]:

1.  [cite_start]**Duty:** Did a legal/social duty exist between entities?[cite: 933].
2.  [cite_start]**Breach:** Did the entity fail to act as agreed?[cite: 934].
3.  [cite_start]**Causation:** Was the entity the driver of that breach?[cite: 935].
4.  [cite_start]**Damages:** Did the breach result in loss or harm?[cite: 936].

*If all four are true, $N$ increases.*

### 2\. Determining Intention ($I$)

[cite_start]Intention is calculated using the inverse logic flow ("The Carrot")[cite: 975]:

1.  [cite_start]**NonDuty:** Rewards assuming responsibility (taking on duties) where none existed[cite: 977, 979].
2.  [cite_start]**NonBreach:** Rewards reliability (having duties but never breaching them)[cite: 982].
3.  [cite_start]**NonCausation:** Rewards risk mitigation (breach occurred, but entity was not the cause)[cite: 990].
4.  [cite_start]**NonDamages:** Rewards harm reduction (breach and cause occurred, but damage was prevented)[cite: 996].

## 📦 Data Structures

[cite_start]The script implements the objects defined in the manuscript's "Event Code" theory[cite: 736, 737].

  * [cite_start]**`Entity`**: Represents an individual, business, or group (e.g., "The Giant", "The Midget")[cite: 32].
  * [cite_start]**`Event`**: A transaction or interaction containing specific "Primes" (quantitative data like force, speed, or financial value)[cite: 949].
  * [cite_start]**`RiskEngine`**: The calculator that simulates the "Court Case" logic to assign scores[cite: 943].

## 🚀 Usage

```python
from risk_models import Entity, Event, RiskEngine
from datetime import datetime

# 1. Define Entities
giant = Entity("The Giant", {'strength': 100})
midget = Entity("The Midget", {'navigation': 100})

# 2. Log an Event (The Desert Journey)
# [cite_start]Based on the allegory from Chapter 10 [cite: 846]
journey = Event(
    name="Desert Crossing",
    timestamp=datetime.now(),
    subjects=[giant, midget],
    concepts=["Survival", "Transport"],
    primes={
        'safety_check': 1,      # Protocol followed (NonBreach)
        'communication': 1,     # Protocol followed (NonBreach)
        'financial_loss': 0     # No Damages
    }
)

# 3. Calculate Score
engine = RiskEngine()
r_score = engine.calculate_responsibility_future(giant, [journey])

print(f"Responsibility Score: {r_score}")
```

## 📂 Project Context

This script serves as the backend logic for the **iMASS** (Integral Manufacturing and Shared Services) ecosystem:

  * **Input:** Data is fed from **gurila.tools** (User task management).
  * **Processing:** This script (`RiskEngine`) runs inside **Account Ninja**.
  * **Output:** The R-Score is displayed on **familyRM.net** dashboards to facilitate family governance and "Responsibility Future" contracts.

-----

*Based on "Stockholm Forgiveness of Responsibility: A Futures Market" (2019).*