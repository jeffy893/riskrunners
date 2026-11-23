# Torque per Capita: Research Agenda Model

**Live site:** https://health.riskrunners.com *(not up yet; it will be soon)*

An interactive model of queues, Itô-style diffusions and captive-insurance governance for the healthcare coverage crisis. It is a Risk Runners project under Integral Mass, and it is the companion to the white paper *The Last Will Be First and the First Will Be Last* in this folder's parent (`models/healthcare/`).

This folder holds only this README. The site's code lives in its own repository folder, `health.riskrunners.com`, and is published at the address above.

## What the site is

A static website, plain HTML and JavaScript with no libraries and no server. Everything runs in the visitor's browser, and nothing is uploaded. It implements the six research steps from section 11 of the white paper, one tab per step:

| Tab | Research step | Paper equations |
|---|---|---|
| 1 Instrument a queue | Estimate arrival rate, service rate, utilization and work in progress for one workflow, and check Little's Law. Accepts your own `arrival,start,end` timestamps. | 4 |
| 2 Fit the diffusion | Fit a reflected diffusion on the first half of the data, then compare it with the held-out half and with a plain discrete-event simulation. | 5 |
| 3 Coupling | Edit a dependency matrix, compute the coupled cost of delay, and see the probability that the spectral radius reaches 1 as coupling grows. | 6 |
| 4 Torque per capita | Set staff, per-person output and technology by stage. Find the constraint and test where investment raises system throughput. | 10, 11 |
| 5 Governance | Compare three coverage designs on the full cost distribution and on recovery time after a shock. | 9 |
| 6 Narrative | Measure cosine similarity between statements, find orthogonal pairs and shared framing terms. | 12 |

## The idea in brief

The paper proposes **torque per capita** as the North Star KPI: the rate of constraint-clearing work each person in a queue can deliver, given the technology they have. System throughput is set by the stage where that rate is lowest relative to demand. The site lets a reader change a stage's staff, rate or technology and see whether system throughput moves.

## Data and limits

- Every default is synthetic or a placeholder assumption. A banner on the site says so. The outputs are not findings about any real plan, employer or person.
- Steps 1 and 2 can run on real timestamps pasted by the user.
- Step 2 includes one extension that is not in the paper: a state-dependent drift, λ − μ·min(Q, c). On the synthetic default it fits the held-out data much better than equation 5 with constant drift.
- Step 5 parameters are assumptions, not estimates.
- Step 6 uses word counts (TF-IDF), a crude proxy for meaning.
- Nothing on the site is medical, legal, actuarial, insurance or investment advice.

## Where things are

- Site (once live): https://health.riskrunners.com
- Site code: the `health.riskrunners.com` folder of the Risk Runners workspace (`index.html`, `style.css`, `js/core.js` for all model code, `js/ui.js` for charts and tables).
- Source repository: https://github.com/jeffy893/riskrunners/tree/dev/2.0/models/healthcare
- White paper: `2026-11-23_The-Last-Will-Be-First_White-Paper.pdf` and `.html` in the parent folder.
- Source documents for the paper: `Coupled Cost of Delay.pdf`, `Queuing-Theory_Synthesis_Report.pdf` and `queueing_theory_alts_visual_brief.pdf`, also in the parent folder.

## Running it before the site is live

Open `index.html` from the `health.riskrunners.com` folder directly in a browser. No build step is needed.

Integral Mass · A Risk Runners Project
