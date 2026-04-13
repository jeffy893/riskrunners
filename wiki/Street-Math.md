# Street Math

[← Home](Home.md)

---

Located in `street-math/`. Ten screenplays that teach formal ISO 31010 risk assessment techniques through everyday street-level scenarios. Also hosted at [street.riskrunners.com](https://street.riskrunners.com).

## The Screenplays

| # | Technique | ISO Section | Scenario |
|---|-----------|-------------|----------|
| 1 | Bow Tie Analysis | B.4.2 | A veteran bouncer explains preventative and reactive controls around a bar brawl |
| 2 | Decision Tree Analysis | B.9.3 | A street hustler maps decision nodes and expected values for a supplier payment |
| 3 | Monte Carlo Simulation | B.5.10 | A mechanic runs 100 mental simulations showing why a quick fix is an 86% failure bet |
| 4 | Game Theory | B.9.4 | Two roommates face the Prisoner's Dilemma when their landlord offers a snitch deal |
| 5 | LOPA | B.4.4 | A heist planner calculates probability of failure on demand for vault protection layers |
| 6 | Ishikawa (Fishbone) | B.3.3 | A food truck owner traces a ruined lunch rush through the 6Ms to find root causes |
| 7 | Pareto Charts | B.8.4 | A bartender teaches the 80/20 rule for revenue loss |
| 8 | Cross Impact Analysis | B.6.2 | A bookie explains how one injury shifts conditional probabilities across prop bets |
| 9 | Cost/Benefit Analysis | B.9.2 | A loan shark walks a borrower through NPV and a 1,160% effective annual rate |
| 10 | Markov Analysis | B.5.9 | A subway busker builds a transition matrix to optimize which train cars to play in |

## How to View

Open `index.html` in any browser. Each screenplay is a standalone HTML file — no server, no dependencies, no build step.

## Design

- Each screenplay has a unique color palette and header image with a visual motif (bow tie shape, decision tree, dice, game grid, fishbone, etc.)
- Dark theme, responsive layout, print-friendly CSS
- Header images are base64-encoded directly into the HTML
- Character names centered and bold, stage directions italicized, scene headings accented

## Regenerating

```bash
pip install Pillow
python3 generate_screenplays.py
```

Reads prompts from `iso_301010_sreenplay_prompts.csv`, generates unique header images using Pillow, and outputs 10 standalone HTML files plus corresponding PNGs in `img/`.

## Requirements

- Python 3.10+
- Pillow
