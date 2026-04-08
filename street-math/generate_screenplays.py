#!/usr/bin/env python3
"""
Street Math Screenplay Generator
Reads prompts from CSV, generates header images and standalone HTML screenplays.
Requires: Python 3.10+, Pillow (pip install Pillow)
"""

import csv
import os
import math
import random
import base64
import textwrap
from io import BytesIO

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed. Installing...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(SCRIPT_DIR, "iso_301010_sreenplay_prompts.csv")
OUTPUT_DIR = SCRIPT_DIR


# ─── Screenplay content for each technique ───────────────────────────────────

SCREENPLAYS = {}

SCREENPLAYS["Bow Tie Analysis"] = {
    "title": "Bow Tie Analysis: The Bouncer's Blueprint",
    "iso_section": "B.4.2",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — EXT. NIGHTCLUB ENTRANCE — NIGHT",
            "content": """FADE IN:

A neon-lit nightclub entrance. Bass thumps from inside. MARCUS (50s, built like a refrigerator, 25 years on the door) stands with arms crossed. DESHAWN (20s, fresh hire, oversized security shirt) fidgets beside him.

MARCUS
(scanning the line)
You see that line? Every single one of them is a variable. And variables, kid, are what get people hurt.

DESHAWN
I just check IDs, right?

MARCUS
(laughs)
That's like saying a pilot just pushes buttons. Nah. You and me? We're running a Bow Tie Analysis every single night. We just don't call it that."""
        },
        {
            "heading": "PAGE 2 — THE CENTRAL EVENT",
            "content": """Marcus pulls out a cocktail napkin and draws a bow tie shape — a knot in the middle with lines fanning out on both sides.

MARCUS
See this knot in the middle? That's the Central Event. For us, that's a bar brawl. A full-on, bottles-flying, tables-flipping disaster.

DESHAWN
Okay...

MARCUS
Everything on the LEFT side? Those are the THREATS — the things that cause the brawl. Drunk guy gets disrespected. Two crews bump into each other. Someone's prior beef walks through the door.

He taps the left side of the napkin.

MARCUS (CONT'D)
Every one of these threats has a pathway straight to that central event. Our job is to put BARRIERS on those pathways. We call them Preventative Controls."""
        },
        {
            "heading": "PAGE 3 — PREVENTATIVE CONTROLS",
            "content": """MARCUS
Control number one: the ID check. That ain't just about age. You're reading body language. Glassy eyes? Slurred words? Aggressive posture? That's a threat indicator. You deny entry — you just blocked a pathway.

DESHAWN
What if they're already inside?

MARCUS
Control number two: the bartender cut-off protocol. Bartender sees someone at seven drinks, they signal us. We do a soft intervention — "Hey man, let me get you some water." That's a barrier between the threat and the brawl.

He draws X marks across the left-side lines.

MARCUS (CONT'D)
Control three: capacity management. Too many bodies, too much heat, too little space — that's a threat multiplier. We keep the count. Period.

DESHAWN
So if all these controls work, no brawl?

MARCUS
In theory. But controls fail. That's the whole point of the bow tie — you plan for BOTH sides."""
        },
        {
            "heading": "PAGE 4 — REACTIVE CONTROLS",
            "content": """Marcus taps the RIGHT side of the bow tie.

MARCUS
Now say the brawl happens anyway. Central event fires off. These lines on the right? Those are the CONSEQUENCES. Injuries. Property damage. Lawsuits. Liquor license revoked. Someone dies.

DESHAWN
(swallows hard)

MARCUS
But just like the left side has barriers, the right side has them too. We call these Reactive Controls — or Recovery Controls. They don't prevent the brawl. They limit the damage AFTER it starts.

He counts on his fingers.

MARCUS (CONT'D)
Reactive control one: bouncers intervene physically. Separate the fighters. Contain the zone. Reactive control two: call the cops immediately. Get EMS on standby. Reactive control three: evacuate bystanders through the side exits. Control four: preserve camera footage for legal protection."""
        },
        {
            "heading": "PAGE 5 — ESCALATION FACTORS",
            "content": """A DRUNK PATRON stumbles past them. Marcus watches him like a hawk, then turns back.

MARCUS
Now here's where it gets ugly. See, every one of those controls — left side AND right side — can be degraded by what we call Escalation Factors.

DESHAWN
Like what?

MARCUS
Like this.

He holds up his radio. It crackles with static.

MARCUS (CONT'D)
Last month, Tony's radio died mid-shift. Dead battery. He couldn't call for backup when two guys started swinging by the pool tables. By the time someone ran to get him, one guy had a broken nose and the other had a chair leg.

DESHAWN
Because of a dead radio?

MARCUS
Because of an escalation factor that degraded our reactive control. The physical intervention barrier failed because the communication system failed. One broken link in the chain and the consequence pathway opens wide."""
        },
        {
            "heading": "PAGE 6 — MAPPING THE FULL BOW TIE",
            "content": """Marcus smooths out the napkin and redraws it more carefully.

MARCUS
Let me lay it out clean for you.

He labels each section:

MARCUS (V.O.)
LEFT SIDE — THREATS:
• Intoxicated patron enters
• Rival groups present
• Prior personal conflict
• Overcrowding

PREVENTATIVE CONTROLS (barriers on left):
• ID check + behavioral screening
• Bartender cut-off protocol
• Capacity management
• Known troublemaker list

CENTER — CENTRAL EVENT:
• Bar Brawl

RIGHT SIDE — CONSEQUENCES:
• Physical injuries
• Property damage
• Legal liability
• License revocation

REACTIVE CONTROLS (barriers on right):
• Bouncer physical intervention
• Police/EMS call
• Bystander evacuation
• Camera footage preservation"""
        },
        {
            "heading": "PAGE 7 — THE MATH OF FAILURE",
            "content": """DESHAWN
So how do you know if you've got enough controls?

MARCUS
You assign probabilities. Say the chance of a drunk getting aggressive is 30% on a Saturday night. My ID check catches 80% of them. That means 20% slip through. So the residual probability of that threat reaching the central event is...

He scribbles on the napkin.

MARCUS (CONT'D)
0.30 times 0.20 equals 0.06. Six percent. Not bad. But if my ID check degrades — say I'm distracted, or short-staffed — that 80% drops to 50%. Now it's 0.30 times 0.50. Fifteen percent. More than double.

DESHAWN
And on the other side?

MARCUS
Same math. If the brawl happens and my radio works, I've got a 90% chance of containing it in under two minutes. Radio dies? That drops to 40%. The consequence pathway probability just more than doubled because of one escalation factor."""
        },
        {
            "heading": "PAGE 8 — REDUNDANCY AND INDEPENDENCE",
            "content": """MARCUS
Here's the key insight, kid. The controls have to be INDEPENDENT. If one fails, the others still hold.

DESHAWN
What do you mean?

MARCUS
If my ID check AND my bartender cut-off both depend on the same guy — say I've got one bouncer doing both — then one failure takes out two controls simultaneously. That's a common cause failure. The bow tie falls apart.

He draws two X marks connected by a single line.

MARCUS (CONT'D)
But if the ID check is me, the cut-off is the bartender, and the capacity count is the door clicker — three independent people, three independent controls — then the probability of ALL three failing is the product of their individual failure rates.

DESHAWN
So like... 0.2 times 0.1 times 0.15...

MARCUS
(impressed)
0.003. Three in a thousand. Now you're thinking like a risk analyst."""
        },
        {
            "heading": "PAGE 9 — THE REAL-WORLD TEST",
            "content": """A BLACK SUV pulls up. Four large men in matching jackets step out. Marcus straightens up.

MARCUS
(quietly)
Watch. This is a live bow tie scenario. Four guys, same crew, already amped up. Threat pathway is active.

He keys his radio.

MARCUS (CONT'D)
(into radio)
Tony, four-top crew arriving. Possible prior history. Eyes on pool table section. Bartender — flag me at drink three for this group.

(to Deshawn)
I just activated three preventative controls simultaneously. Surveillance, early cut-off trigger, and zone monitoring. If any of those fail, I've still got the reactive side ready.

DESHAWN
And if your radio dies?

MARCUS
(pulls out his phone)
Backup communication channel. That's how you mitigate an escalation factor — you build redundancy into the system.

He winks."""
        },
        {
            "heading": "PAGE 10 — THE LESSON",
            "content": """The crew enters without incident. The night continues. Marcus leans against the wall.

MARCUS
Every night is a bow tie, kid. Threats on the left, consequences on the right, and the event we're trying to prevent sitting right in the middle. Our job isn't to eliminate risk — that's impossible. Our job is to stack enough independent barriers on both sides that the probability of a bad outcome drops to something we can live with.

DESHAWN
(looking at the napkin)
This is... actually kind of elegant.

MARCUS
(smiling)
ISO 31010, Section B.4.2. Bow Tie Analysis. They teach it in boardrooms with PowerPoints. We teach it on the door with cocktail napkins.

He folds the napkin and hands it to Deshawn.

MARCUS (CONT'D)
Keep it. Study it. Because tomorrow night, YOU'RE running the left side.

Deshawn looks at the napkin, then at the line of people waiting to get in. He nods.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Decision Tree Analysis"] = {
    "title": "Decision Tree Analysis: The Hustler's Gambit",
    "iso_section": "B.9.3",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — EXT. CORNER BODEGA — DAY",
            "content": """FADE IN:

A hot summer afternoon. RICO (30s, sharp eyes, gold chain, always calculating) sits on a milk crate outside a bodega. His friend JAYLEN (20s, nervous, pacing) approaches.

JAYLEN
Yo Rico, I got a problem. I owe Manny twelve hundred for that shipment. I got the cash but if I pay him now, I'm broke for two weeks. If I dodge him...

RICO
(cutting him off)
Sit down. You're about to make a decision based on feelings. That's how people end up in trunks. We're gonna do this with math."""
        },
        {
            "heading": "PAGE 2 — THE DECISION NODE",
            "content": """Rico pulls a pen from behind his ear and flattens a brown paper bag on the crate.

RICO
First thing — you got a Decision Node. That's you, right now, with a choice to make. I draw it as a square.

He draws a small square.

RICO (CONT'D)
Two branches come off that square. Branch one: Pay Manny now. Branch two: Dodge Manny.

JAYLEN
That's it?

RICO
That's the start. But each branch leads to more nodes — Chance Nodes. Those are circles. They represent what MANNY does next, and you don't control that. You can only estimate the probabilities."""
        },
        {
            "heading": "PAGE 3 — BRANCH ONE: PAY NOW",
            "content": """RICO
Let's map Branch One. You pay Manny the twelve hundred today.

He draws the branch and a circle at the end.

RICO (CONT'D)
Chance node: What happens next? Two possibilities. One — Manny's happy, gives you priority on the next shipment. I'd say that's an 85% chance. The value of that? You make back two grand in a week. Net outcome: positive eight hundred.

JAYLEN
And the other?

RICO
Two — Manny takes the money and ghosts you anyway. Fifteen percent chance. You're out twelve hundred with nothing to show. Net outcome: negative twelve hundred.

He writes the numbers on each branch.

RICO (CONT'D)
So the Expected Value of paying now is: 0.85 times 800, plus 0.15 times negative 1200. That's 680 minus 180. Equals positive 500."""
        },
        {
            "heading": "PAGE 4 — BRANCH TWO: DODGE",
            "content": """RICO
Now Branch Two. You dodge Manny. Keep the twelve hundred in your pocket.

He draws the second main branch with another circle.

RICO (CONT'D)
Chance node: Manny's reaction. Three possibilities now. One — Manny doesn't care, moves on. Maybe 20% chance. You keep your twelve hundred. Net outcome: positive twelve hundred.

JAYLEN
That sounds good.

RICO
Hold on. Two — Manny sends someone to collect, adds a 50% penalty. That's 40% likely. Now you owe eighteen hundred. Net outcome: negative eighteen hundred.

JAYLEN
And three?

RICO
Three — Manny cuts you off permanently. No more supply. 40% chance. You keep the twelve hundred but lose your income stream. Long-term net outcome: negative five thousand over six months."""
        },
        {
            "heading": "PAGE 5 — CALCULATING EXPECTED VALUE",
            "content": """Rico writes out the math carefully.

RICO
Expected Value of dodging: 0.20 times 1200, plus 0.40 times negative 1800, plus 0.40 times negative 5000.

He calculates.

RICO (CONT'D)
That's 240, minus 720, minus 2000. Total: negative 2,480.

He circles both expected values.

RICO (CONT'D)
Pay now: positive 500. Dodge: negative 2,480. The decision tree just told you the answer. It's not even close.

JAYLEN
(staring at the bag)
Damn. When you lay it out like that...

RICO
That's the whole point. Your gut said "keep the cash." The tree says "pay the man." Your gut doesn't do multiplication."""
        },
        {
            "heading": "PAGE 6 — SEQUENTIAL DECISIONS",
            "content": """JAYLEN
But what if I pay him and THEN he ghosts me? What do I do then?

RICO
Good. Now you're thinking in sequences. That's what makes a decision tree powerful — it handles chains of decisions.

He extends the "Manny ghosts" branch with another square.

RICO (CONT'D)
New decision node: If Manny ghosts after you pay, you've got two new choices. One — find a new supplier. Two — confront Manny.

JAYLEN
Each of those has its own chances too?

RICO
Exactly. New supplier: 60% chance you find one in a week, 40% chance it takes a month. Confront Manny: 30% chance he makes it right, 70% chance it gets ugly. Every branch keeps splitting until you hit a terminal node — a final outcome with a dollar value."""
        },
        {
            "heading": "PAGE 7 — ROLLING BACK THE TREE",
            "content": """RICO
Here's the trick though. You don't solve a decision tree forward. You solve it BACKWARD. It's called "rolling back" or "folding back."

JAYLEN
Backward?

RICO
You start at the terminal nodes — the endpoints — and work your way back to the root. At every chance node, you calculate the expected value. At every decision node, you pick the branch with the HIGHEST expected value.

He traces his finger from the tips of the branches back toward the root.

RICO (CONT'D)
By the time you get back to your original square — your first decision — every branch has been evaluated. The optimal path lights up like a highway. You just follow it.

JAYLEN
So the tree tells you the best move at EVERY step, not just the first one?

RICO
Now you're getting it. It's a complete strategy, not just a single choice."""
        },
        {
            "heading": "PAGE 8 — SENSITIVITY CHECK",
            "content": """JAYLEN
But what if my probabilities are wrong? I'm just guessing that Manny ghosts 15% of the time.

RICO
Smart question. That's called sensitivity analysis. You test how much the answer changes when you change the inputs.

He rewrites the pay-now calculation with different numbers.

RICO (CONT'D)
Say Manny's ghost probability isn't 15% — say it's 30%. Now the expected value of paying is: 0.70 times 800 plus 0.30 times negative 1200. That's 560 minus 360. Equals positive 200.

JAYLEN
Still positive.

RICO
Right. And the dodge path is still deeply negative. So even if your estimates are off by double, the decision doesn't change. That means your answer is ROBUST. If a small change in probability flipped the answer, you'd need to be more careful. But this one's solid."""
        },
        {
            "heading": "PAGE 9 — THE INFORMATION VALUE",
            "content": """JAYLEN
What if I could find out for sure whether Manny would ghost me?

RICO
Ah, now you're talking about the Value of Perfect Information. If you KNEW Manny's move before deciding, how much more would you make?

He thinks for a moment.

RICO (CONT'D)
With perfect info: if Manny's legit (85%), you pay and make 800. If he'd ghost (15%), you dodge and keep 1200. Expected value with perfect info: 0.85 times 800 plus 0.15 times 1200 equals 680 plus 180 equals 860.

JAYLEN
And without perfect info, the best was 500.

RICO
So perfect information is worth 860 minus 500 equals 360 dollars. That means if someone could tell you Manny's true intentions for less than 360 bucks, it's worth paying for that intel.

JAYLEN
(laughing)
You're telling me to pay for a snitch?

RICO
I'm telling you information has a calculable value. Whether you buy it from a snitch or earn it from experience — that's your call."""
        },
        {
            "heading": "PAGE 10 — THE DECISION",
            "content": """Jaylen stares at the paper bag covered in branches, numbers, and circles. He takes a deep breath.

JAYLEN
I'm paying Manny.

RICO
(nodding)
The tree doesn't lie, brother. Every branch, every probability, every outcome — it all points the same direction.

He folds the bag.

RICO (CONT'D)
ISO 31010, Section B.9.3. Decision Tree Analysis. They use it in hospitals to decide on surgeries. In oil companies to decide where to drill. We use it on a milk crate to decide whether to pay a supplier.

JAYLEN
Same math though.

RICO
Same math. Different stakes. But the logic? Universal.

Jaylen pulls out an envelope of cash, counts it, and heads down the block. Rico watches him go, then pulls out a fresh paper bag and starts sketching a new tree — this one for himself.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Monte Carlo Simulation"] = {
    "title": "Monte Carlo Simulation: The Mechanic's Odds",
    "iso_section": "B.5.10",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — INT. AUTO REPAIR SHOP — DAY",
            "content": """FADE IN:

A grimy auto shop. Engine parts everywhere. VINCE (50s, oil-stained hands, cigarette behind ear, knows every engine ever made) leans against a workbench. TERRELL (30s, impatient, car keys jangling) stands across from him.

TERRELL
Just patch the head gasket, Vince. I don't need a full rebuild. I need the car running by Friday.

VINCE
(wiping hands on a rag)
I can patch it. But I'm not gonna. And I'm gonna tell you why with math, not feelings."""
        },
        {
            "heading": "PAGE 2 — THE PROBLEM WITH SINGLE ESTIMATES",
            "content": """VINCE
You want a quick fix. You're thinking: patch it, it holds, I drive. One outcome. One straight line. But that's not how engines work. That's not how ANYTHING works.

TERRELL
What do you mean?

VINCE
I mean there's not one future for your car. There's a thousand futures. And most of them end with you on the side of the highway at 2 AM.

He grabs a clipboard.

VINCE (CONT'D)
See, a single estimate — "it'll probably be fine" — is worthless. What you need is a probability distribution. A picture of ALL the possible outcomes and how likely each one is. That's what Monte Carlo simulation gives you."""
        },
        {
            "heading": "PAGE 3 — THE RANDOM VARIABLES",
            "content": """Vince draws three columns on the clipboard.

VINCE
Your engine's fate depends on three random variables. Things I can't predict exactly, but I can estimate their ranges.

He labels them:

VINCE (CONT'D)
Variable one: Part Wear Rate. That patched gasket could last anywhere from 2,000 to 15,000 miles. Most likely around 6,000. That's not a fixed number — it's a distribution. Bell-shaped, skewed toward the low end because it's a patch, not a replacement.

TERRELL
Okay...

VINCE
Variable two: Your Driving Habits. You drive like a normal person? Or do you floor it on the highway? I'd estimate your stress factor ranges from 0.8 (gentle) to 1.5 (aggressive). Based on those bald tires, I'm guessing you skew high.

TERRELL
(defensive)
I drive normal.

VINCE
Sure. Variable three: Weather and Temperature. Summer heat expands metal. Winter cold contracts it. Temperature cycling ranges from mild to severe depending on the season. Each cycle stresses the patch."""
        },
        {
            "heading": "PAGE 4 — RUNNING THE SIMULATION",
            "content": """VINCE
Now here's what I do. In my head — and I've been doing this for thirty years — I run the simulation. Not once. Not twice. A hundred times.

TERRELL
A hundred times?

VINCE
Each time, I randomly pick a value for each variable from its range. Random gasket life. Random driving stress. Random weather pattern. Then I calculate: does the engine survive 12 months?

He starts scribbling.

VINCE (CONT'D)
Iteration one: Gasket lasts 8,000 miles, you drive gentle, mild winter. Engine survives. Iteration two: Gasket lasts 3,000 miles, you drive hard, brutal summer. Engine fails at month four. Iteration three: Gasket lasts 6,000, moderate driving, average weather. Fails at month nine.

TERRELL
You're just making up numbers.

VINCE
I'm SAMPLING from distributions. There's a difference. Each iteration is equally possible. The magic is in the aggregate."""
        },
        {
            "heading": "PAGE 5 — THE PROBABILITY DISTRIBUTION",
            "content": """Vince flips the clipboard and draws a rough histogram.

VINCE
After a hundred iterations, I stack up the results. How many times did the engine last 12 months? How many times did it fail at 6? At 3? At 1?

He draws bars of different heights.

VINCE (CONT'D)
Out of my hundred mental simulations: 14 times the engine survived the full year. 28 times it failed between 6 and 12 months. 38 times it failed between 3 and 6 months. And 20 times? It failed in under 3 months.

TERRELL
So there's only a 14% chance it lasts?

VINCE
Fourteen percent. And an 86% chance you're back here — or worse, at a tow yard — within the year. That's not a guess. That's a probability distribution built from a hundred scenarios."""
        },
        {
            "heading": "PAGE 6 — PERCENTILES AND CONFIDENCE",
            "content": """VINCE
Let me give you the percentiles. The P10 — meaning 90% of outcomes are worse than this — is about 2 months. The P50 — the median — is about 5 months. The P90 — only 10% of outcomes are better — is 11 months.

TERRELL
What does that mean in English?

VINCE
It means if you're an optimist, you've got maybe 11 months. If you're a realist, you've got 5. And if Murphy's Law shows up — which it does, regularly — you've got 2.

He taps the histogram.

VINCE (CONT'D)
The question isn't "will it fail?" The question is "when." And Monte Carlo just told you the answer is probably sooner than you want."""
        },
        {
            "heading": "PAGE 7 — SENSITIVITY: WHAT MATTERS MOST",
            "content": """TERRELL
What if I drive really carefully? Does that change things?

VINCE
Good instinct. That's sensitivity analysis — figuring out which variable has the most impact on the outcome.

He redraws the chart with the driving stress locked at 0.8 (gentle).

VINCE (CONT'D)
If I fix your driving at gentle and re-run the simulation... survival rate goes from 14% to about 31%. Better, but still a coin flip you lose.

TERRELL
What about the gasket quality?

VINCE
If I upgrade the patch to a better sealant — shifting the gasket life distribution from 2,000-15,000 to 5,000-20,000 — survival jumps to 48%. THAT variable moves the needle the most. It's the dominant risk driver.

TERRELL
So the patch material matters more than how I drive?

VINCE
By a factor of two. Monte Carlo doesn't just tell you the odds — it tells you WHERE to spend your money to change them."""
        },
        {
            "heading": "PAGE 8 — THE COST COMPARISON",
            "content": """VINCE
Now let's talk dollars. The patch costs you $400. The full rebuild costs $2,200. Sounds like a no-brainer, right? Patch is cheaper.

TERRELL
That's what I'm saying.

VINCE
But Monte Carlo says there's an 86% chance the patch fails within a year. When it fails, you're looking at a tow ($200), emergency repair ($1,800), plus rental car ($600). Total failure cost: $2,600.

He writes the expected values.

VINCE (CONT'D)
Expected cost of the patch: $400 plus 0.86 times $2,600 equals $400 plus $2,236 equals $2,636. Expected cost of the rebuild: $2,200 plus 0.05 times $800 (small chance of minor issues) equals $2,240.

TERRELL
(long pause)
The patch is actually MORE expensive?

VINCE
By almost four hundred bucks. The cheap option is the expensive option. Monte Carlo sees through the illusion."""
        },
        {
            "heading": "PAGE 9 — CONVERGENCE",
            "content": """TERRELL
How do you know a hundred simulations is enough? What if you ran a thousand?

VINCE
(grinning)
Now you're asking the right question. That's about convergence. Early on — say ten iterations — the results bounce around. You might get 30% survival or 5%. It's noisy.

He draws a line that wobbles wildly at first, then smooths out.

VINCE (CONT'D)
But as you add more iterations, the average stabilizes. By fifty runs, it's settling. By a hundred, it's steady. By a thousand, you're just adding decimal places. The distribution has converged.

TERRELL
So a hundred is good enough?

VINCE
For this? Yeah. If we were designing a bridge, I'd want ten thousand. The stakes determine the precision. But for your Honda? A hundred mental iterations gives me confidence in the answer."""
        },
        {
            "heading": "PAGE 10 — THE VERDICT",
            "content": """Terrell leans against his car, arms crossed, staring at the clipboard full of histograms and numbers.

TERRELL
(sighing)
Do the rebuild.

VINCE
(nodding)
Smart. You just made a decision based on a probability distribution instead of a gut feeling. That's the difference between gambling and calculating.

He tosses the rag over his shoulder.

VINCE (CONT'D)
ISO 31010, Section B.5.10. Monte Carlo Simulation. NASA uses it to plan missions. Banks use it to price derivatives. I use it to save guys like you from blowing a head gasket on I-95.

TERRELL
You should charge more.

VINCE
(laughing)
I charge exactly what the distribution says I'm worth. Keys on the counter. I'll have it done by Tuesday.

Terrell drops the keys. Vince picks them up, pops the hood, and gets to work.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Game Theory"] = {
    "title": "Game Theory: The Roommate's Dilemma",
    "iso_section": "B.9.4",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — INT. APARTMENT LIVING ROOM — NIGHT",
            "content": """FADE IN:

A cramped apartment. Pizza boxes and textbooks everywhere. OMAR (20s, pre-law student, thinks three moves ahead) sits at the kitchen table. His roommate KYLE (20s, impulsive, panicking) bursts through the door.

KYLE
We're screwed. Landlord found out about the dog. And the sublet. And the wall we knocked down.

OMAR
(calm)
I know. He called me too. Sit down.

KYLE
He said whoever tells him the full story first gets to keep the lease. The other one gets evicted AND sued for damages.

OMAR
(nodding slowly)
He's running the Prisoner's Dilemma on us. And he's counting on us being stupid."""
        },
        {
            "heading": "PAGE 2 — THE PAYOFF MATRIX",
            "content": """Omar clears the table and grabs a notebook.

OMAR
Let me show you something. This is a payoff matrix. It's the foundation of game theory.

He draws a 2x2 grid.

OMAR (CONT'D)
Two players: you and me. Two strategies each: Stay Quiet or Snitch. Four possible outcomes.

He fills in the grid:

OMAR (V.O.)
If we BOTH stay quiet: Landlord has no proof. Minor fine, we both keep the lease. Call it negative 500 each.

If I snitch and you stay quiet: I keep the lease, you get evicted and sued. I get zero, you get negative 5,000.

If you snitch and I stay quiet: You get zero, I get negative 5,000.

If we BOTH snitch: Landlord has full info, evicts us both but with reduced penalties since we cooperated. Negative 2,000 each.

KYLE
(staring at the grid)
So the best outcome is if we both shut up."""
        },
        {
            "heading": "PAGE 3 — THE DOMINANT STRATEGY TRAP",
            "content": """OMAR
You'd think so. But here's the trap. Look at it from YOUR perspective only.

He highlights Kyle's column.

OMAR (CONT'D)
If I stay quiet, your best move is to snitch. You get zero instead of negative 500. If I snitch, your best move is STILL to snitch. You get negative 2,000 instead of negative 5,000.

KYLE
So snitching is always better for me?

OMAR
That's called a Dominant Strategy. No matter what I do, snitching gives you a better individual outcome. And guess what? The same logic applies to me. My dominant strategy is also to snitch.

KYLE
So we both snitch?

OMAR
If we both follow our dominant strategies, we both snitch and we both get negative 2,000. But if we'd both stayed quiet, we'd only lose 500 each. The "rational" individual choice leads to a WORSE collective outcome. That's the dilemma."""
        },
        {
            "heading": "PAGE 4 — NASH EQUILIBRIUM",
            "content": """OMAR
The outcome where we both snitch? That's called the Nash Equilibrium. Named after John Nash — the Beautiful Mind guy.

KYLE
What makes it an equilibrium?

OMAR
It's the outcome where neither player can improve their position by changing strategy alone. If we're both snitching and I switch to staying quiet, I go from negative 2,000 to negative 5,000. Worse. Same for you. So neither of us has an incentive to deviate.

He circles the both-snitch cell.

OMAR (CONT'D)
The Nash Equilibrium is STABLE, but it's not OPTIMAL. The both-quiet outcome is better for everyone, but it's not stable — because each of us is tempted to defect.

KYLE
That's messed up.

OMAR
That's math. Individual rationality and collective rationality are different things. Game theory shows you exactly where they diverge."""
        },
        {
            "heading": "PAGE 5 — WHY COOPERATION WORKS",
            "content": """KYLE
So what do we do? Just accept the bad outcome?

OMAR
No. We change the game. See, the classic Prisoner's Dilemma assumes a ONE-SHOT game. You play once, never see each other again. In that case, snitching is rational.

KYLE
But we live together.

OMAR
Exactly. This isn't one-shot. This is a REPEATED game. We're gonna deal with this landlord — or the next one — for years. And in repeated games, cooperation becomes the optimal strategy.

He writes on the notebook:

OMAR (V.O.)
One-shot game: Snitch (dominant strategy)
Repeated game: Cooperate (optimal long-term strategy)

OMAR (CONT'D)
In a repeated game, I can punish you for snitching in future rounds. And you can punish me. That threat of retaliation changes the math entirely."""
        },
        {
            "heading": "PAGE 6 — TIT FOR TAT",
            "content": """OMAR
The best strategy for repeated games was discovered by a political scientist named Robert Axelrod. It's called Tit for Tat.

KYLE
Sounds aggressive.

OMAR
It's actually the opposite. The rules are simple: Start by cooperating. Then, in every subsequent round, do whatever the other player did last round. If they cooperated, you cooperate. If they defected, you defect. Then forgive and go back to cooperating if they do.

KYLE
So it's... nice but not a pushover?

OMAR
Exactly. It's nice — it starts with cooperation. It's retaliatory — it punishes defection immediately. It's forgiving — it returns to cooperation as soon as the other player does. And it's clear — the other player always knows what to expect.

He taps the notebook.

OMAR (CONT'D)
In Axelrod's tournament, Tit for Tat beat every other strategy. The simplest approach won because it built trust while maintaining deterrence."""
        },
        {
            "heading": "PAGE 7 — THE COMMITMENT DEVICE",
            "content": """KYLE
Okay but how do I KNOW you won't snitch? You just showed me it's in your self-interest.

OMAR
Fair. That's the trust problem. In game theory, you solve it with a Commitment Device — something that makes defection costly for me, so you can trust my cooperation.

KYLE
Like what?

OMAR
Like this. I'm going to text you right now: "I, Omar, confirm that we both agreed to stay quiet about the lease violations." Screenshot it.

KYLE
Why?

OMAR
Because if I snitch to the landlord after sending that text, you've got proof I was involved too. My snitch loses its value because I've implicated myself. I've made my own defection costly. That's a credible commitment.

He sends the text. Kyle's phone buzzes.

OMAR (CONT'D)
Now we're not relying on trust. We're relying on aligned incentives. That's stronger."""
        },
        {
            "heading": "PAGE 8 — THE LANDLORD'S STRATEGY",
            "content": """KYLE
Wait — what about the landlord? He's a player too.

OMAR
(impressed)
Now you're thinking in multi-player games. Yes. The landlord designed this situation deliberately. He's using a mechanism called "divide and conquer." By offering a deal to the first snitch, he's trying to break our coalition.

He adds the landlord to the diagram.

OMAR (CONT'D)
His optimal outcome: one of us snitches, he gets full information, evicts the guilty party, and keeps the other as a grateful tenant who'll never break rules again. His worst outcome: we both stay quiet and he has to actually investigate, which costs him time and money.

KYLE
So our silence is actually expensive for HIM?

OMAR
Very. If we both stay quiet, his expected cost of investigation is maybe $2,000 in legal fees and time. If one of us snitches, his cost drops to zero. He's trying to externalize his investigation costs onto our relationship."""
        },
        {
            "heading": "PAGE 9 — THE COUNTER-PLAY",
            "content": """OMAR
So here's our counter-strategy. We both stay quiet. But we don't just stonewall — we go to him together with a unified front.

KYLE
And say what?

OMAR
We acknowledge the violations. We offer to fix the wall, re-home the dog, and end the sublet. We present a remediation plan. This changes the game from adversarial to cooperative.

He redraws the payoff matrix with the new option.

OMAR (CONT'D)
New outcome: Landlord gets his problems fixed at zero cost to him. We keep the lease with a warning. Maybe a small fine. Call it negative 800 each — better than any outcome in the original matrix except the one where we snitch on each other.

KYLE
And the landlord goes for this because...

OMAR
Because finding new tenants costs him two months of vacancy plus turnover costs. About $4,000. Our remediation plan saves him money. We've turned a zero-sum game into a positive-sum game. Everyone wins."""
        },
        {
            "heading": "PAGE 10 — THE LESSON",
            "content": """Kyle sits back, looking at the notebook full of matrices and strategies.

KYLE
So the whole time, the answer wasn't about snitching or not snitching. It was about changing the game.

OMAR
(smiling)
That's the deepest lesson in game theory. If the game has a bad equilibrium, don't play the game. Change the rules, change the players, change the payoffs. Redesign the incentive structure.

He closes the notebook.

OMAR (CONT'D)
ISO 31010, Section B.9.4. Game Theory. They use it in nuclear deterrence, auction design, and antitrust law. We just used it to save our apartment.

KYLE
I'm switching my major to econ.

OMAR
(laughing)
Start with the payoff matrix. Everything else is just footnotes.

Omar picks up his phone and dials the landlord. Kyle sits beside him, united front. The camera pulls back as we hear Omar's calm, strategic voice begin the negotiation.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Layers of Protection Analysis (LOPA)"] = {
    "title": "LOPA: The Heist Planner's Calculus",
    "iso_section": "B.4.4",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — INT. WAREHOUSE BACK ROOM — NIGHT",
            "content": """FADE IN:

A dimly lit warehouse. A single bulb hangs over a folding table covered in blueprints. FRANK (50s, silver hair, meticulous, speaks like a professor) stands at the head. Around the table: NINA (30s, tech specialist), DARIUS (40s, muscle), and PETE (20s, the driver, nervous).

FRANK
(tapping the blueprint)
The target is a private vault in the basement of the Meridian Building. Contents: bearer bonds, estimated value two point four million. But before anyone gets excited, we need to talk about why we're probably NOT doing this job.

PETE
Wait, what?

FRANK
I said probably. Let's do the math first."""
        },
        {
            "heading": "PAGE 2 — THE INITIATING EVENT",
            "content": """FRANK
In Layers of Protection Analysis, everything starts with an Initiating Event. That's the thing that kicks off the scenario. For us, the initiating event is: we attempt to breach the building.

He writes on a whiteboard:

FRANK (CONT'D)
The frequency of the initiating event is once — because we're only doing this once. So we set it at 1.0. One attempt.

NINA
And then?

FRANK
And then we hit the protection layers. Each one is an Independent Protection Layer — an IPL. Each one has a Probability of Failure on Demand — a PFD. Our job is to calculate whether the overall probability of getting caught is low enough to be... tolerable.

DARIUS
What's tolerable?

FRANK
Less than one in ten thousand. If the math says our chance of getting caught is higher than that, we walk away. No exceptions."""
        },
        {
            "heading": "PAGE 3 — LAYER ONE: THE CAMERAS",
            "content": """FRANK
Layer one: the camera system. Sixteen cameras, full coverage, monitored by a security company off-site.

He looks at Nina.

FRANK (CONT'D)
Nina, what's the PFD?

NINA
I can loop the feeds for approximately 45 minutes using a signal intercept on their wireless backhaul. But there's a 1-in-20 chance the security company notices the loop — they run random spot checks.

FRANK
So the PFD — the probability that this layer FAILS to stop us — is 19 out of 20. We get through 95% of the time. But the probability it CATCHES us is 1 in 20. We write that as 0.05.

He writes: IPL 1 (Cameras) — PFD = 5 × 10⁻²

FRANK (CONT'D)
But remember — we need the layer to FAIL for us to succeed. So from our perspective, 0.95 is our pass-through rate. From the security's perspective, 0.05 is their detection rate."""
        },
        {
            "heading": "PAGE 4 — LAYER TWO: THE GUARDS",
            "content": """FRANK
Layer two: two armed guards. One in the lobby, one patrolling floors. Twelve-minute rotation cycle.

DARIUS
I can handle the guards.

FRANK
I know you can. But "handling" isn't the question. The question is: what's the probability they detect us despite our countermeasures?

He thinks.

FRANK (CONT'D)
We enter during the rotation gap — a 3-minute window. If our timing is perfect, detection probability is about 1 in 50. But timing depends on external factors — elevator delays, bathroom breaks, radio checks. Realistically, I'd put detection at 1 in 25.

He writes: IPL 2 (Guards) — PFD = 4 × 10⁻²

NINA
That's pretty good.

FRANK
Individually, yes. But LOPA doesn't care about individual layers. It cares about the product."""
        },
        {
            "heading": "PAGE 5 — LAYER THREE: THE VAULT DOOR",
            "content": """FRANK
Layer three: the vault itself. Reinforced steel, electronic keypad with biometric backup, time-lock that only opens during business hours.

PETE
So we go during business hours?

FRANK
No. Nina bypasses the time-lock remotely. But the biometric is the problem.

NINA
I've got a workaround — a cloned fingerprint from the building manager's gym membership card. It's not perfect. I'd give it a 70% chance of working on the first try, 85% within three tries.

FRANK
And if it fails all three times?

NINA
The system locks out and triggers a silent alarm. Response time: four minutes.

FRANK
So the probability this layer stops us — detection via lockout and alarm — is about 15%. Or 1.5 × 10⁻¹.

He writes: IPL 3 (Vault Door) — PFD = 1.5 × 10⁻¹"""
        },
        {
            "heading": "PAGE 6 — LAYER FOUR: THE SILENT ALARM",
            "content": """FRANK
Layer four: even if we get into the vault, there's a pressure-sensitive floor mat inside. Step on it wrong, silent alarm triggers. Different system from the vault lockout — independent circuit.

DARIUS
Can we disable it?

NINA
I can identify the circuit, but I can't guarantee I'll find it before someone steps on it. I'd say 1 in 10 chance it catches us.

FRANK
So PFD = 1 × 10⁻¹.

He writes: IPL 4 (Pressure Alarm) — PFD = 1 × 10⁻¹

FRANK (CONT'D)
Now. The critical principle of LOPA: each layer must be INDEPENDENT. If the cameras and the pressure alarm run on the same system, they're not independent — one failure could take out both, or one success could catch us twice. But they're on separate circuits, separate monitoring. So we can multiply."""
        },
        {
            "heading": "PAGE 7 — THE MULTIPLICATION",
            "content": """Frank steps back and looks at the whiteboard.

FRANK
Here's the LOPA calculation. The overall probability of getting caught is the initiating event frequency times the product of each layer's detection probability.

He writes:

FRANK (V.O.)
P(caught) = f(IE) × PFD₁ × PFD₂ × PFD₃ × PFD₄
P(caught) = 1.0 × 0.05 × 0.04 × 0.15 × 0.10

He calculates step by step.

FRANK (CONT'D)
0.05 times 0.04 is 0.002. Times 0.15 is 0.0003. Times 0.10 is 0.00003. That's 3 × 10⁻⁵. Or about 1 in 33,000.

The room is silent.

PETE
That's... really low.

FRANK
It's below our threshold of 1 in 10,000. Mathematically, the risk is tolerable.

DARIUS
So we're doing it?

FRANK
(holding up a finger)
I said mathematically. We haven't stress-tested the assumptions yet."""
        },
        {
            "heading": "PAGE 8 — STRESS-TESTING THE LAYERS",
            "content": """FRANK
LOPA requires us to verify that each layer is truly independent and that our PFD estimates are conservative. Let's challenge them.

He points to each layer.

FRANK (CONT'D)
Cameras: Nina, what if they've upgraded to AI-based anomaly detection since your last recon?

NINA
(pausing)
That would change the PFD from 0.05 to maybe 0.20.

FRANK
Guards: what if they've added a third guard we don't know about?

DARIUS
Detection goes from 0.04 to maybe 0.10.

FRANK
Let's recalculate with degraded assumptions. 1.0 times 0.20 times 0.10 times 0.15 times 0.10.

He writes:

FRANK (CONT'D)
0.20 times 0.10 is 0.02. Times 0.15 is 0.003. Times 0.10 is 0.0003. That's 3 × 10⁻⁴. Or 1 in 3,333.

PETE
That's above the threshold.

FRANK
Exactly. Under degraded assumptions, the risk is no longer tolerable. Which means our decision depends entirely on the quality of our intelligence."""
        },
        {
            "heading": "PAGE 9 — THE GO/NO-GO DECISION",
            "content": """FRANK
So here's where we are. Best case: 1 in 33,000. Worst case: 1 in 3,333. The truth is somewhere in between.

He draws a line between the two numbers.

FRANK (CONT'D)
LOPA gives us a framework, not a guarantee. If we can verify — with fresh recon — that the cameras haven't been upgraded and there's no third guard, we're in the tolerable zone. If we can't verify, we're gambling.

NINA
I can do another site visit. Two days.

FRANK
Do it. And while you're there, check for any fifth layer we might have missed. A hidden sensor, a secondary vault lock, anything. Because in LOPA, the layer you don't know about is the one that gets you caught.

DARIUS
And if everything checks out?

FRANK
Then the math says go. And I trust the math more than I trust my gut.

He caps the marker."""
        },
        {
            "heading": "PAGE 10 — THE PRINCIPLE",
            "content": """The team studies the whiteboard in silence. Frank leans against the wall.

FRANK
Every security system in the world is built on layers. Banks, nuclear plants, data centers — they all use the same principle. Stack enough independent barriers and the probability of a breach drops to near zero.

PETE
And we're trying to beat those layers.

FRANK
We're trying to QUANTIFY them. There's a difference. A thief who doesn't do LOPA just sees a vault and hopes for the best. We see four independent protection layers with measurable failure probabilities and a calculable overall risk.

He taps the whiteboard.

FRANK (CONT'D)
ISO 31010, Section B.4.4. Layers of Protection Analysis. Chemical plants use it to prevent explosions. We use it to decide whether a job is worth the risk.

NINA
And if the recon comes back bad?

FRANK
Then we walk. Because the math walked first.

He turns off the light over the table. The blueprints disappear into shadow.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Ishikawa (Fishbone) Analysis"] = {
    "title": "Ishikawa Analysis: The Food Truck Meltdown",
    "iso_section": "B.3.3",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — EXT. FOOD TRUCK LOT — AFTERNOON",
            "content": """FADE IN:

A food truck lot after the lunch rush. Trash blowing. CHEF RAY (50s, tattooed forearms, bandana, built the truck from nothing) stands with arms crossed, staring at a nearly full warming tray of unsold tacos. MIGUEL (20s, new cook, sauce-stained apron) shrinks against the truck.

CHEF RAY
You see that tray? That's two hundred dollars of food nobody bought. We served half our usual volume. The line was out to the street by noon and GONE by 12:15. You know what happened?

MIGUEL
The... the grill was slow?

CHEF RAY
The grill was ONE thing. But this wasn't one failure. This was a SYSTEM failure. And we're gonna dissect it like a fish."""
        },
        {
            "heading": "PAGE 2 — THE FISHBONE",
            "content": """Chef Ray grabs a piece of butcher paper and slaps it on the side of the truck. He draws a long horizontal arrow pointing right, with a box at the tip.

CHEF RAY
This arrow? That's the spine. The box at the end? That's the EFFECT — the problem we're trying to explain. Today's effect: "Lunch rush failure — 50% revenue loss."

He draws six diagonal lines branching off the spine, like ribs on a fish skeleton.

CHEF RAY (CONT'D)
These bones? These are the CAUSE CATEGORIES. In manufacturing they call them the 6Ms. In a food truck, same thing applies: Methods, Machinery, Materials, Manpower, Measurement, and Mother Nature — which I call Management and Environment.

MIGUEL
That's a lot of categories.

CHEF RAY
That's the point. When something goes wrong, people grab the first explanation they see. "The grill was slow." But a fishbone forces you to look at EVERY category. The root cause is usually hiding in the one you didn't check."""
        },
        {
            "heading": "PAGE 3 — METHODS",
            "content": """Chef Ray writes "METHODS" on the first bone.

CHEF RAY
Methods means HOW we do things. Our process. Our workflow. What went wrong with our methods today?

MIGUEL
I... I changed the order I prepped the stations.

CHEF RAY
Why?

MIGUEL
I thought it would be faster to prep the proteins first and the toppings last.

CHEF RAY
And what happened?

MIGUEL
The toppings weren't ready when the first orders came in. So I was chopping cilantro while tickets were piling up.

Chef Ray draws a sub-branch: "Prep sequence changed → toppings delayed → order backlog."

CHEF RAY
That's a methods failure. The process exists for a reason. You changed it without understanding the downstream dependencies. Every minute of topping delay cascaded into three minutes of order delay."""
        },
        {
            "heading": "PAGE 4 — MACHINERY",
            "content": """Chef Ray writes "MACHINERY" on the second bone.

CHEF RAY
Machinery. Equipment. Tools. What broke or underperformed?

MIGUEL
The flat-top grill was taking forever to heat up.

CHEF RAY
Because?

MIGUEL
I don't know. It just seemed slow.

Chef Ray walks to the grill, runs his finger along the burner ports. They're clogged with grease.

CHEF RAY
When's the last time you cleaned the burner ports?

MIGUEL
(silence)

CHEF RAY
The ports are clogged. Gas flow is restricted. Heat output drops by maybe 30%. That means every protein takes 40% longer to cook. On a normal day, we push 80 orders in an hour. Today? Maybe 50.

He draws: "Clogged burner ports → reduced heat → slower cook times → reduced throughput."

CHEF RAY (CONT'D)
That's not bad luck. That's a maintenance failure. Machinery doesn't fail randomly — it fails predictably when you skip the maintenance schedule."""
        },
        {
            "heading": "PAGE 5 — MATERIALS",
            "content": """Chef Ray writes "MATERIALS" on the third bone.

CHEF RAY
Materials. Ingredients. Supply quality. What came in wrong?

MIGUEL
The tortillas were different today. Thicker.

CHEF RAY
(nodding)
I noticed. Our usual supplier was out, so the backup sent a different brand. Thicker tortillas take longer on the grill, absorb more sauce, and change the texture. Customers notice.

He draws: "Substitute tortillas → longer grill time → taste deviation → customer complaints."

CHEF RAY (CONT'D)
Three people sent back tacos today. Three. In two years, I've had maybe five send-backs total. That's a materials-driven quality failure.

MIGUEL
But we couldn't control the supplier being out.

CHEF RAY
We could have controlled our RESPONSE. We should have adjusted the grill temp for thicker tortillas and modified the sauce ratio. We didn't adapt because we didn't identify the variable. That's on us."""
        },
        {
            "heading": "PAGE 6 — MANPOWER",
            "content": """Chef Ray writes "MANPOWER" on the fourth bone.

CHEF RAY
Manpower. The people. Skills, training, staffing levels.

He looks at Miguel.

CHEF RAY (CONT'D)
No offense, kid, but you're three weeks in. You're still learning the rhythm. On a normal day, I've got Rosa on prep and you on assembly. Today, Rosa called in sick.

MIGUEL
So I was doing both.

CHEF RAY
One person doing two jobs at 70% efficiency each. That's not 140% output — that's maybe 50% of what two people produce. The throughput bottleneck wasn't just the grill. It was the human bandwidth.

He draws: "Single operator → split attention → prep delays + assembly errors → reduced output."

CHEF RAY (CONT'D)
And here's the compounding effect: your prep delay (Methods) hit at the same time as your reduced bandwidth (Manpower). Two causes on different bones, but they INTERSECTED at the same moment. That's how small failures become big ones."""
        },
        {
            "heading": "PAGE 7 — MEASUREMENT",
            "content": """Chef Ray writes "MEASUREMENT" on the fifth bone.

CHEF RAY
Measurement. How do we track what's happening in real time? What metrics did we miss?

MIGUEL
I wasn't really tracking anything. I was just trying to keep up.

CHEF RAY
Exactly. On a normal day, I check the ticket time every fifteen minutes. Average should be four minutes from order to serve. If it creeps past six, I adjust — simplify the menu, pre-batch proteins, whatever it takes.

He draws: "No real-time ticket monitoring → no early warning → no corrective action → full cascade."

CHEF RAY (CONT'D)
Today, nobody was watching the numbers. By the time we realized we were behind, the line had already bailed. Twelve customers walked away. At $14 average ticket, that's $168 in lost revenue just from the walkouts.

MIGUEL
We needed a thermometer for the process, not just the grill.

CHEF RAY
(pointing at him)
Now you're getting it. Measurement is the feedback loop. Without it, you're flying blind."""
        },
        {
            "heading": "PAGE 8 — MANAGEMENT / ENVIRONMENT",
            "content": """Chef Ray writes "MANAGEMENT" on the sixth bone.

CHEF RAY
Last bone. Management and environment. The stuff above our pay grade — or in this case, the stuff I should have handled.

MIGUEL
Like what?

CHEF RAY
Like the fact that I knew Rosa might call in sick — she texted me last night that she wasn't feeling great — and I didn't line up a backup. That's a management failure. I had a leading indicator and ignored it.

He draws: "No contingency staffing → single point of failure on prep → cascade."

CHEF RAY (CONT'D)
And environment: it's 95 degrees today. The truck's internal temp hit 115 by 11:30. Heat stress reduces cognitive performance by 15-20%. You were slower, I was slower, the equipment was hotter. Everything degraded.

He draws: "Extreme heat → equipment stress + human fatigue → compound performance loss."

CHEF RAY (CONT'D)
Management should have anticipated the heat and adjusted: earlier start, extra water breaks, simplified menu. I didn't. That's on me."""
        },
        {
            "heading": "PAGE 9 — TRACING TO ROOT CAUSES",
            "content": """Chef Ray steps back and looks at the full fishbone diagram on the butcher paper.

CHEF RAY
Now look at the whole picture. Six categories. Eleven individual causes. But they're not all equal.

He circles three items.

CHEF RAY (CONT'D)
The ROOT causes — the ones that triggered everything else — are these three: No contingency staffing (Management), skipped burner maintenance (Machinery), and changed prep sequence (Methods). Fix those three, and most of the other failures don't happen.

MIGUEL
The tortillas?

CHEF RAY
Secondary cause. If the grill was running right and the prep was on schedule, the thicker tortillas would have been a minor adjustment, not a crisis. Context determines severity.

He draws arrows from the three root causes to the other branches, showing the cascade.

CHEF RAY (CONT'D)
That's the power of the fishbone. It doesn't just list causes — it shows you the STRUCTURE of the failure. Which causes are roots, which are branches, and which are leaves. You fix the roots, the whole tree stabilizes."""
        },
        {
            "heading": "PAGE 10 — THE CORRECTIVE ACTIONS",
            "content": """Chef Ray tears the butcher paper off the truck and rolls it up.

CHEF RAY
Here's what changes starting tomorrow. One: burner ports get cleaned every night. Non-negotiable. Two: prep sequence goes back to the standard order — toppings first, proteins second. Three: I build a backup staffing list. Four: we track ticket times every ten minutes during rush.

MIGUEL
And the tortillas?

CHEF RAY
I'm calling the supplier tonight. But I'm also writing a spec sheet — thickness, diameter, moisture content — so any substitute meets our baseline. That's how you turn a materials failure into a materials STANDARD.

He hands Miguel the rolled-up fishbone.

CHEF RAY (CONT'D)
ISO 31010, Section B.3.3. Ishikawa Diagram. Also called Cause-and-Effect Analysis. Toyota uses it to build cars. We use it to sell tacos. Same logic: trace the effect back through every possible cause category until you find the roots.

MIGUEL
(holding the diagram)
I'll clean the burners tonight.

CHEF RAY
(clapping him on the shoulder)
That's a start. Now help me close up. Tomorrow we run it right.

They begin breaking down the truck as the sun sets over the lot.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Pareto Charts"] = {
    "title": "Pareto Charts: The Bartender's 80/20",
    "iso_section": "B.8.4",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — INT. DIVE BAR — LATE AFTERNOON",
            "content": """FADE IN:

A worn-in dive bar before the evening rush. Stools being wiped down. JACKIE (40s, no-nonsense, owns the place, seen everything) polishes glasses behind the bar. TOMMY (20s, new bartender, eager, overwhelmed) reviews a complaint notebook.

TOMMY
Jackie, I've been going through the complaint book. There's like forty things in here from last month. Warm beer, slow service, wrong orders, sticky floors, bad music, broken bathroom lock, weak drinks, no parking...

JACKIE
(not looking up)
How many of those do you think actually matter?

TOMMY
All of them? A complaint is a complaint.

JACKIE
(setting down the glass)
No. A complaint is data. And data has a hierarchy. Sit down. I'm about to save you from the biggest rookie mistake in this business."""
        },
        {
            "heading": "PAGE 2 — THE 80/20 RULE",
            "content": """Jackie grabs a bar napkin and draws a simple chart.

JACKIE
In 1896, an Italian economist named Vilfredo Pareto noticed that 80% of the land in Italy was owned by 20% of the people. Turns out, that ratio shows up everywhere. In business, 80% of your problems come from 20% of the causes.

TOMMY
The 80/20 rule.

JACKIE
Also called the Pareto Principle. And in this bar, it means that out of your forty complaints, maybe eight of them are responsible for almost all of our actual revenue loss. The rest? Noise.

TOMMY
How do you know which eight?

JACKIE
You count. You measure. You build a Pareto Chart. And then you focus your energy on the vital few instead of drowning in the trivial many."""
        },
        {
            "heading": "PAGE 3 — COUNTING THE DATA",
            "content": """Jackie pulls out a ledger — handwritten, meticulous.

JACKIE
I've been tracking complaints for six months. Not just "someone complained" — I track the complaint, the frequency, and the estimated revenue impact. Watch.

She reads from the ledger:

JACKIE (CONT'D)
Slow service: 47 complaints, estimated $3,200 in lost tabs (people leave). Weak drinks: 31 complaints, $2,100 in lost repeat customers. Wrong orders: 22 complaints, $1,400 in remakes and comps. Warm beer: 18 complaints, $900 in refunds. Bad music: 15 complaints, $200 impact. Sticky floors: 12 complaints, $100 impact. Broken bathroom lock: 8 complaints, $50 impact. No parking: 6 complaints, $0 direct impact.

TOMMY
You track all that?

JACKIE
If you don't measure it, you can't manage it. Now let's chart it."""
        },
        {
            "heading": "PAGE 4 — BUILDING THE CHART",
            "content": """Jackie draws a bar chart on a larger piece of paper. Bars descending from left to right.

JACKIE
A Pareto Chart has two parts. First: bars showing each cause, sorted from highest impact to lowest. Left to right, biggest to smallest.

She draws the bars:

JACKIE (V.O.)
Slow service: $3,200
Weak drinks: $2,100
Wrong orders: $1,400
Warm beer: $900
Bad music: $200
Sticky floors: $100
Bathroom lock: $50
No parking: $0

JACKIE (CONT'D)
Total revenue impact: $7,950. Now the second part: a cumulative percentage line.

She draws a rising curve over the bars.

JACKIE (CONT'D)
Slow service alone is 40% of the total. Add weak drinks: 67%. Add wrong orders: 84%. Three causes — out of eight — account for 84% of our revenue loss. That's your vital few."""
        },
        {
            "heading": "PAGE 5 — THE VITAL FEW VS. THE TRIVIAL MANY",
            "content": """TOMMY
So the sticky floors and the bathroom lock...

JACKIE
Trivial many. They're real complaints, sure. But fixing the bathroom lock saves us fifty bucks. Fixing slow service saves us thirty-two hundred. Where do you want to spend your time?

TOMMY
Slow service. Obviously.

JACKIE
But what does every new bartender do? They fix the easy stuff. They tighten the bathroom lock, they mop the floors twice, they change the playlist. Because it FEELS productive. Meanwhile, the three causes that are actually bleeding money go untouched.

She taps the chart.

JACKIE (CONT'D)
The Pareto Chart is an antidote to busywork. It forces you to prioritize by IMPACT, not by ease or visibility. The vital few are usually the hardest to fix — that's why they're still problems."""
        },
        {
            "heading": "PAGE 6 — DRILLING INTO THE TOP CAUSE",
            "content": """TOMMY
Okay, so slow service is number one. How do we fix it?

JACKIE
First, we break it down further. Slow service isn't one cause — it's a category. We need a SECOND Pareto analysis within it.

She draws another chart.

JACKIE (CONT'D)
Why is service slow? I tracked the sub-causes: Understaffed on Fridays (18 incidents), bartender bottleneck at the well (12 incidents), kitchen backup on food orders (10 incidents), POS system freezing (7 incidents).

She charts them.

JACKIE (CONT'D)
Understaffing on Fridays is 38% of slow service incidents. Add the well bottleneck: 64%. Two sub-causes drive nearly two-thirds of our biggest problem.

TOMMY
So we hire another Friday bartender and reorganize the well?

JACKIE
Now you're thinking in Pareto. Attack the biggest bar in the chart. Then re-measure. Then attack the next one. Continuous improvement, driven by data."""
        },
        {
            "heading": "PAGE 7 — THE COST OF IGNORING PARETO",
            "content": """JACKIE
Let me show you what happens when you DON'T use Pareto. Last year, the previous owner spent $4,000 on a new sound system because of music complaints.

TOMMY
That's the $200 impact category.

JACKIE
Exactly. He spent $4,000 to fix a $200 problem. Meanwhile, slow service — the $3,200 problem — got nothing. He could have hired a part-time Friday bartender for $2,400 a year and recovered most of that $3,200.

She writes the numbers:

JACKIE (V.O.)
Sound system: $4,000 spent → $200 recovered → ROI: -95%
Friday bartender: $2,400 spent → $3,200 recovered → ROI: +33%

JACKIE (CONT'D)
That's the cost of solving problems by gut instead of by data. You invest in the wrong place and wonder why nothing improves. Pareto would have told him in five minutes where to put the money."""
        },
        {
            "heading": "PAGE 8 — DYNAMIC PARETO",
            "content": """TOMMY
Does the chart change over time?

JACKIE
Great question. Yes. Pareto is not a one-time exercise. You build the chart, fix the top causes, then REBUILD the chart. The bars shift.

She draws a second chart labeled "After Fixes."

JACKIE (CONT'D)
Say we fix slow service and weak drinks. Now the chart looks different. Wrong orders moves to number one. Warm beer moves to number two. New vital few, new priorities.

TOMMY
So you're always chasing the tallest bar.

JACKIE
Exactly. And over time, the total impact shrinks. First month: $7,950 in losses. After fixing the top two: maybe $3,000. After the next round: $1,200. You're compressing the problem space with each iteration.

She draws a declining total line.

JACKIE (CONT'D)
That's continuous improvement. Not random fixes. Targeted, measured, prioritized improvement. Pareto is the engine that drives it."""
        },
        {
            "heading": "PAGE 9 — THE CUSTOMER PERCEPTION TRAP",
            "content": """TOMMY
What about complaints that don't have a dollar value? Like, people just FEEL like the vibe is off?

JACKIE
Good. That's the perception trap. Some complaints are loud but cheap. Some are quiet but expensive. Pareto helps you separate signal from noise.

She points to the chart.

JACKIE (CONT'D)
"Bad music" gets mentioned a lot because it's easy to complain about. It's visible. But it drives almost zero revenue loss — people don't leave over music. "Weak drinks," on the other hand, gets fewer complaints because people just quietly stop coming back. It's invisible but deadly.

TOMMY
So the loudest complaints aren't the most important?

JACKIE
Almost never. The most important complaints are the ones that change BEHAVIOR — people leaving, not returning, spending less. Those are the ones that show up in the revenue column. Pareto forces you to look at impact, not volume.

She underlines "revenue impact" on the chart.

JACKIE (CONT'D)
Volume tells you what people talk about. Impact tells you what actually matters."""
        },
        {
            "heading": "PAGE 10 — THE LESSON",
            "content": """Tommy looks at the charts spread across the bar. Jackie pours two coffees.

JACKIE
Here's the bottom line, kid. You've got limited time, limited money, and limited energy. You cannot fix everything. The Pareto Chart tells you what to fix FIRST, what to fix NEXT, and what to ignore entirely.

TOMMY
And the 80/20 really holds up?

JACKIE
It's not always exactly 80/20. Sometimes it's 70/30 or 90/10. The principle is what matters: a small number of causes drive a disproportionate share of the effect. Find them, fix them, re-measure, repeat.

She picks up the complaint notebook and hands it back to Tommy.

JACKIE (CONT'D)
ISO 31010, Section B.8.4. Pareto Analysis. Quality engineers use it in factories. Supply chain managers use it in warehouses. We use it to run a bar that doesn't bleed money.

TOMMY
(flipping through the notebook)
I'm gonna start tracking revenue impact on every complaint.

JACKIE
(smiling)
Now you're a bartender. Before, you were just pouring drinks.

The evening crowd starts filtering in. Tommy takes his position behind the bar with new eyes — scanning not for complaints, but for the vital few.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Cross Impact Analysis"] = {
    "title": "Cross Impact Analysis: The Bookie's Web",
    "iso_section": "B.6.2",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — INT. SPORTS BAR BACK BOOTH — EVENING",
            "content": """FADE IN:

A dimly lit sports bar. Multiple screens showing pre-game coverage. SAL (60s, reading glasses, three phones, old-school bookie who survived the digital age) sits in a corner booth. DANNY (20s, sharp but green, thinks he's figured out sports betting) slides in across from him.

DANNY
Sal, I've got a lock. Titans are playing the Wolves tonight. Titans' star point guard just sprained his ankle in warmups. The line hasn't moved yet. I'm hammering the Wolves moneyline.

SAL
(not looking up from his phones)
You think you're the only one who saw that tweet?

DANNY
The line hasn't moved yet!

SAL
The line will move. But that's not your problem. Your problem is you're thinking in straight lines. One event, one outcome. The real money is in the web."""
        },
        {
            "heading": "PAGE 2 — BEYOND SIMPLE ODDS",
            "content": """SAL
When Marcus Reed sprains his ankle, you see one thing: Titans are weaker, Wolves win. Simple probability shift. Maybe Titans' win probability drops from 60% to 40%.

DANNY
Right. So I bet the Wolves.

SAL
And so does everyone else. The line adjusts. Your edge disappears in minutes. But here's what the amateurs miss: Reed's ankle doesn't just change the game outcome. It changes EVERYTHING connected to that game. And those connections? That's where the real value hides.

He pulls out a small notebook filled with grids.

SAL (CONT'D)
This is Cross Impact Analysis. Instead of looking at one event in isolation, you map how every event affects the probability of every OTHER event. It's a matrix of conditional probabilities."""
        },
        {
            "heading": "PAGE 3 — THE CROSS IMPACT MATRIX",
            "content": """Sal draws a grid on a napkin. Rows and columns labeled with events.

SAL
Here are the events connected to tonight's game. Event A: Reed is out. Event B: Titans win. Event C: Total points over 210.5. Event D: Titans' backup guard scores over 15 points. Event E: Wolves' center gets over 12 rebounds.

He fills in the matrix:

SAL (CONT'D)
The matrix shows: if Event A happens (Reed out), what's the new probability of each other event?

SAL (V.O.)
A→B: Titans win drops from 60% to 40%
A→C: Over 210.5 drops from 55% to 42% (less scoring without Reed)
A→D: Backup over 15 pts rises from 20% to 65% (more minutes, more shots)
A→E: Wolves center over 12 rebounds rises from 35% to 55% (weaker interior defense)

SAL (CONT'D)
One event. Four probability shifts. And the market is only pricing in the first one."""
        },
        {
            "heading": "PAGE 4 — CONDITIONAL PROBABILITIES",
            "content": """DANNY
Wait. So the over/under changes too?

SAL
Of course it does. Reed averages 24 points a game. His backup averages 11. That's a 13-point expected scoring drop from one position. Even if the backup plays more minutes, the efficiency drops. The total is likely to go UNDER.

DANNY
But the total line hasn't moved either.

SAL
Because the market is slow on cross impacts. The moneyline adjusts fast — that's the obvious bet. The total adjusts slower. And the prop bets? The player props? Those are the last to move. That's your window.

He circles Event D on the matrix.

SAL (CONT'D)
The backup guard's point total. The market still has his over/under at 12.5 based on his season average. But with Reed out, he's getting 35 minutes instead of 15. His conditional probability of hitting 15+ just tripled. THAT'S the bet."""
        },
        {
            "heading": "PAGE 5 — SECOND-ORDER EFFECTS",
            "content": """SAL
But we're not done. Cross Impact Analysis doesn't stop at first-order effects. Event A affects Event D. But Event D affects OTHER events too.

DANNY
Like what?

SAL
If the backup guard is taking more shots (Event D), he's taking shots AWAY from someone else. The Titans' power forward, who normally gets 18 shots, might only get 12. His point total prop is now overvalued.

He adds to the matrix:

SAL (CONT'D)
D→F: If backup takes more shots, power forward's points drop. His over/under at 22.5 is now probably a strong under.

And it cascades further. If the power forward is getting fewer touches, he's less engaged defensively. Which means the Wolves' small forward has easier driving lanes. His assist numbers go up.

DANNY
(eyes widening)
It's like dominoes.

SAL
It's like a WEB. Every node connects to every other node. Pull one thread and the whole structure shifts. The amateurs see the thread. The professionals see the web."""
        },
        {
            "heading": "PAGE 6 — BUILDING THE FULL MATRIX",
            "content": """Sal flips to a fresh page and draws a larger matrix — 6 events by 6 events.

SAL
A proper Cross Impact Matrix is N-by-N. Every event gets a row and a column. The cell at row i, column j tells you: "If event i occurs, what is the new probability of event j?"

He fills in numbers:

SAL (V.O.)
         B(Win)  C(Over)  D(Backup)  E(Reb)  F(PF pts)
A(Reed)   0.40    0.42     0.65       0.55     0.35
B(Win)     —      0.60     0.45       0.30     0.55
C(Over)   0.55     —       0.50       0.45     0.50
D(Backup) 0.38    0.48      —         0.50     0.30
E(Reb)    0.42    0.52     0.50        —       0.48

SAL (CONT'D)
The diagonal is empty — an event doesn't impact itself. But every other cell is a conditional probability. This matrix IS the game. Everything else is just commentary."""
        },
        {
            "heading": "PAGE 7 — FINDING THE VALUE",
            "content": """SAL
Now here's how you make money. You compare the cross-impact adjusted probabilities to the market's implied probabilities.

He writes two columns:

SAL (V.O.)
Market implied probability vs. Cross-impact adjusted:
Wolves moneyline: Market 55% → Adjusted 60% → Small edge
Under 210.5: Market 48% → Adjusted 58% → Moderate edge
Backup over 12.5 pts: Market 45% → Adjusted 65% → LARGE edge
Wolves C over 12 reb: Market 38% → Adjusted 55% → Large edge
PF under 22.5 pts: Market 50% → Adjusted 65% → Moderate edge

SAL (CONT'D)
The moneyline? Tiny edge. Everyone's already on it. The under? Decent. But the backup's points and the center's rebounds? Those are 15-20 point probability gaps. The market hasn't priced in the cross impacts yet.

DANNY
So I bet those instead of the moneyline?

SAL
You bet where the EDGE is largest. The moneyline is the obvious play with the smallest edge. The prop bets are the hidden plays with the biggest edges. Cross Impact Analysis shows you exactly where the market is wrong."""
        },
        {
            "heading": "PAGE 8 — CORRELATION VS. INDEPENDENCE",
            "content": """DANNY
Can I parlay all of them? Backup points AND center rebounds AND the under?

SAL
Careful. That's where correlation kills you. These events aren't independent — they're connected through the same causal web. A parlay assumes independence. If the events are positively correlated, the parlay overestimates your edge.

DANNY
What do you mean?

SAL
If the backup scores a lot, it probably means the game is close, which means more possessions, which means the total might go OVER, not under. Your "under" bet and your "backup over" bet are partially contradictory.

He draws arrows between the events.

SAL (CONT'D)
Cross Impact Analysis shows you the correlations explicitly. Cell D→C tells you: if the backup scores big, the over probability shifts to 48%. That's HIGHER than the baseline. So combining "backup over" with "game under" in a parlay is fighting against the correlation structure.

DANNY
So I pick the bets that are POSITIVELY correlated for parlays?

SAL
Or you bet them individually and size each one by the edge. Don't let the parlay payout seduce you into ignoring the math."""
        },
        {
            "heading": "PAGE 9 — REAL-TIME UPDATES",
            "content": """The game tips off on the screen above them. Sal watches intently.

SAL
Now watch. The matrix isn't static. As the game unfolds, new information updates the conditional probabilities in real time.

First quarter ends. The backup guard has 8 points.

SAL (CONT'D)
He's on pace for 32. The market is adjusting his live line, but it's still lagging. More importantly, his hot shooting is pulling the defense toward him, which means...

DANNY
The center is getting easier rebounds?

SAL
(pointing at him)
The cross impact is playing out in real time. Center already has 5 rebounds in the first quarter. His live over/under just moved from 12.5 to 14.5, but our model had him at 55% for over 12 — he's tracking even higher.

He checks his phone.

SAL (CONT'D)
And the total? Currently on pace for 198. Under is looking strong. The market had it at 48% under. We had it at 58%. The first quarter data is confirming our cross-impact model.

DANNY
This is insane.

SAL
This is math. The insane part is that most people bet without it."""
        },
        {
            "heading": "PAGE 10 — THE LESSON",
            "content": """Final buzzer. Wolves win. Total: 201 (under). Backup guard: 22 points. Center: 14 rebounds. Power forward: 16 points (under his line).

Sal checks his notebook. Every cross-impact prediction landed.

DANNY
(stunned)
You called all of it.

SAL
I didn't call anything. The matrix called it. I just read the matrix.

He closes the notebook.

SAL (CONT'D)
ISO 31010, Section B.6.2. Cross Impact Analysis. Intelligence agencies use it to predict geopolitical events. Epidemiologists use it to model disease spread. I use it to find value in a basketball game.

DANNY
Can you teach me to build the matrix?

SAL
(standing up)
I just did. One event changes everything it touches. Everything it touches changes everything THEY touch. Map the web, quantify the connections, and you'll see what the market can't.

He drops a twenty on the table for the drinks.

SAL (CONT'D)
The straight-line thinkers bet the moneyline and break even. The web thinkers bet the cross impacts and build an edge. Choose your geometry.

Sal walks out. Danny stares at the napkin matrix, then pulls out his own notebook and starts building his first grid.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Cost/Benefit Analysis (CBA)"] = {
    "title": "Cost/Benefit Analysis: The Loan Shark's Lesson",
    "iso_section": "B.9.2",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — INT. PAWN SHOP BACK OFFICE — NIGHT",
            "content": """FADE IN:

A cluttered pawn shop office. Gold chains in glass cases. A desk calculator from the 1980s. LEON (50s, calm, well-dressed for a pawn shop, speaks softly because he doesn't need to yell) sits behind the desk. CARLOS (30s, desperate, fidgeting, needs money yesterday) sits across from him.

CARLOS
I need a thousand. I can pay you back fifty a week. That's fair, right?

LEON
(leaning back)
Fifty a week. Let me ask you something, Carlos. Do you know what that fifty dollars actually costs you?

CARLOS
It costs fifty dollars. That's the point.

LEON
(smiling)
No. That's the illusion. The fifty dollars you pay me next week is not the same as the fifty dollars you pay me in six months. And until you understand why, you're going to keep sitting in that chair."""
        },
        {
            "heading": "PAGE 2 — THE TIME VALUE OF MONEY",
            "content": """Leon opens a desk drawer and pulls out a crisp hundred-dollar bill. He holds it up.

LEON
This hundred dollars today — what's it worth?

CARLOS
A hundred dollars.

LEON
Wrong. It's worth MORE than a hundred dollars. Because if you have it today, you can use it today. Invest it, spend it, earn with it. A hundred dollars in your hand right now is worth more than a hundred dollars promised to you a year from now.

CARLOS
Why?

LEON
Three reasons. Inflation: prices go up, so future dollars buy less. Opportunity cost: money today can be put to work earning more money. And risk: the future is uncertain — that promised hundred might never arrive.

He sets the bill down.

LEON (CONT'D)
This is called the Time Value of Money. It's the foundation of every financial calculation that matters. And it's the reason your "fifty a week" is not what you think it is."""
        },
        {
            "heading": "PAGE 3 — THE DISCOUNT RATE",
            "content": """LEON
To compare money at different points in time, you need a Discount Rate. Think of it as the cost of waiting. The higher the rate, the less future money is worth today.

He pulls out the calculator.

LEON (CONT'D)
A bank might use 5% per year. A venture capitalist might use 20%. For someone in your situation — high risk, no collateral, urgent need — the effective discount rate is much higher. Let's say 15% per year, or about 0.29% per week.

CARLOS
That doesn't sound like much.

LEON
It doesn't SOUND like much. But it compounds. Every week, the value of your future payment shrinks a little more. The fifty dollars you pay me in week one is worth about $49.85 in today's money. The fifty you pay in week twenty is worth about $47.20. The fifty you pay in week forty? About $44.70.

CARLOS
So the same fifty dollars is worth less and less?

LEON
To ME, yes. But to YOU, it costs the same effort every single week. That's the asymmetry I profit from."""
        },
        {
            "heading": "PAGE 4 — NET PRESENT VALUE",
            "content": """LEON
Now let's calculate the Net Present Value of your deal. NPV is the sum of all future cash flows, each one discounted back to today's value.

He starts punching numbers.

LEON (CONT'D)
You want a thousand dollars today. You'll pay me fifty a week for... how long?

CARLOS
Until it's paid off. Twenty weeks?

LEON
(laughing softly)
Twenty weeks at fifty is a thousand. That's just the principal. My fee is fifty a week in INTEREST. The principal stays. You pay fifty a week until you can pay back the full thousand PLUS the weekly fifty.

CARLOS
(paling)
So I'm paying fifty a week... forever?

LEON
Not forever. But let's say it takes you six months — 26 weeks — to save up the thousand to pay me back. In that time, you've paid me 26 times fifty: $1,300 in interest. Plus the $1,000 principal. Total: $2,300 for a $1,000 loan."""
        },
        {
            "heading": "PAGE 5 — THE NPV CALCULATION",
            "content": """LEON
Let me show you the NPV from YOUR perspective. You receive $1,000 today. That's positive. Then you pay $50 per week for 26 weeks, plus $1,000 at week 26. All negative.

He writes:

LEON (V.O.)
NPV = +$1,000 - Σ($50 / (1 + 0.0029)^n) for n=1 to 26 - $1,000/(1.0029)^26

LEON (CONT'D)
The discounted value of the 26 weekly payments is about $1,270. The discounted value of the final $1,000 payback is about $927. Total present value of what you pay: $2,197.

He circles the result.

LEON (CONT'D)
NPV for you: $1,000 minus $2,197 equals NEGATIVE $1,197. You're destroying $1,197 in present value. For every dollar I lend you, you lose a dollar twenty in real terms.

CARLOS
(staring at the numbers)
That can't be right.

LEON
It's exactly right. The fifty a week FEELS small. But when you discount all those payments back to today and add them up, the true cost is more than double the loan."""
        },
        {
            "heading": "PAGE 6 — THE EFFECTIVE ANNUAL RATE",
            "content": """LEON
Want to know your effective annual interest rate? Fifty dollars a week on a thousand-dollar principal. That's 5% per WEEK.

CARLOS
Five percent doesn't sound bad.

LEON
Per WEEK. Compounded. The effective annual rate is: (1.05)^52 minus 1.

He calculates.

LEON (CONT'D)
That's 11.6. As in 1,160%. Your annual interest rate is over a thousand percent.

CARLOS
(standing up)
That's insane.

LEON
(calmly)
Sit down. I'm not trying to sell you the loan. I'm trying to show you the math so you can make an informed decision. Most people in your position don't see these numbers. They see "fifty a week" and think it's manageable. The math says otherwise.

Carlos sits back down, slowly."""
        },
        {
            "heading": "PAGE 7 — THE COST/BENEFIT FRAMEWORK",
            "content": """LEON
Let's do a proper Cost/Benefit Analysis. What do you need the thousand for?

CARLOS
My car's transmission. Without it, I can't get to work. I lose my job.

LEON
Now we have a benefit to quantify. What do you earn?

CARLOS
Six-fifty a week, take-home.

LEON
So the benefit of the loan is: you keep your job. The value of that over 26 weeks is 26 times $650 equals $16,900 in income preserved.

He writes two columns:

LEON (V.O.)
BENEFITS:
- Income preserved: $16,900
- Continued employment: ongoing value

COSTS:
- Interest payments: $1,300
- Principal repayment: $1,000
- NPV of total payments: $2,197
- Opportunity cost of $50/week: reduced savings capacity

LEON (CONT'D)
Net benefit: $16,900 minus $2,300 equals $14,600. The loan is a terrible financial product but a rational economic decision — IF and ONLY IF losing the car means losing the job."""
        },
        {
            "heading": "PAGE 8 — ALTERNATIVE ANALYSIS",
            "content": """LEON
But a good CBA doesn't stop at one option. You compare alternatives.

He adds columns:

LEON (CONT'D)
Alternative one: Borrow from me. Cost: $2,300. Benefit: keep job. Net: +$14,600.

Alternative two: Ask your employer for a $1,000 advance. Cost: maybe $0 in interest, but social cost — you look desperate. Probability they say yes: maybe 40%.

Alternative three: Use public transit for a month while you save. Cost: $120 in bus passes plus 90 extra minutes commuting daily. Risk: 15% chance of being late enough to get fired.

Alternative four: Find a credit union emergency loan. Cost: maybe $1,100 total at 18% APR. But processing takes two weeks — can you survive two weeks without the car?

CARLOS
I didn't think about the credit union.

LEON
Most people don't. They see the immediate problem and grab the immediate solution. CBA forces you to line up ALL the options and compare them on the same basis — Net Present Value."""
        },
        {
            "heading": "PAGE 9 — THE DECISION MATRIX",
            "content": """Leon draws a comparison table.

LEON (V.O.)
Option          | NPV Cost | Probability | Risk-Adjusted NPV
Loan from me    | -$2,197  | 100%        | -$2,197
Employer advance| -$0      | 40%         | -$0 (but 60% chance of plan B)
Public transit  | -$350    | 85% success | -$298 (15% job loss risk = -$2,535)
Credit union    | -$1,050  | 90%         | -$945 (10% timing risk)

LEON (CONT'D)
Risk-adjusted, the credit union loan costs you $945 in present value. My loan costs you $2,197. The credit union is less than half the cost.

CARLOS
But it takes two weeks.

LEON
So the real question is: can you survive two weeks? If yes, the credit union saves you $1,252 in present value. If no, my loan is the rational choice despite being expensive. The CBA doesn't tell you what to WANT. It tells you what each option actually COSTS.

CARLOS
(thinking hard)
My brother could drive me for two weeks.

LEON
Then you just found a bridge strategy that makes the credit union option viable. Your effective cost just dropped from $2,197 to about $945 plus whatever you owe your brother in gas money."""
        },
        {
            "heading": "PAGE 10 — THE LESSON",
            "content": """Carlos stands up. He hasn't taken the loan.

CARLOS
I'm gonna try the credit union first.

LEON
(nodding)
Smart. And if they say no, I'm still here. Same terms. I don't change the price based on desperation — that's a different kind of business.

He walks Carlos to the door.

LEON (CONT'D)
ISO 31010, Section B.9.2. Cost/Benefit Analysis and Net Present Value. Governments use it to decide whether to build highways. Hospitals use it to evaluate new equipment. You just used it to avoid a thousand-percent interest rate.

CARLOS
Why'd you show me all that? You could've just given me the loan.

LEON
(leaning against the doorframe)
Because an informed borrower is a borrower who pays me back. And a borrower who understands NPV? He only comes to me when he truly has no other option. That's the customer I want — the one who's done the math and decided I'm still the best choice. Not the one who's just desperate.

Carlos nods and walks out into the night. Leon watches him go, then returns to his desk and his calculator.

FADE OUT.

— END —"""
        }
    ]
}


SCREENPLAYS["Markov Analysis"] = {
    "title": "Markov Analysis: The Busker's Calculus",
    "iso_section": "B.5.9",
    "subtitle": "A Street Math Screenplay",
    "pages": [
        {
            "heading": "PAGE 1 — INT. SUBWAY CAR — MORNING",
            "content": """FADE IN:

A New York City subway car, mid-morning. Half-empty. JEROME (40s, saxophone case, weathered hands, PhD dropout who chose music over academia) sits in a corner seat, counting crumpled bills. AISHA (20s, violin case, new to busking, conservatory student paying rent) sits across from him.

AISHA
How do you know which car to play in? I've been picking randomly and some days I make sixty bucks, some days I make six.

JEROME
(folding the bills)
You're not picking randomly. You're picking BLINDLY. There's a difference. Random means you understand the probabilities and accept the variance. Blind means you don't know the probabilities at all.

AISHA
So what are the probabilities?

JEROME
That depends on the state of the car. And the state of the car is all that matters."""
        },
        {
            "heading": "PAGE 2 — DEFINING THE STATES",
            "content": """Jerome pulls a small notebook from his saxophone case. It's filled with tally marks and numbers.

JEROME
I've been tracking subway cars for three years. Every car I enter, I classify it into one of three states.

He writes:

JEROME (V.O.)
State G (Good): Car is 40-70% full, mixed demographics, relaxed vibe, no headphones majority. Expected earnings: $15-25 per performance.

State F (Fair): Car is either too empty (<30%) or too full (>80%), or the crowd is disengaged — headphones, sleeping, hostile. Expected earnings: $3-8 per performance.

State X (Failed): Transit police present, or a competing performer, or an aggressive passenger situation. Expected earnings: $0, plus risk of citation or confrontation.

AISHA
So you just pick the Good cars?

JEROME
If only it were that simple. The problem is: cars change state. A Good car can become Fair. A Fair car can become Failed. And the transitions happen according to probabilities that I can measure."""
        },
        {
            "heading": "PAGE 3 — THE TRANSITION MATRIX",
            "content": """JEROME
This is a Markov Chain. A system that moves between discrete states, where the probability of the next state depends ONLY on the current state — not on the history. It's called the Memoryless Property.

AISHA
The car doesn't remember what it was before?

JEROME
Exactly. If I'm in a Good car right now, the probability of it being Good, Fair, or Failed at the next stop is fixed — regardless of whether it was Good for the last five stops or just became Good.

He draws a 3x3 grid:

JEROME (V.O.)
Transition Matrix (per stop):
         To G    To F    To X
From G:  0.60    0.30    0.10
From F:  0.20    0.50    0.30
From X:  0.05    0.35    0.60

JEROME (CONT'D)
Read it like this: if I'm in a Good car, there's a 60% chance it stays Good at the next stop, 30% chance it drops to Fair, and 10% chance it goes to Failed. People get off, cops get on, the vibe shifts."""
        },
        {
            "heading": "PAGE 4 — ONE-STEP PREDICTIONS",
            "content": """AISHA
So if I'm in a Good car right now, what happens at the next stop?

JEROME
60% chance it stays Good. You keep playing, keep earning. 30% chance it drops to Fair — crowd thins out or someone puts on a podcast at full volume. 10% chance it goes Failed — transit cop boards or someone starts hassling you.

AISHA
And if I'm in a Fair car?

JEROME
Only 20% chance it improves to Good. 50% it stays Fair. 30% it degrades to Failed. See the asymmetry? It's EASIER to go from Good to Fair than from Fair to Good. The system has a natural drift toward degradation.

He taps the matrix.

JEROME (CONT'D)
That drift is critical. It means you can't just sit in a car and hope it gets better. The math says a Fair car is more likely to get worse than better. You need to actively manage your state — which means knowing when to MOVE."""
        },
        {
            "heading": "PAGE 5 — MULTI-STEP PROBABILITIES",
            "content": """JEROME
Now here's where it gets powerful. I can predict not just one stop ahead, but multiple stops. To get the two-step transition matrix, I multiply the matrix by itself.

He scribbles the calculation.

JEROME (CONT'D)
After two stops, starting from Good: probability of still being Good is about 42%. Fair: 33%. Failed: 25%.

After three stops from Good: Good drops to about 33%. Fair: 33%. Failed: 34%.

AISHA
So after three stops, there's a one-in-three chance I'm dealing with cops?

JEROME
Starting from a Good car, yes. After three stops, the states are almost equally likely. The system is converging toward its steady state — the long-run distribution where the probabilities stop changing.

AISHA
What's the steady state?

JEROME
That's the big question. Let me show you."""
        },
        {
            "heading": "PAGE 6 — THE STEADY STATE",
            "content": """JEROME
The steady state — also called the stationary distribution — is where the system settles if you let it run long enough. No matter where you start, you end up at the same long-run probabilities.

He writes a system of equations:

JEROME (V.O.)
πG = 0.60·πG + 0.20·πF + 0.05·πX
πF = 0.30·πG + 0.50·πF + 0.35·πX
πX = 0.10·πG + 0.30·πF + 0.60·πX
πG + πF + πX = 1

JEROME (CONT'D)
Solving this system... the steady state is approximately: πG = 0.22, πF = 0.36, πX = 0.42.

AISHA
(dismayed)
42% of the time, I'm in a Failed state?

JEROME
In the LONG RUN, if you just ride the train without strategy, you'll spend 22% of your time in Good cars, 36% in Fair cars, and 42% in Failed cars. The system's natural equilibrium is weighted toward failure.

AISHA
That's depressing.

JEROME
That's the baseline. But Markov Analysis doesn't just describe the system — it tells you how to BEAT it."""
        },
        {
            "heading": "PAGE 7 — THE OPTIMAL STRATEGY",
            "content": """JEROME
The steady state assumes you're passive — you stay in whatever car you're in and let the transitions happen. But what if you're ACTIVE? What if you change cars strategically?

AISHA
Like, get off and move to a different car?

JEROME
Exactly. My strategy: if I'm in a Good car, I stay and play. If I drop to Fair, I play one more stop — there's a 20% chance it recovers. If it's still Fair after one stop, I move. If I ever hit Failed, I move IMMEDIATELY.

He recalculates.

JEROME (CONT'D)
With this strategy, I'm essentially resetting my state every time I move. When I enter a new car, I'm sampling from the train's overall distribution. About 35% of cars are Good at any given time, 40% Fair, 25% Failed.

AISHA
So by moving, you get better odds than the steady state?

JEROME
Much better. My active strategy keeps me in Good cars about 45% of the time instead of 22%. That more than doubles my expected earnings."""
        },
        {
            "heading": "PAGE 8 — EXPECTED EARNINGS",
            "content": """JEROME
Let me put dollars on it. Passive strategy — ride the steady state:

He calculates:

JEROME (V.O.)
E(passive) = 0.22 × $20 + 0.36 × $5 + 0.42 × $0
E(passive) = $4.40 + $1.80 + $0 = $6.20 per stop

JEROME (CONT'D)
Active strategy — move when Fair persists or Failed:

JEROME (V.O.)
E(active) = 0.45 × $20 + 0.35 × $5 + 0.20 × $0
E(active) = $9.00 + $1.75 + $0 = $10.75 per stop

JEROME (CONT'D)
That's $10.75 versus $6.20. Over a 20-stop session, that's $215 versus $124. The active strategy earns 73% more.

AISHA
Just from knowing when to move?

JEROME
Just from understanding the transition probabilities and acting on them instead of hoping. The math doesn't change the system. It changes YOUR behavior within the system. And that changes everything."""
        },
        {
            "heading": "PAGE 9 — ABSORPTION AND TIME TO FAILURE",
            "content": """AISHA
How long until I definitely get caught by transit police? Like, what's the expected number of stops before I hit Failed for the first time?

JEROME
That's called the Expected Time to Absorption — if we treat Failed as an absorbing state (once you're caught, you're done for the day).

He modifies the matrix, removing transitions OUT of Failed.

JEROME (CONT'D)
Using the fundamental matrix of the absorbing chain... starting from Good, the expected number of stops before first hitting Failed is about 6.5. Starting from Fair, it's about 3.8.

AISHA
So if I start in a Good car, I've got about six or seven stops before trouble finds me?

JEROME
On average. Could be two, could be fifteen. But the expected value is 6.5. That's your planning horizon. If you're in a Good car, you've got roughly six stops of productive playing before the probability of a Failed state becomes dominant.

AISHA
So I should plan my set list for six stops.

JEROME
(grinning)
Now you're thinking like a Markov analyst. Optimize for the expected window, not the best case."""
        },
        {
            "heading": "PAGE 10 — THE LESSON",
            "content": """The train pulls into a station. Jerome looks at the car — it's thinning out. Fair state.

JEROME
(standing)
This car just went Fair. I'm moving. You coming?

Aisha grabs her violin case and follows him to the next car. It's 60% full, mixed crowd, good energy. Good state.

JEROME (CONT'D)
(setting up his sax)
ISO 31010, Section B.5.9. Markov Analysis. Engineers use it to predict when machines will break down. Epidemiologists use it to model disease progression. We use it to figure out which subway car to play saxophone in.

AISHA
(tuning her violin)
Same math.

JEROME
Same math. Different stage. The system has states, the states have transitions, and the transitions have probabilities. Once you see that structure, you stop being a passenger in the system and start being a player.

He lifts the saxophone to his lips. Aisha raises her bow. They lock eyes, nod, and begin playing a duet. The car fills with music. Passengers look up from their phones. Bills start appearing in the open cases.

Good state. Six stops to make it count.

FADE OUT.

— END —"""
        }
    ]
}


# ─── Image Generation ─────────────────────────────────────────────────────────

# Color palettes for each screenplay
COLOR_PALETTES = {
    "Bow Tie Analysis": {"bg": (15, 10, 35), "accent": (220, 50, 80), "text": (255, 255, 255), "shape": (180, 40, 70)},
    "Decision Tree Analysis": {"bg": (10, 30, 15), "accent": (50, 200, 80), "text": (255, 255, 255), "shape": (40, 160, 65)},
    "Monte Carlo Simulation": {"bg": (35, 15, 10), "accent": (230, 140, 30), "text": (255, 255, 255), "shape": (190, 110, 25)},
    "Game Theory": {"bg": (10, 15, 40), "accent": (60, 120, 230), "text": (255, 255, 255), "shape": (50, 100, 190)},
    "Layers of Protection Analysis (LOPA)": {"bg": (30, 10, 30), "accent": (180, 60, 200), "text": (255, 255, 255), "shape": (150, 50, 170)},
    "Ishikawa (Fishbone) Analysis": {"bg": (35, 25, 10), "accent": (220, 170, 40), "text": (255, 255, 255), "shape": (180, 140, 30)},
    "Pareto Charts": {"bg": (10, 30, 30), "accent": (40, 200, 200), "text": (255, 255, 255), "shape": (30, 160, 160)},
    "Cross Impact Analysis": {"bg": (25, 10, 10), "accent": (220, 60, 60), "text": (255, 255, 255), "shape": (180, 50, 50)},
    "Cost/Benefit Analysis (CBA)": {"bg": (10, 25, 10), "accent": (80, 200, 80), "text": (255, 255, 255), "shape": (60, 160, 60)},
    "Markov Analysis": {"bg": (20, 15, 35), "accent": (140, 100, 230), "text": (255, 255, 255), "shape": (110, 80, 190)},
}

# Visual motifs for each technique
TECHNIQUE_ICONS = {
    "Bow Tie Analysis": "bowtie",
    "Decision Tree Analysis": "tree",
    "Monte Carlo Simulation": "dice",
    "Game Theory": "grid",
    "Layers of Protection Analysis (LOPA)": "layers",
    "Ishikawa (Fishbone) Analysis": "fishbone",
    "Pareto Charts": "bars",
    "Cross Impact Analysis": "web",
    "Cost/Benefit Analysis (CBA)": "scale",
    "Markov Analysis": "chain",
}


def draw_bowtie(draw, cx, cy, palette):
    """Draw a bow tie shape."""
    s = palette["shape"]
    a = palette["accent"]
    # Left triangle
    draw.polygon([(cx-120, cy-50), (cx, cy), (cx-120, cy+50)], fill=s, outline=a, width=2)
    # Right triangle
    draw.polygon([(cx+120, cy-50), (cx, cy), (cx+120, cy+50)], fill=s, outline=a, width=2)
    # Center knot
    draw.ellipse([(cx-15, cy-15), (cx+15, cy+15)], fill=a)


def draw_tree(draw, cx, cy, palette):
    """Draw a decision tree."""
    s = palette["shape"]
    a = palette["accent"]
    # Root
    draw.rectangle([(cx-10, cy-60), (cx+10, cy-40)], fill=a)
    # Branches
    draw.line([(cx, cy-40), (cx-60, cy)], fill=s, width=3)
    draw.line([(cx, cy-40), (cx+60, cy)], fill=s, width=3)
    # Sub-branches
    draw.line([(cx-60, cy), (cx-90, cy+40)], fill=s, width=2)
    draw.line([(cx-60, cy), (cx-30, cy+40)], fill=s, width=2)
    draw.line([(cx+60, cy), (cx+30, cy+40)], fill=s, width=2)
    draw.line([(cx+60, cy), (cx+90, cy+40)], fill=s, width=2)
    # Nodes
    for pos in [(cx-60, cy), (cx+60, cy)]:
        draw.ellipse([(pos[0]-8, pos[1]-8), (pos[0]+8, pos[1]+8)], fill=a)
    for pos in [(cx-90, cy+40), (cx-30, cy+40), (cx+30, cy+40), (cx+90, cy+40)]:
        draw.ellipse([(pos[0]-6, pos[1]-6), (pos[0]+6, pos[1]+6)], fill=a)


def draw_dice(draw, cx, cy, palette):
    """Draw dice for Monte Carlo."""
    s = palette["shape"]
    a = palette["accent"]
    # Die 1
    draw.rectangle([(cx-70, cy-40), (cx-10, cy+20)], outline=a, width=3)
    for dot in [(cx-55, cy-25), (cx-40, cy-10), (cx-25, cy+5)]:
        draw.ellipse([(dot[0]-4, dot[1]-4), (dot[0]+4, dot[1]+4)], fill=a)
    # Die 2
    draw.rectangle([(cx+10, cy-40), (cx+70, cy+20)], outline=a, width=3)
    for dot in [(cx+25, cy-25), (cx+55, cy-25), (cx+25, cy+5), (cx+55, cy+5)]:
        draw.ellipse([(dot[0]-4, dot[1]-4), (dot[0]+4, dot[1]+4)], fill=a)


def draw_grid(draw, cx, cy, palette):
    """Draw a 2x2 game theory grid."""
    s = palette["shape"]
    a = palette["accent"]
    size = 80
    x0, y0 = cx - size//2, cy - size//2
    draw.rectangle([(x0, y0), (x0+size, y0+size)], outline=a, width=3)
    draw.line([(x0+size//2, y0), (x0+size//2, y0+size)], fill=a, width=2)
    draw.line([(x0, y0+size//2), (x0+size, y0+size//2)], fill=a, width=2)
    # Fill quadrants
    draw.rectangle([(x0+2, y0+2), (x0+size//2-1, y0+size//2-1)], fill=(*s, 100))
    draw.rectangle([(x0+size//2+1, y0+size//2+1), (x0+size-2, y0+size-2)], fill=(*s, 100))


def draw_layers(draw, cx, cy, palette):
    """Draw concentric protection layers."""
    a = palette["accent"]
    for i, r in enumerate([60, 45, 30, 15]):
        alpha = 255 - i * 50
        c = tuple(max(0, min(255, v - i*20)) for v in a)
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], outline=c, width=3)
    draw.ellipse([(cx-5, cy-5), (cx+5, cy+5)], fill=a)


def draw_fishbone(draw, cx, cy, palette):
    """Draw a fishbone/Ishikawa diagram."""
    s = palette["shape"]
    a = palette["accent"]
    # Spine
    draw.line([(cx-100, cy), (cx+100, cy)], fill=a, width=4)
    # Head
    draw.polygon([(cx+100, cy-15), (cx+130, cy), (cx+100, cy+15)], fill=a)
    # Ribs
    for offset in [-70, -35, 0, 35, 70]:
        draw.line([(cx+offset, cy), (cx+offset-25, cy-35)], fill=s, width=2)
        draw.line([(cx+offset, cy), (cx+offset-25, cy+35)], fill=s, width=2)


def draw_bars(draw, cx, cy, palette):
    """Draw Pareto-style descending bars."""
    a = palette["accent"]
    s = palette["shape"]
    heights = [70, 55, 40, 25, 15, 8]
    bar_w = 16
    start_x = cx - (len(heights) * (bar_w + 4)) // 2
    for i, h in enumerate(heights):
        x = start_x + i * (bar_w + 4)
        c = tuple(max(0, min(255, v - i*15)) for v in a)
        draw.rectangle([(x, cy + 40 - h), (x + bar_w, cy + 40)], fill=c)
    # Cumulative line
    pts = []
    for i, h in enumerate(heights):
        x = start_x + i * (bar_w + 4) + bar_w // 2
        cum = sum(heights[:i+1]) / sum(heights)
        y = cy + 40 - int(cum * 80)
        pts.append((x, y))
    if len(pts) > 1:
        draw.line(pts, fill=s, width=2)


def draw_web(draw, cx, cy, palette):
    """Draw a cross-impact web."""
    a = palette["accent"]
    s = palette["shape"]
    import math as m
    nodes = []
    for i in range(6):
        angle = m.radians(i * 60 - 90)
        x = cx + int(55 * m.cos(angle))
        y = cy + int(55 * m.sin(angle))
        nodes.append((x, y))
    # Draw connections
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            draw.line([nodes[i], nodes[j]], fill=(*s, 80), width=1)
    # Draw nodes
    for n in nodes:
        draw.ellipse([(n[0]-6, n[1]-6), (n[0]+6, n[1]+6)], fill=a)


def draw_scale(draw, cx, cy, palette):
    """Draw a balance scale for CBA."""
    a = palette["accent"]
    s = palette["shape"]
    # Fulcrum
    draw.polygon([(cx, cy+40), (cx-15, cy+55), (cx+15, cy+55)], fill=s)
    # Beam
    draw.line([(cx-70, cy+30), (cx+70, cy+45)], fill=a, width=3)
    # Pans
    draw.arc([(cx-90, cy+20), (cx-50, cy+50)], 0, 180, fill=a, width=2)
    draw.arc([(cx+50, cy+35), (cx+90, cy+65)], 0, 180, fill=a, width=2)


def draw_chain(draw, cx, cy, palette):
    """Draw Markov chain states."""
    a = palette["accent"]
    s = palette["shape"]
    positions = [(cx-70, cy), (cx, cy), (cx+70, cy)]
    labels = ["G", "F", "X"]
    # Arrows between states
    for i in range(len(positions)-1):
        draw.line([(positions[i][0]+18, positions[i][1]), (positions[i+1][0]-18, positions[i+1][1])], fill=s, width=2)
        # Arrowhead
        ax = positions[i+1][0] - 22
        draw.polygon([(ax, positions[i][1]-5), (ax+8, positions[i][1]), (ax, positions[i][1]+5)], fill=s)
    # Self-loops (small arcs above)
    for pos in positions:
        draw.arc([(pos[0]-20, pos[1]-35), (pos[0]+20, pos[1]-5)], 200, 340, fill=s, width=2)
    # State circles
    for pos in positions:
        draw.ellipse([(pos[0]-16, pos[1]-16), (pos[0]+16, pos[1]+16)], outline=a, width=3)


DRAW_FUNCTIONS = {
    "bowtie": draw_bowtie,
    "tree": draw_tree,
    "dice": draw_dice,
    "grid": draw_grid,
    "layers": draw_layers,
    "fishbone": draw_fishbone,
    "bars": draw_bars,
    "web": draw_web,
    "scale": draw_scale,
    "chain": draw_chain,
}


def generate_header_image(technique_name, title, iso_section):
    """Generate a header image for a screenplay and return base64 encoded PNG."""
    width, height = 1200, 400
    palette = COLOR_PALETTES.get(technique_name, COLOR_PALETTES["Bow Tie Analysis"])
    bg = palette["bg"]
    accent = palette["accent"]
    text_color = palette["text"]

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Background pattern - subtle grid
    for x in range(0, width, 30):
        draw.line([(x, 0), (x, height)], fill=tuple(c + 15 for c in bg), width=1)
    for y in range(0, height, 30):
        draw.line([(0, y), (width, y)], fill=tuple(c + 15 for c in bg), width=1)

    # Draw technique icon on the left
    icon_name = TECHNIQUE_ICONS.get(technique_name, "bowtie")
    draw_fn = DRAW_FUNCTIONS.get(icon_name, draw_bowtie)
    draw_fn(draw, 150, 200, palette)

    # Accent line
    draw.line([(280, 80), (280, 320)], fill=accent, width=3)

    # Title text
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
        sub_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
        iso_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        tag_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except (OSError, IOError):
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
            sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
            iso_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            tag_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except (OSError, IOError):
            title_font = ImageFont.load_default()
            sub_font = title_font
            iso_font = title_font
            tag_font = title_font

    # "STREET MATH" tag
    draw.text((310, 80), "STREET MATH", fill=accent, font=tag_font)

    # Accent underline for tag
    draw.line([(310, 100), (430, 100)], fill=accent, width=2)

    # Main title - wrap if needed
    wrapped = textwrap.wrap(title, width=35)
    y_pos = 120
    for line in wrapped:
        draw.text((310, y_pos), line, fill=text_color, font=title_font)
        y_pos += 50

    # ISO section
    draw.text((310, y_pos + 20), f"ISO 31010 — Section {iso_section}", fill=(*accent, 200), font=iso_font)

    # "A Street Math Screenplay" subtitle
    draw.text((310, y_pos + 50), "A Street Math Screenplay", fill=(180, 180, 180), font=sub_font)

    # Bottom accent bar
    draw.rectangle([(0, height - 4), (width, height)], fill=accent)

    # Encode to base64
    buffer = BytesIO()
    img.save(buffer, format="PNG", quality=95)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# ─── HTML Generation ──────────────────────────────────────────────────────────

def generate_html(technique_name, screenplay_data, image_src,
                   prev_file=None, next_file=None, prev_title=None, next_title=None):
    """Generate a standalone 10-page HTML file for a screenplay."""
    palette = COLOR_PALETTES.get(technique_name, COLOR_PALETTES["Bow Tie Analysis"])
    accent = palette["accent"]
    accent_css = f"rgb({accent[0]},{accent[1]},{accent[2]})"
    bg = palette["bg"]
    bg_css = f"rgb({bg[0]},{bg[1]},{bg[2]})"

    pages_html = ""
    for i, page in enumerate(screenplay_data["pages"]):
        content_escaped = page["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Convert character names to styled spans
        import re
        lines = content_escaped.split("\n")
        formatted_lines = []
        for line in lines:
            stripped = line.strip()
            # Character name (all caps, standalone line)
            if stripped and stripped == stripped.upper() and len(stripped) > 1 and not stripped.startswith("—") and not stripped.startswith("•") and ":" not in stripped and len(stripped) < 40 and stripped.isalpha() or (stripped.endswith(")") and "(" in stripped and stripped.split("(")[0].strip().isupper()):
                formatted_lines.append(f'<span class="character">{stripped}</span>')
            # Stage direction in parentheses
            elif stripped.startswith("(") and stripped.endswith(")"):
                formatted_lines.append(f'<span class="direction">{stripped}</span>')
            # Scene heading
            elif stripped.startswith("FADE IN") or stripped.startswith("FADE OUT") or stripped.startswith("CUT TO"):
                formatted_lines.append(f'<span class="scene-dir">{stripped}</span>')
            else:
                formatted_lines.append(line)

        content_formatted = "\n".join(formatted_lines)

        page_break = 'style="page-break-before: always;"' if i > 0 else ''
        pages_html += f"""
        <div class="page" {page_break}>
            <div class="page-number">— {i+1} of 10 —</div>
            <h2 class="page-heading">{page["heading"]}</h2>
            <div class="screenplay-content"><pre>{content_formatted}</pre></div>
        </div>
"""

    # Build prev/next navigation HTML
    prev_link_top = ""
    next_link_top = ""
    prev_link_bot = ""
    next_link_bot = ""
    if prev_file:
        prev_link_top = f'<a class="topnav-link" href="{prev_file}" title="{prev_title}">&larr; Prev</a>'
        prev_link_bot = f'<a class="bn-link bn-prev" href="{prev_file}"><span class="bn-dir">&larr; Previous</span><span class="bn-title">{prev_title}</span></a>'
    else:
        prev_link_top = '<span class="topnav-link disabled"></span>'
        prev_link_bot = '<span class="bn-link bn-prev disabled"></span>'
    if next_file:
        next_link_top = f'<a class="topnav-link" href="{next_file}" title="{next_title}">Next &rarr;</a>'
        next_link_bot = f'<a class="bn-link bn-next" href="{next_file}"><span class="bn-dir">Next &rarr;</span><span class="bn-title">{next_title}</span></a>'
    else:
        next_link_top = '<span class="topnav-link disabled"></span>'
        next_link_bot = '<span class="bn-link bn-next disabled"></span>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{screenplay_data["title"]}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600;700&display=swap');

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            background: #0a0a0f;
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
        }}

        /* ── Top Navigation Bar ── */
        .topnav {{
            position: sticky;
            top: 0;
            z-index: 200;
            background: rgba(10, 10, 15, 0.92);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid #1a1a2e;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
        }}

        .topnav-link {{
            font-size: 0.85em;
            color: {accent_css};
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 6px;
            transition: background 0.2s, color 0.2s;
            white-space: nowrap;
        }}

        .topnav-link:hover {{
            background: rgba({accent[0]},{accent[1]},{accent[2]}, 0.15);
        }}

        .topnav-link.disabled {{
            visibility: hidden;
            pointer-events: none;
        }}

        .topnav-home {{
            font-family: 'Courier Prime', monospace;
            font-size: 0.8em;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #888;
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 6px;
            transition: background 0.2s, color 0.2s;
        }}

        .topnav-home:hover {{
            background: rgba(255,255,255,0.05);
            color: #fff;
        }}

        .header-image {{
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            display: block;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .meta {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid #222;
            margin-bottom: 40px;
        }}

        .meta h1 {{
            font-size: 2.2em;
            font-weight: 700;
            color: {accent_css};
            margin-bottom: 10px;
            font-family: 'Inter', sans-serif;
        }}

        .meta .iso {{
            font-size: 0.95em;
            color: #888;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        .meta .subtitle {{
            font-size: 1.1em;
            color: #666;
            margin-top: 8px;
            font-style: italic;
        }}

        .page {{
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 1px solid #1a1a2e;
        }}

        .page-number {{
            text-align: center;
            color: {accent_css};
            font-size: 0.85em;
            letter-spacing: 3px;
            margin-bottom: 20px;
            opacity: 0.7;
        }}

        .page-heading {{
            font-family: 'Courier Prime', monospace;
            font-size: 1.1em;
            color: {accent_css};
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 25px;
            padding: 10px 0;
            border-left: 3px solid {accent_css};
            padding-left: 15px;
        }}

        .screenplay-content pre {{
            font-family: 'Courier Prime', monospace;
            font-size: 0.95em;
            line-height: 1.7;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #d0d0d0;
        }}

        .screenplay-content .character {{
            display: block;
            text-align: center;
            color: #fff;
            font-weight: 700;
            margin-top: 20px;
            margin-bottom: 2px;
            letter-spacing: 1px;
        }}

        .screenplay-content .direction {{
            display: block;
            text-align: center;
            color: #888;
            font-style: italic;
            margin-bottom: 5px;
        }}

        .screenplay-content .scene-dir {{
            display: block;
            color: {accent_css};
            font-weight: 700;
            margin: 15px 0;
        }}

        /* ── Bottom Prev/Next Navigation ── */
        .bottom-nav {{
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            gap: 20px;
            margin: 60px 0 40px;
            padding-top: 40px;
            border-top: 1px solid #1a1a2e;
        }}

        .bn-link {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding: 16px 20px;
            background: #111118;
            border: 1px solid #1a1a2e;
            border-radius: 10px;
            text-decoration: none;
            color: inherit;
            flex: 1;
            transition: border-color 0.25s, background 0.25s;
        }}

        .bn-link:hover {{
            border-color: {accent_css};
            background: rgba({accent[0]},{accent[1]},{accent[2]}, 0.05);
        }}

        .bn-link.disabled {{
            visibility: hidden;
            pointer-events: none;
        }}

        .bn-next {{
            text-align: right;
        }}

        .bn-dir {{
            font-size: 0.8em;
            color: {accent_css};
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .bn-title {{
            font-size: 0.95em;
            color: #ccc;
            font-weight: 600;
        }}

        .bn-home {{
            text-align: center;
            margin-bottom: 20px;
        }}

        .bn-home a {{
            font-family: 'Courier Prime', monospace;
            font-size: 0.85em;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #666;
            text-decoration: none;
            padding: 8px 20px;
            border: 1px solid #222;
            border-radius: 6px;
            transition: color 0.2s, border-color 0.2s;
        }}

        .bn-home a:hover {{
            color: {accent_css};
            border-color: {accent_css};
        }}

        /* ── Floating scroll-to-top ── */
        .float-nav {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            z-index: 100;
        }}

        .float-nav a {{
            display: block;
            width: 40px;
            height: 40px;
            background: {accent_css};
            color: #fff;
            text-align: center;
            line-height: 40px;
            border-radius: 50%;
            text-decoration: none;
            font-size: 1.2em;
            opacity: 0.7;
            transition: opacity 0.2s;
        }}

        .float-nav a:hover {{ opacity: 1; }}

        .toc {{
            background: #111118;
            border: 1px solid #222;
            border-radius: 8px;
            padding: 25px 30px;
            margin-bottom: 50px;
        }}

        .toc h3 {{
            color: {accent_css};
            font-size: 0.9em;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 15px;
        }}

        .toc ol {{
            list-style: none;
            counter-reset: toc-counter;
        }}

        .toc li {{
            counter-increment: toc-counter;
            margin-bottom: 8px;
        }}

        .toc li a {{
            color: #999;
            text-decoration: none;
            font-size: 0.9em;
            transition: color 0.2s;
        }}

        .toc li a:hover {{ color: {accent_css}; }}

        .toc li a::before {{
            content: counter(toc-counter, decimal-leading-zero) " — ";
            color: {accent_css};
            opacity: 0.5;
        }}

        .footer {{
            text-align: center;
            padding: 40px 0;
            color: #444;
            font-size: 0.85em;
            border-top: 1px solid #1a1a2e;
        }}

        .footer .accent {{ color: {accent_css}; }}

        @media print {{
            body {{ background: #fff; color: #000; }}
            .topnav, .float-nav, .bottom-nav, .bn-home {{ display: none; }}
            .page {{ page-break-after: always; }}
        }}

        @media (max-width: 600px) {{
            .container {{ padding: 20px 15px; }}
            .meta h1 {{ font-size: 1.6em; }}
            .screenplay-content pre {{ font-size: 0.85em; }}
            .bottom-nav {{ flex-direction: column; }}
            .bn-next {{ text-align: left; }}
        }}
    </style>
</head>
<body>

    <nav class="topnav">
        {prev_link_top}
        <a class="topnav-home" href="index.html">&#9670; Street Math</a>
        {next_link_top}
    </nav>

    <img class="header-image" src="{image_src}" alt="{screenplay_data['title']} header image">

    <div class="container">
        <div class="meta">
            <h1>{screenplay_data["title"]}</h1>
            <div class="iso">ISO 31010 — Section {screenplay_data["iso_section"]}</div>
            <div class="subtitle">{screenplay_data["subtitle"]}</div>
        </div>

        <div class="toc">
            <h3>Scenes</h3>
            <ol>
"""

    for i, page in enumerate(screenplay_data["pages"]):
        html += f'                <li><a href="#page-{i+1}">{page["heading"]}</a></li>\n'

    html += f"""            </ol>
        </div>

{pages_html}

        <div class="bn-home">
            <a href="index.html">&#9670; Back to Street Math Home</a>
        </div>

        <div class="bottom-nav">
            {prev_link_bot}
            {next_link_bot}
        </div>

        <div class="footer">
            <p><span class="accent">STREET MATH</span> — Risk Analysis Through Storytelling</p>
            <p>Based on ISO 31010 Risk Assessment Techniques</p>
        </div>
    </div>

    <nav class="float-nav">
        <a href="#" title="Back to top" aria-label="Back to top">&uarr;</a>
    </nav>

    <script>
        // Add page IDs for TOC navigation
        document.querySelectorAll('.page').forEach((page, i) => {{
            page.id = 'page-' + (i + 1);
        }});
    </script>
</body>
</html>"""

    return html


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("STREET MATH SCREENPLAY GENERATOR")
    print("=" * 60)

    # Read CSV to get the technique list
    techniques = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            techniques.append({
                "technique": row["Technique"].strip('"'),
                "iso_section": row["ISO_31010_Section"].strip('"'),
                "prompt": row["Prompt"].strip('"'),
            })

    print(f"\nFound {len(techniques)} techniques in CSV.\n")

    # Build ordered list of techniques that have screenplays, with filenames
    def make_filename(name):
        safe = name.lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "").replace(",", "")
        return f"screenplay_{safe}.html"

    ordered = []
    for tech in techniques:
        name = tech["technique"]
        if name in SCREENPLAYS:
            ordered.append({
                "name": name,
                "sp": SCREENPLAYS[name],
                "filename": make_filename(name),
            })

    generated = 0
    for idx, entry in enumerate(ordered):
        name = entry["name"]
        sp = entry["sp"]
        filename = entry["filename"]

        # Determine prev/next
        prev_file = ordered[idx - 1]["filename"] if idx > 0 else None
        prev_title = ordered[idx - 1]["sp"]["title"] if idx > 0 else None
        next_file = ordered[idx + 1]["filename"] if idx < len(ordered) - 1 else None
        next_title = ordered[idx + 1]["sp"]["title"] if idx < len(ordered) - 1 else None

        print(f"  [GEN] {sp['title']}...")

        # Use corresponding image from img/ folder
        image_src = f"img/{filename.replace('.html', '.png')}"

        # Generate HTML
        html = generate_html(name, sp, image_src,
                             prev_file=prev_file, next_file=next_file,
                             prev_title=prev_title, next_title=next_title)

        # Write file
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"         → {filename} ({len(sp['pages'])} pages)")
        generated += 1

    print(f"\n{'=' * 60}")
    print(f"Generated {generated} screenplay HTML files in:")
    print(f"  {OUTPUT_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
