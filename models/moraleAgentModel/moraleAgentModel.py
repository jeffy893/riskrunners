"""
Morale-Driven Agent-Based Model: Wealth Distribution & Boundary Conditions

This model demonstrates how boundary conditions (policies that prevent extreme 
wealth concentration) keep agents transacting - which is the behavioral signature 
of high morale in a system.

Hypothesis: Communication/transaction networks (a la Conway's Law) require boundary 
conditions to prevent Pareto-style wealth concentration. Without them, morale collapses 
for the majority, transactions cease, and the system dies.

Three scenarios are simulated:
1. No Boundaries (Free Market Collapse) - wealth concentrates, morale drops, transactions stop
2. Soft Boundaries (Progressive Redistribution) - mild floor/ceiling keeps most agents active
3. Active Boundaries (Transaction Incentives) - rewards for transacting with lower-wealth agents

Author: Jefferson (enhanced from original concept)
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from collections import defaultdict

# ─────────────────────────────────────────────────────────────────────────────
# AGENT CLASS
# ─────────────────────────────────────────────────────────────────────────────

class Agent:
    def __init__(self, agent_id, capital):
        self.agent_id = agent_id
        self.capital = capital
        self.morale = 1.0  # 0.0 to 1.0 continuous scale
        self.transactions_this_round = 0
        self.total_transactions = 0
    
    def calculate_morale(self, community_median, community_max):
        """
        Morale is a function of relative standing.
        Agents far below the median lose morale; agents near or above maintain it.
        """
        if community_max == 0:
            self.morale = 0.5
            return
        
        # Relative position in the wealth distribution
        relative_position = self.capital / max(community_median, 1)
        
        # Morale decays when you're far below the median
        if relative_position >= 1.0:
            self.morale = min(1.0, 0.7 + 0.3 * min(relative_position, 2.0) / 2.0)
        else:
            # Below median: morale drops sharply
            self.morale = max(0.05, relative_position ** 1.5)
    
    def willing_to_transact(self):
        """Probability of engaging in a transaction is driven by morale."""
        return random.random() < self.morale
    
    def reset_round(self):
        self.transactions_this_round = 0


# ─────────────────────────────────────────────────────────────────────────────
# SIMULATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def calculate_gini(capitals):
    """Calculate Gini coefficient (0 = perfect equality, 1 = perfect inequality)."""
    sorted_caps = np.sort(capitals)
    n = len(sorted_caps)
    cumulative = np.cumsum(sorted_caps)
    return (2 * np.sum((np.arange(1, n + 1) * sorted_caps)) - (n + 1) * np.sum(sorted_caps)) / (n * np.sum(sorted_caps)) if np.sum(sorted_caps) > 0 else 0


def run_simulation(num_agents=100, num_rounds=300, scenario="none", seed=42):
    """
    Run the agent-based simulation under different boundary conditions.
    
    Scenarios:
    - "none": No intervention. Pure emergent dynamics → wealth concentrates.
    - "redistribution": Soft floor/ceiling on wealth (progressive tax + UBI).
    - "incentive": Bonus rewards for cross-wealth transactions + morale boost.
    """
    random.seed(seed)
    np.random.seed(seed)
    
    # Initialize agents with mild inequality (log-normal starting wealth)
    starting_capitals = np.random.lognormal(mean=3.5, sigma=0.6, size=num_agents)
    agents = [Agent(agent_id=i, capital=cap) for i, cap in enumerate(starting_capitals)]
    
    # Tracking metrics
    gini_history = []
    transaction_count_history = []
    avg_morale_history = []
    wealth_snapshots = []
    snapshot_rounds = [0, num_rounds // 4, num_rounds // 2, 3 * num_rounds // 4, num_rounds - 1]
    
    for round_num in range(num_rounds):
        # Reset round counters
        for agent in agents:
            agent.reset_round()
        
        # Calculate community statistics
        capitals = np.array([a.capital for a in agents])
        community_median = np.median(capitals)
        community_max = np.max(capitals)
        community_mean = np.mean(capitals)
        
        # Update morale
        for agent in agents:
            agent.calculate_morale(community_median, community_max)
        
        # ── INCENTIVE PRE-TRANSACTION PHASE: ACTIVE BOUNDARY CONDITIONS ──
        # These fire BEFORE transactions — they shape willingness to participate.
        if scenario == "incentive":
            # BOUNDARY 1: Participation Morale Floor
            # Any agent who transacted last round gets a morale floor — rewarding
            # the ACT of participation, not the outcome. This is the key mechanism:
            # you maintain engagement by making engagement itself rewarding.
            for agent in agents:
                if agent.total_transactions > 0:
                    # Recent participants get a morale floor (can't drop below 0.55)
                    agent.morale = max(agent.morale, 0.55)
                else:
                    # Even non-participants get a nudge to try
                    agent.morale = max(agent.morale, 0.35)
            
            # BOUNDARY 2: Structural Advantage Dampener
            # Cap how much structural advantage the wealthy can accumulate.
            # In org terms: prevent information/power hoarding.
            # (Applied by reducing the effective wealth ratio in transactions below)
            
            # BOUNDARY 3: Network Vitality Bonus
            # When overall transaction volume is high, everyone benefits slightly
            # (positive externality of a healthy network — more liquidity, more
            # opportunities, more information flow)
            if round_num > 0:
                last_round_txns = transaction_count_history[-1] if transaction_count_history else 0
                max_possible_txns = num_agents * 3 // 2  # theoretical max
                network_health = last_round_txns / max(max_possible_txns, 1)
                for agent in agents:
                    # Everyone gets a small morale bump proportional to network activity
                    agent.morale = min(1.0, agent.morale + network_health * 0.12)
        
        # ── TRANSACTION PHASE ──
        # Multiple transaction opportunities per round
        round_transactions = 0
        
        for _ in range(3):  # 3 transaction opportunities per round
            shuffled = list(agents)
            random.shuffle(shuffled)
            
            for i in range(0, len(shuffled) - 1, 2):
                agent_a = shuffled[i]
                agent_b = shuffled[i + 1]
                
                # Both agents must be willing to transact
                if agent_a.willing_to_transact() and agent_b.willing_to_transact():
                    # Transaction value: proportional to the poorer agent's capital
                    stake_fraction = random.uniform(0.02, 0.12)
                    transaction_value = stake_fraction * min(agent_a.capital, agent_b.capital)
                    
                    # Winner determination: wealthier agent has structural advantage
                    wealth_ratio = agent_a.capital / max(agent_a.capital + agent_b.capital, 1)
                    structural_advantage = (wealth_ratio - 0.5) * 0.3  # up to ±15%
                    
                    # ── INCENTIVE: Dampen structural advantage ──
                    if scenario == "incentive":
                        # Cap structural advantage at ±5% instead of ±15%
                        # The boundary doesn't eliminate competition — it prevents
                        # runaway compounding of positional advantage
                        structural_advantage *= 0.33
                    
                    if random.random() < 0.5 + structural_advantage:
                        agent_a.capital += transaction_value
                        agent_b.capital -= transaction_value
                    else:
                        agent_b.capital += transaction_value
                        agent_a.capital -= transaction_value
                    
                    # ── INCENTIVE POST-TRANSACTION: Cross-wealth bonus ──
                    if scenario == "incentive":
                        # Both parties get rewarded for transacting across wealth gaps.
                        # This is the "diversity dividend" — heterogeneous interactions
                        # create more value than homogeneous ones.
                        wealth_gap = abs(agent_a.capital - agent_b.capital)
                        gap_ratio = wealth_gap / max(community_mean, 1)
                        bonus = transaction_value * min(1.0, gap_ratio * 0.5)
                        
                        poorer = agent_a if agent_a.capital < agent_b.capital else agent_b
                        richer = agent_b if agent_a.capital < agent_b.capital else agent_a
                        # Asymmetric: poorer agent gets more (progressive incentive)
                        poorer.capital += bonus * 0.75
                        richer.capital += bonus * 0.25
                        
                        # Direct morale reward for participating
                        agent_a.morale = min(1.0, agent_a.morale + 0.06)
                        agent_b.morale = min(1.0, agent_b.morale + 0.06)
                    
                    agent_a.transactions_this_round += 1
                    agent_b.transactions_this_round += 1
                    agent_a.total_transactions += 1
                    agent_b.total_transactions += 1
                    round_transactions += 1
        
        # ── REDISTRIBUTION BOUNDARY ──
        if scenario == "redistribution":
            capitals = np.array([a.capital for a in agents])
            mean_wealth = np.mean(capitals)
            
            tax_pool = 0.0
            for agent in agents:
                if agent.capital > mean_wealth * 2.5:
                    excess = agent.capital - mean_wealth * 2.5
                    tax = excess * 0.12
                    agent.capital -= tax
                    tax_pool += tax
            
            # Distribute tax pool as UBI to those below median
            below_median = [a for a in agents if a.capital < community_median]
            if below_median and tax_pool > 0:
                ubi_per_agent = tax_pool / len(below_median)
                for agent in below_median:
                    agent.capital += ubi_per_agent
            
            # Hard floor: no one drops below 10% of mean
            for agent in agents:
                if agent.capital < mean_wealth * 0.1:
                    agent.capital = mean_wealth * 0.1
        
        # Prevent negative wealth (everyone can hit 0 but not below in "none")
        for agent in agents:
            if scenario == "none":
                agent.capital = max(agent.capital, 0.01)
            else:
                agent.capital = max(agent.capital, 0.1)
        
        # ── RECORD METRICS ──
        capitals = np.array([a.capital for a in agents])
        gini_history.append(calculate_gini(capitals))
        transaction_count_history.append(round_transactions)
        avg_morale_history.append(np.mean([a.morale for a in agents]))
        
        if round_num in snapshot_rounds:
            wealth_snapshots.append(capitals.copy())
    
    return {
        "gini_history": gini_history,
        "transaction_count_history": transaction_count_history,
        "avg_morale_history": avg_morale_history,
        "wealth_snapshots": wealth_snapshots,
        "snapshot_rounds": snapshot_rounds,
        "final_capitals": np.array([a.capital for a in agents]),
        "agents": agents
    }


# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def generate_visualization(results_none, results_redist, results_incentive, num_rounds=200):
    """Generate a beautiful multi-panel visualization."""
    
    # Color palette
    COLOR_NONE = "#E74C3C"       # Red - danger, collapse
    COLOR_REDIST = "#F39C12"     # Amber - moderate
    COLOR_INCENTIVE = "#27AE60"  # Green - healthy
    BG_COLOR = "#1a1a2e"
    PANEL_BG = "#16213e"
    TEXT_COLOR = "#e8e8e8"
    GRID_COLOR = "#2a2a4a"
    
    fig = plt.figure(figsize=(20, 14), facecolor=BG_COLOR)
    fig.suptitle(
        "Boundary Conditions & Morale: Why Networks Need Guardrails to Keep Transacting",
        fontsize=16, fontweight='bold', color=TEXT_COLOR, y=0.97
    )
    
    gs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35,
                  left=0.06, right=0.96, top=0.92, bottom=0.06)
    
    scenarios = [
        ("No Boundaries\n(Free Market)", results_none, COLOR_NONE),
        ("Soft Boundaries\n(Redistribution)", results_redist, COLOR_REDIST),
        ("Active Boundaries\n(Transaction Incentives)", results_incentive, COLOR_INCENTIVE),
    ]
    
    rounds = range(num_rounds)
    
    # ── ROW 1: Gini Coefficient Over Time ──
    ax_gini = fig.add_subplot(gs[0, :])
    ax_gini.set_facecolor(PANEL_BG)
    for label, results, color in scenarios:
        ax_gini.plot(rounds, results["gini_history"], color=color, linewidth=2.5, 
                     label=label.replace('\n', ' '), alpha=0.9)
    ax_gini.axhline(y=0.4, color='#ffffff', linestyle='--', alpha=0.3, linewidth=1)
    ax_gini.text(num_rounds * 0.82, 0.42, "Dangerous Inequality Threshold", 
                 color='#ffffff', alpha=0.5, fontsize=9)
    ax_gini.set_xlabel("Simulation Round", color=TEXT_COLOR, fontsize=10)
    ax_gini.set_ylabel("Gini Coefficient", color=TEXT_COLOR, fontsize=10)
    ax_gini.set_title("Wealth Inequality Over Time (Gini: 0=Equal, 1=One Agent Has All)", 
                      color=TEXT_COLOR, fontsize=12, fontweight='bold', pad=10)
    ax_gini.legend(loc='upper left', fontsize=10, framealpha=0.8)
    ax_gini.set_ylim(0, 1)
    ax_gini.tick_params(colors=TEXT_COLOR)
    ax_gini.grid(True, alpha=0.2, color=GRID_COLOR)
    ax_gini.spines['bottom'].set_color(GRID_COLOR)
    ax_gini.spines['left'].set_color(GRID_COLOR)
    ax_gini.spines['top'].set_visible(False)
    ax_gini.spines['right'].set_visible(False)
    
    # ── ROW 2: Transaction Volume & Average Morale ──
    ax_trans = fig.add_subplot(gs[1, 0:2])
    ax_trans.set_facecolor(PANEL_BG)
    for label, results, color in scenarios:
        # Smooth the transaction data
        window = 5
        smoothed = np.convolve(results["transaction_count_history"], 
                               np.ones(window)/window, mode='valid')
        ax_trans.plot(range(len(smoothed)), smoothed, color=color, linewidth=2, 
                      label=label.replace('\n', ' '), alpha=0.9)
    ax_trans.set_xlabel("Simulation Round", color=TEXT_COLOR, fontsize=10)
    ax_trans.set_ylabel("Transactions per Round", color=TEXT_COLOR, fontsize=10)
    ax_trans.set_title("Transaction Volume (System Vitality)", 
                      color=TEXT_COLOR, fontsize=12, fontweight='bold', pad=10)
    ax_trans.legend(loc='best', fontsize=9, framealpha=0.8)
    ax_trans.tick_params(colors=TEXT_COLOR)
    ax_trans.grid(True, alpha=0.2, color=GRID_COLOR)
    ax_trans.spines['bottom'].set_color(GRID_COLOR)
    ax_trans.spines['left'].set_color(GRID_COLOR)
    ax_trans.spines['top'].set_visible(False)
    ax_trans.spines['right'].set_visible(False)
    
    ax_morale = fig.add_subplot(gs[1, 2])
    ax_morale.set_facecolor(PANEL_BG)
    for label, results, color in scenarios:
        ax_morale.plot(rounds, results["avg_morale_history"], color=color, linewidth=2.5, 
                       label=label.replace('\n', ' '), alpha=0.9)
    ax_morale.set_xlabel("Round", color=TEXT_COLOR, fontsize=10)
    ax_morale.set_ylabel("Avg Morale", color=TEXT_COLOR, fontsize=10)
    ax_morale.set_title("Average Agent Morale", 
                        color=TEXT_COLOR, fontsize=12, fontweight='bold', pad=10)
    ax_morale.set_ylim(0, 1)
    ax_morale.tick_params(colors=TEXT_COLOR)
    ax_morale.grid(True, alpha=0.2, color=GRID_COLOR)
    ax_morale.spines['bottom'].set_color(GRID_COLOR)
    ax_morale.spines['left'].set_color(GRID_COLOR)
    ax_morale.spines['top'].set_visible(False)
    ax_morale.spines['right'].set_visible(False)
    
    # ── ROW 3: Final Wealth Distribution (Histogram) ──
    for idx, (label, results, color) in enumerate(scenarios):
        ax = fig.add_subplot(gs[2, idx])
        ax.set_facecolor(PANEL_BG)
        
        final_caps = results["final_capitals"]
        # Log-scale bins for better visualization of Pareto-like distributions
        bins = np.logspace(np.log10(max(0.1, final_caps.min())), 
                           np.log10(final_caps.max() + 1), 25)
        ax.hist(final_caps, bins=bins, color=color, alpha=0.8, edgecolor='white', linewidth=0.5)
        ax.set_xscale('log')
        ax.set_xlabel("Wealth (log scale)", color=TEXT_COLOR, fontsize=9)
        ax.set_ylabel("# Agents", color=TEXT_COLOR, fontsize=9)
        ax.set_title(label, color=color, fontsize=11, fontweight='bold', pad=8)
        ax.tick_params(colors=TEXT_COLOR, labelsize=8)
        ax.grid(True, alpha=0.2, color=GRID_COLOR)
        ax.spines['bottom'].set_color(GRID_COLOR)
        ax.spines['left'].set_color(GRID_COLOR)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add Gini annotation
        final_gini = results["gini_history"][-1]
        total_trans = sum(results["transaction_count_history"])
        ax.text(0.95, 0.92, f"Gini: {final_gini:.3f}\nTotal Txns: {total_trans:,}", 
                transform=ax.transAxes, fontsize=9, color=TEXT_COLOR,
                ha='right', va='top', 
                bbox=dict(boxstyle='round,pad=0.3', facecolor=PANEL_BG, 
                          edgecolor=color, alpha=0.9))
    
    # ── Footer annotation ──
    fig.text(0.5, 0.01, 
             "Model: 100 agents, 200 rounds, bilateral transactions weighted by morale | "
             "Hypothesis: Boundary conditions maintain morale → sustain transactions → healthier wealth distribution",
             ha='center', fontsize=9, color='#888888', style='italic')
    
    output_path = "/Users/jefferson/000_coderepo/riskrunners/models/moraleAgentModel/morale_boundary_conditions.png"
    plt.savefig(output_path, dpi=180, facecolor=BG_COLOR, bbox_inches='tight')
    plt.close()
    print(f"Visualization saved to: {output_path}")
    return output_path


# ─────────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    NUM_AGENTS = 100
    NUM_ROUNDS = 300
    
    print("=" * 70)
    print("MORALE-DRIVEN AGENT MODEL: BOUNDARY CONDITIONS & WEALTH DISTRIBUTION")
    print("=" * 70)
    
    print("\n[1/3] Running scenario: No Boundaries (free market dynamics)...")
    results_none = run_simulation(NUM_AGENTS, NUM_ROUNDS, scenario="none", seed=42)
    print(f"      Final Gini: {results_none['gini_history'][-1]:.4f} | "
          f"Avg Morale: {results_none['avg_morale_history'][-1]:.4f} | "
          f"Total Transactions: {sum(results_none['transaction_count_history']):,}")
    
    print("\n[2/3] Running scenario: Soft Boundaries (redistribution)...")
    results_redist = run_simulation(NUM_AGENTS, NUM_ROUNDS, scenario="redistribution", seed=42)
    print(f"      Final Gini: {results_redist['gini_history'][-1]:.4f} | "
          f"Avg Morale: {results_redist['avg_morale_history'][-1]:.4f} | "
          f"Total Transactions: {sum(results_redist['transaction_count_history']):,}")
    
    print("\n[3/3] Running scenario: Active Boundaries (transaction incentives)...")
    results_incentive = run_simulation(NUM_AGENTS, NUM_ROUNDS, scenario="incentive", seed=42)
    print(f"      Final Gini: {results_incentive['gini_history'][-1]:.4f} | "
          f"Avg Morale: {results_incentive['avg_morale_history'][-1]:.4f} | "
          f"Total Transactions: {sum(results_incentive['transaction_count_history']):,}")
    
    print("\n[*] Generating multi-panel visualization...")
    output_path = generate_visualization(results_none, results_redist, results_incentive, NUM_ROUNDS)
    
    print("\n" + "=" * 70)
    print("KEY FINDINGS:")
    print("-" * 70)
    print(f"  Without boundaries:  Gini → {results_none['gini_history'][-1]:.3f}  "
          f"(morale collapses to {results_none['avg_morale_history'][-1]:.3f})")
    print(f"  With redistribution: Gini → {results_redist['gini_history'][-1]:.3f}  "
          f"(morale stabilizes at {results_redist['avg_morale_history'][-1]:.3f})")
    print(f"  With incentives:     Gini → {results_incentive['gini_history'][-1]:.3f}  "
          f"(morale thrives at {results_incentive['avg_morale_history'][-1]:.3f})")
    print("=" * 70)
    print("\nConclusion: Boundary conditions don't just redistribute wealth —")
    print("they sustain the MORALE that keeps agents TRANSACTING.")
    print("Dead networks aren't poor. They're demoralized.\n")
