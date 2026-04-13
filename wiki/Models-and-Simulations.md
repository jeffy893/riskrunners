# Models & Simulations

[← Home](Home.md)

---

Standalone simulation models and analytical tools. Located in `models/`.

## Capital Lifecycle Model

`models/capital-lifecycle/`

A Python visualization of three types of capital mapped to life stages using logistic S-curves and skewed distributions.

### The Three Capitals

| Capital Type | Curve Color | Distribution | Life Stage Peak |
|-------------|-------------|--------------|-----------------|
| Scope Capital (Physical) | Green | Normal | Highest deceleration at age 32 |
| Social Capital (Career) | Orange | Left-skewed | Highest velocity at age 32 |
| Material Capital (Wealth) | Blue | Right-skewed | Highest acceleration at age 32 |

The model uses `scipy.stats.skewnorm` and logistic functions to show how physical development plateaus early, career momentum peaks at midlife, and wealth accumulation accelerates later. The bottom plot shows population-level distributions with a Dunbar's number (~150) annotation for social capital.

**Output:** `life_capital_curves.png`

**Run:** `python capital-lifecycle.py`

---

## Pickleball Ladder League Simulation

`models/pickleball/`

Monte Carlo simulation of a 24-player pickleball ladder league to evaluate different scoring systems.

### Parameters
- 50 full league simulations
- 24 players with random skill levels (50–100)
- 6 matches per player, courts of 4 with round-robin pairings
- Tests bonus point values of 0, 1, 2, 3, 4 per win

### Output
- `pickleball_league_simulation_results.csv` — Full results with rank comparisons
- `2025-07-25_Pickleball-Sim.twb` — Tableau workbook for visualization
- `ladder-league-simulation.png` — Visual summary

The simulation compares final rankings under each scoring method against the "true" skill-based ranking to evaluate which bonus point system best rewards actual skill.

**Run:** `python sim-matches.py`

---

## Linguistics: French Language Analysis

`models/linguistics/french.md`

An exploration of how the French subjunctive mood serves as a grammatical mechanism for expressing uncertainty, and how French cultural concepts (l'absurde, l'ironie, l'esprit critique, le décalage) provide frameworks for naming paradoxical or absurd situations.

Key concepts covered:
- The subjunctive as the language of contingent desire and lack of control
- L'esprit de l'escalier, Système D, raison d'être
- Existentialism and absurdism (Sartre, Camus) as cultural vocabulary
- Application to social dynamics and the optionality of human relationships
