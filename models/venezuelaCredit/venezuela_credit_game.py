"""
Venezuela Credit-for-Refugees Game Theory Simulation
=====================================================
Models the strategic interaction where Venezuela directs refugee flows
toward countries holding lines of credit in Venezuelan oil — using
humanitarian migration as leverage to pressure creditors into yielding
or renegotiating their credit positions.

Players:
  - Venezuela: Directs refugees toward creditor nations as leverage
  - Creditor Countries: Hold oil credit lines, face pressure to yield
  - International Organizations: Can provide aid that shifts incentives
  - Refugee Advocate NGOs: Apply public/media pressure on creditors

Output: PNG visualization of equilibrium outcomes and payoff trajectories.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

np.random.seed(42)

# ─── Configuration ───────────────────────────────────────────────────────────
NUM_ROUNDS = 50
NUM_SIMULATIONS = 500  # Monte Carlo runs

# Strategy definitions — clarified for the credit-leverage dynamic
STRATEGY_LABELS = {
    "Venezuela": [
        "Low Refugee Flow",           # Minimal displacement toward creditors
        "Flood Creditor Nations",     # Mass refugee direction to credit-holders as leverage
        "Conditional Refugee Flow",   # Tied explicitly to credit renegotiation offers
    ],
    "Creditors": [
        "Reject & Hold Credit",       # Refuse refugees, retain full credit position
        "Accept & Yield Credit",      # Accept refugees, surrender credit line
        "Renegotiate Terms",          # Accept some refugees, negotiate partial credit relief
    ],
    "Intl Orgs": [
        "No Intervention",            # Stay out
        "Aid Venezuela",              # Fund Venezuela to reduce outflows
        "Compensate Creditors",       # Offset creditor losses for accepting refugees
        "Broker Deal (Aid Both)",     # Full mediation package
    ],
    "NGOs": [
        "Silent",                     # No public campaign
        "Moderate Advocacy",          # Media pressure on creditors
        "Aggressive Campaign",        # Full-court press on creditors to accept
    ],
}

# ─── Payoff Functions (Rechecked) ────────────────────────────────────────────
# Payoff scale: units represent normalized geopolitical utility
# Credit line value ~5.0 baseline (significant economic asset)
# Reputation effects compound over rounds

def venezuela_payoff(v_strat, c_strat, io_strat, ngo_strat, reputation_v):
    """
    Venezuela's objective: Use refugee flows to pressure creditors into
    yielding credit positions. Gains come from creditors capitulating,
    diplomatic reputation, and international aid.
    """
    base = 0.0

    # Strategy payoffs — flooding creditors is high-reward if they capitulate
    if v_strat == 1:  # Flood Creditor Nations
        base += 2.0  # base cost of organizing mass displacement
        if c_strat >= 1:  # creditors capitulate in some form
            base += 5.0  # major win — leverage worked
        else:
            base += 1.0  # still builds pressure, some diplomatic gain
        base += reputation_v * 0.5  # reputation multiplier
    elif v_strat == 2:  # Conditional Flow
        base += 1.5
        if c_strat == 2:  # renegotiation matches conditional offer
            base += 4.0
        elif c_strat == 1:
            base += 3.5
        base += reputation_v * 0.4
    else:  # Low Flow
        base += 0.5  # minimal leverage applied

    # International aid to Venezuela
    if io_strat in (1, 3):
        base += 2.0

    # NGO pressure on creditors indirectly helps Venezuela
    if ngo_strat >= 1 and c_strat == 0:
        base += 0.5 * ngo_strat  # NGOs softening creditor resistance

    return base


def creditor_payoff(v_strat, c_strat, io_strat, ngo_strat, reputation_c, credit_value):
    """
    Creditors weigh: keeping credit lines (economic) vs. accepting refugees
    (reputation + intl pressure relief). Rejection preserves wealth but
    accumulates diplomatic and PR costs.
    """
    base = 0.0

    if c_strat == 0:  # Reject & Hold Credit
        base += credit_value  # full economic value retained
        # Costs scale with how much pressure Venezuela is applying
        if v_strat == 1:  # mass refugee pressure
            base -= 2.5  # diplomatic cost of visible rejection during crisis
            base -= reputation_c * 1.0  # reputation damage compounds
        elif v_strat == 2:
            base -= 1.5
        if ngo_strat >= 1:
            base -= 1.5 * ngo_strat  # NGO backlash

    elif c_strat == 1:  # Accept & Yield Credit
        base -= credit_value * 0.7  # lose most of the credit position
        base += reputation_c * 2.5  # significant reputation boost
        if io_strat in (2, 3):  # international compensation
            base += credit_value * 0.3  # partial offset from intl orgs
        if v_strat == 1:
            base += 1.0  # relief from pressure

    else:  # Renegotiate Terms
        base -= credit_value * 0.35  # partial credit concession
        base += reputation_c * 1.5   # moderate reputation gain
        if io_strat in (2, 3):
            base += credit_value * 0.15
        if v_strat == 2:  # conditional flow aligns with renegotiation
            base += 2.0  # mutual benefit from structured deal

    return base


def intl_org_payoff(v_strat, c_strat, io_strat, ngo_strat):
    """
    International orgs maximize humanitarian outcomes (refugees resettled)
    while minimizing expenditure. Brokering deals is most efficient.
    """
    base = 0.0
    refugees_resettled = 0

    if v_strat >= 1 and c_strat >= 1:
        refugees_resettled = 4 if v_strat == 1 else 2

    base += refugees_resettled * 1.5  # humanitarian outcome value

    # Cost of intervention
    costs = [0, -1.5, -2.0, -3.0]
    base += costs[io_strat]

    # Efficiency bonus: brokering when both sides cooperate
    if io_strat == 3 and c_strat >= 1 and v_strat >= 1:
        base += 2.5  # successful mediation bonus

    # NGO alignment amplifies effectiveness
    if ngo_strat >= 1 and io_strat >= 1:
        base += 1.0

    return base


def ngo_payoff(v_strat, c_strat, io_strat, ngo_strat):
    """
    NGOs maximize refugee resettlement. Pressure campaigns cost resources
    but pay off only if they shift creditor behavior.
    """
    base = 0.0
    refugees_resettled = 0

    if v_strat >= 1 and c_strat >= 1:
        refugees_resettled = 4 if v_strat == 1 else 2

    base += refugees_resettled * 2.5  # core mission payoff

    # Campaign costs
    base -= ngo_strat * 1.5

    # Effectiveness bonus — pressure paid off
    if ngo_strat >= 1 and c_strat >= 1:
        base += 2.5  # advocacy moved the needle

    # Wasted effort penalty — pressure applied but creditors still rejected
    if ngo_strat >= 1 and c_strat == 0:
        base -= 1.0  # diminishing returns on failed campaigns

    return base


# ─── Adaptive Strategy Selection (Reinforcement Learning) ────────────────────

def softmax(q_values, temperature=1.0):
    """Softmax strategy selection with exploration."""
    exp_q = np.exp((q_values - np.max(q_values)) / max(temperature, 0.1))
    return exp_q / exp_q.sum()


def run_simulation():
    """Run a single multi-round simulation with adaptive players."""
    q_venezuela = np.zeros(3)
    q_creditors = np.zeros(3)
    q_intl_orgs = np.zeros(4)
    q_ngos = np.zeros(3)

    reputation_v = 0.5
    reputation_c = 0.5
    credit_value = 5.0  # initial credit line value (significant asset)

    history = {
        "venezuela": {"strategies": [], "payoffs": []},
        "creditors": {"strategies": [], "payoffs": []},
        "intl_orgs": {"strategies": [], "payoffs": []},
        "ngos": {"strategies": [], "payoffs": []},
    }

    temperature = 2.0  # exploration (decays over rounds)

    for round_num in range(NUM_ROUNDS):
        # Strategy selection via softmax
        p_v = softmax(q_venezuela, temperature)
        p_c = softmax(q_creditors, temperature)
        p_io = softmax(q_intl_orgs, temperature)
        p_n = softmax(q_ngos, temperature)

        v_strat = np.random.choice(3, p=p_v)
        c_strat = np.random.choice(3, p=p_c)
        io_strat = np.random.choice(4, p=p_io)
        ngo_strat = np.random.choice(3, p=p_n)

        # Public opinion shock
        opinion_shock = np.random.normal(0, 0.2)

        # Calculate payoffs
        pv = venezuela_payoff(v_strat, c_strat, io_strat, ngo_strat, reputation_v)
        pc = creditor_payoff(v_strat, c_strat, io_strat, ngo_strat, reputation_c, credit_value)
        pio = intl_org_payoff(v_strat, c_strat, io_strat, ngo_strat)
        pn = ngo_payoff(v_strat, c_strat, io_strat, ngo_strat)

        # Apply opinion shock (affects reputation-sensitive players more)
        pv += opinion_shock * 0.5
        pc += opinion_shock

        # Update Q-values (decaying learning rate)
        lr = 0.3 / (1 + round_num * 0.04)
        q_venezuela[v_strat] += lr * (pv - q_venezuela[v_strat])
        q_creditors[c_strat] += lr * (pc - q_creditors[c_strat])
        q_intl_orgs[io_strat] += lr * (pio - q_intl_orgs[io_strat])
        q_ngos[ngo_strat] += lr * (pn - q_ngos[ngo_strat])

        # Reputation dynamics (bounded 0-1)
        if v_strat >= 1:
            reputation_v = min(1.0, reputation_v + 0.015)
        else:
            reputation_v = max(0.0, reputation_v - 0.02)

        if c_strat >= 1:
            reputation_c = min(1.0, reputation_c + 0.02)
        else:
            reputation_c = max(0.0, reputation_c - 0.025)

        # Credit depreciates when yielded
        if c_strat == 1:
            credit_value *= 0.93
        elif c_strat == 2:
            credit_value *= 0.97

        # Decay exploration
        temperature *= 0.96

        # Record
        history["venezuela"]["strategies"].append(v_strat)
        history["venezuela"]["payoffs"].append(pv)
        history["creditors"]["strategies"].append(c_strat)
        history["creditors"]["payoffs"].append(pc)
        history["intl_orgs"]["strategies"].append(io_strat)
        history["intl_orgs"]["payoffs"].append(pio)
        history["ngos"]["strategies"].append(ngo_strat)
        history["ngos"]["payoffs"].append(pn)

    return history


# ─── Monte Carlo Aggregation ─────────────────────────────────────────────────

def run_monte_carlo():
    """Run multiple simulations and aggregate results."""
    all_payoffs = {"venezuela": [], "creditors": [], "intl_orgs": [], "ngos": []}
    all_strategies = {"venezuela": [], "creditors": [], "intl_orgs": [], "ngos": []}
    final_strategies = {"venezuela": [], "creditors": [], "intl_orgs": [], "ngos": []}

    for _ in range(NUM_SIMULATIONS):
        history = run_simulation()
        for player in all_payoffs:
            all_payoffs[player].append(history[player]["payoffs"])
            all_strategies[player].append(history[player]["strategies"])
            # Equilibrium = mode of final 10 rounds
            final_strats = history[player]["strategies"][-10:]
            mode_strat = max(set(final_strats), key=final_strats.count)
            final_strategies[player].append(mode_strat)

    return all_payoffs, all_strategies, final_strategies


# ─── Visualization ───────────────────────────────────────────────────────────

def create_visualization(all_payoffs, all_strategies, final_strategies):
    """Generate comprehensive PNG visualization with clear strategy explanations."""
    fig = plt.figure(figsize=(20, 16), facecolor="#1a1a2e")

    # Main title with scenario description
    fig.suptitle(
        "Venezuela Refugee-as-Leverage Game Theory\n"
        "Venezuela directs refugee flows toward oil-credit-holding nations to pressure them into yielding credit positions",
        fontsize=14,
        fontweight="bold",
        color="white",
        y=0.98,
        linespacing=1.4,
    )

    colors = {
        "venezuela": "#e63946",
        "creditors": "#457b9d",
        "intl_orgs": "#2a9d8f",
        "ngos": "#e9c46a",
    }
    player_names = {
        "venezuela": "Venezuela",
        "creditors": "Creditor Countries",
        "intl_orgs": "International Orgs",
        "ngos": "NGOs",
    }

    # ── Panel 1: Strategy Explanation + Equilibrium ──
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_facecolor("#16213e")
    ax1.axis("off")

    explanation = (
        "STRATEGY BREAKDOWN\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "VENEZUELA (Refugee Grantor / Leverage Player)\n"
        "  • Low Flow — minimal refugee displacement\n"
        "  • Flood Creditor Nations — mass refugee\n"
        "    direction toward credit-holders as\n"
        "    geopolitical pressure to yield oil credit\n"
        "  • Conditional Flow — refugees tied to\n"
        "    explicit credit renegotiation offers\n\n"
        "CREDITOR COUNTRIES (Oil Credit Holders)\n"
        "  • Reject & Hold — refuse refugees, keep credit\n"
        "  • Accept & Yield — take refugees, lose credit\n"
        "  • Renegotiate — partial deal on both\n\n"
        "INTL ORGS — Mediate / compensate / stay out\n"
        "NGOs — Pressure creditors via public campaigns"
    )

    ax1.text(
        0.05, 0.95, explanation, ha="left", va="top",
        fontsize=9.5, color="white", transform=ax1.transAxes,
        family="monospace", linespacing=1.4,
    )

    # ── Panel 2: Equilibrium Convergence Bars ──
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_facecolor("#16213e")

    strategy_names_map = {
        "venezuela": STRATEGY_LABELS["Venezuela"],
        "creditors": STRATEGY_LABELS["Creditors"],
        "intl_orgs": STRATEGY_LABELS["Intl Orgs"],
        "ngos": STRATEGY_LABELS["NGOs"],
    }

    for i, (player, strats) in enumerate(final_strategies.items()):
        unique_vals, counts = np.unique(strats, return_counts=True)
        probs = counts / counts.sum()
        dominant_idx = unique_vals[np.argmax(probs)]
        dominant_pct = probs.max() * 100
        ax2.bar(
            i, dominant_pct, width=0.6,
            color=colors[player], alpha=0.85,
            edgecolor="white", linewidth=0.5,
        )
        strat_label = strategy_names_map[player][dominant_idx]
        ax2.text(
            i, dominant_pct + 1.5,
            f"{strat_label}\n({dominant_pct:.1f}%)",
            ha="center", va="bottom", color="white",
            fontsize=8, fontweight="bold",
        )

    ax2.set_xticks(range(4))
    ax2.set_xticklabels(
        [player_names[p] for p in final_strategies.keys()],
        color="white", fontsize=9,
    )
    ax2.set_ylabel("Convergence Frequency (%)", color="white", fontsize=10)
    ax2.set_title(
        "Dominant Strategy at Equilibrium (Final 10 Rounds)",
        color="white", fontsize=11,
    )
    ax2.set_ylim(0, 100)
    ax2.tick_params(colors="white")
    ax2.spines["bottom"].set_color("gray")
    ax2.spines["left"].set_color("gray")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", alpha=0.2, color="gray")

    # ── Panel 3: Payoff Trajectories ──
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor("#16213e")
    for player, color in colors.items():
        mean_payoffs = np.mean(all_payoffs[player], axis=0)
        cumulative = np.cumsum(mean_payoffs)
        std_payoffs = np.std(
            np.cumsum(np.array(all_payoffs[player]), axis=1), axis=0
        )
        rounds = np.arange(1, NUM_ROUNDS + 1)
        ax3.plot(
            rounds, cumulative, color=color, linewidth=2,
            label=player_names[player],
        )
        ax3.fill_between(
            rounds,
            cumulative - std_payoffs * 0.3,
            cumulative + std_payoffs * 0.3,
            alpha=0.15, color=color,
        )
    ax3.set_xlabel("Round", color="white", fontsize=10)
    ax3.set_ylabel("Cumulative Payoff", color="white", fontsize=10)
    ax3.set_title(
        "Payoff Trajectories — Venezuela gains while creditors stagnate",
        color="white", fontsize=11,
    )
    ax3.legend(
        loc="upper left", fontsize=9,
        facecolor="#16213e", edgecolor="gray", labelcolor="white",
    )
    ax3.tick_params(colors="white")
    ax3.spines["bottom"].set_color("gray")
    ax3.spines["left"].set_color("gray")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.grid(alpha=0.2, color="gray")

    # ── Panel 4: Outcome Summary & Interpretation ──
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_facecolor("#16213e")
    ax4.axis("off")

    # Determine dominant outcome
    v_dominant = max(
        set(final_strategies["venezuela"]),
        key=final_strategies["venezuela"].count,
    )
    c_dominant = max(
        set(final_strategies["creditors"]),
        key=final_strategies["creditors"].count,
    )

    # Calculate percentages for summary
    v_counts = np.unique(final_strategies["venezuela"], return_counts=True)
    c_counts = np.unique(final_strategies["creditors"], return_counts=True)
    io_counts = np.unique(final_strategies["intl_orgs"], return_counts=True)
    n_counts = np.unique(final_strategies["ngos"], return_counts=True)

    if v_dominant >= 1 and c_dominant >= 1:
        outcome = "COOPERATIVE EQUILIBRIUM"
        outcome_color = "#2a9d8f"
        outcome_desc = (
            "Creditors find that yielding credit positions\n"
            "in exchange for refugee acceptance produces\n"
            "higher long-term payoffs than resisting."
        )
    elif c_dominant == 0:
        outcome = "STALEMATE — LEVERAGE FAILS TO CONVERT"
        outcome_color = "#e63946"
        outcome_desc = (
            "Venezuela floods creditor nations with refugees,\n"
            "but creditors absorb the reputational cost rather\n"
            "than surrender economically valuable credit lines.\n"
            "The leverage pressures but does not convert."
        )
    else:
        outcome = "PARTIAL COOPERATION"
        outcome_color = "#e9c46a"
        outcome_desc = (
            "Mixed strategies — some creditors renegotiate\n"
            "while others hold firm."
        )

    ax4.text(
        0.5, 0.95, "SIMULATION RESULT", ha="center", va="top",
        fontsize=10, color="gray", transform=ax4.transAxes,
    )
    ax4.text(
        0.5, 0.88, outcome, ha="center", va="top",
        fontsize=14, fontweight="bold", color=outcome_color,
        transform=ax4.transAxes,
    )
    ax4.text(
        0.5, 0.75, outcome_desc, ha="center", va="top",
        fontsize=10, color="white", transform=ax4.transAxes,
        linespacing=1.5,
    )

    # Key interpretation
    interpretation = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "INTERPRETATION\n\n"
        "• Venezuela's \"Flood Creditor Nations\" strategy\n"
        "  dominates because it costs little to direct\n"
        "  refugee flows and builds diplomatic capital\n"
        "  regardless of creditor response.\n\n"
        "• Creditors rationally hold credit positions\n"
        "  because oil credit value > reputation cost\n"
        "  in the short-to-medium term.\n\n"
        "• Breaking this equilibrium requires external\n"
        "  mechanisms that change the economic calculus\n"
        "  (intl compensation, debt restructuring).\n\n"
        f"Based on {NUM_SIMULATIONS} Monte Carlo simulations × "
        f"{NUM_ROUNDS} rounds"
    )
    ax4.text(
        0.5, 0.55, interpretation, ha="center", va="top",
        fontsize=9, color="white", transform=ax4.transAxes,
        family="monospace", linespacing=1.4,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.94])

    output_path = Path(__file__).parent / "venezuela_credit_game_theory.png"
    plt.savefig(
        output_path, dpi=150, bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    plt.close()
    print(f"\nVisualization saved to: {output_path}")
    return output_path


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Running Monte Carlo simulation...")
    print(f"  Simulations: {NUM_SIMULATIONS}")
    print(f"  Rounds per sim: {NUM_ROUNDS}")
    print()

    all_payoffs, all_strategies, final_strategies = run_monte_carlo()

    # Print equilibrium results
    strategy_names_map = {
        "venezuela": STRATEGY_LABELS["Venezuela"],
        "creditors": STRATEGY_LABELS["Creditors"],
        "intl_orgs": STRATEGY_LABELS["Intl Orgs"],
        "ngos": STRATEGY_LABELS["NGOs"],
    }
    player_names = {
        "venezuela": "Venezuela",
        "creditors": "Creditor Countries",
        "intl_orgs": "International Orgs",
        "ngos": "NGOs",
    }

    print("═══ Equilibrium Strategies (Final 10 Rounds Mode) ═══")
    for player, strats in final_strategies.items():
        unique_vals, counts = np.unique(strats, return_counts=True)
        print(f"\n  {player_names[player]}:")
        for val, count in zip(unique_vals, counts):
            pct = count / len(strats) * 100
            label = strategy_names_map[player][val]
            print(f"    {label:.<35} {pct:>5.1f}%")

    print("\n═══ Generating Visualization ═══")
    output_path = create_visualization(all_payoffs, all_strategies, final_strategies)
    print("Done.")
