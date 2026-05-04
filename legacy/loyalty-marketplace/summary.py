import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------
# The Mutually Beneficial LMV Surge
# Demonstrating how exercising a high-esteem Put Option
# elevates the entire network's baseline value.
# ---------------------------------------------------------

plt.style.use('dark_background')

# Timeframe setup
time = np.linspace(0, 15, 300)

# Phase 1 & 2: Baseline Network LMV vs. Individual effort driving value up
network_baseline = 20 + time * 1.5 + np.sin(time * 1.8) * 2
individual_lmv = 20 + time * 3.5 + np.sin(time * 1.2) * 3

# Phase 3: Individual steps back (locks in Put Option strike price at t=6)
strike_time_idx = 120  # index for t=6
strike_price = individual_lmv[strike_time_idx]

# Individual's perceived daily value drops due to absence, but option remains
individual_lmv[strike_time_idx:] = strike_price - (time[strike_time_idx:] - time[strike_time_idx]) * 2 \
    + np.sin(time[strike_time_idx:] * 3) * 1.5

# Phase 4: Exercising the Put Option (at t=11) creates a systemic surge
exercise_time_idx = 220  # index for t=11
post_exercise_surge = np.copy(network_baseline)

# The network honors the high strike price, permanently shifting the baseline up
post_exercise_surge[exercise_time_idx:] = post_exercise_surge[exercise_time_idx:] \
    + (strike_price - post_exercise_surge[exercise_time_idx])
post_exercise_surge[exercise_time_idx:] += (time[exercise_time_idx:] - time[exercise_time_idx]) * 2.5

fig, ax = plt.subplots(figsize=(14, 8))

# --- Fills ---
# Premium zone: gap between individual and network during buildup
ax.fill_between(time[:strike_time_idx+1],
                network_baseline[:strike_time_idx+1],
                individual_lmv[:strike_time_idx+1],
                alpha=0.07, color='#8866ff', label='Loyalty Premium Built')

# Decay zone: individual dropping below strike
ax.fill_between(time[strike_time_idx:exercise_time_idx],
                individual_lmv[strike_time_idx:exercise_time_idx],
                strike_price,
                where=individual_lmv[strike_time_idx:exercise_time_idx] < strike_price,
                alpha=0.12, color='#ff4444', label='Perceived Value Erosion')

# Surge zone: post-exercise lift above old baseline
ax.fill_between(time[exercise_time_idx:],
                network_baseline[exercise_time_idx:],
                post_exercise_surge[exercise_time_idx:],
                alpha=0.15, color='#44ff88', label='Network Elevation Zone')

# --- Strike price line with subtle glow ---
ax.axhline(y=strike_price, color='#aa66ff', linestyle=':', linewidth=1.5, alpha=0.5)
ax.fill_between(time, strike_price - 0.8, strike_price + 0.8, color='#aa66ff', alpha=0.04)

# --- Lines ---
# Network baseline (pre-exercise)
ax.plot(time[:exercise_time_idx+1], network_baseline[:exercise_time_idx+1],
        color='#666666', linestyle='--', linewidth=1.5, label='Network Baseline LMV')

# Individual LMV — rise phase
ax.plot(time[:strike_time_idx+1], individual_lmv[:strike_time_idx+1],
        color='#6688ff', linewidth=2.5, label="Individual's Active LMV")
for w in [5, 3]:
    ax.plot(time[:strike_time_idx+1], individual_lmv[:strike_time_idx+1],
            color='#6688ff', linewidth=w, alpha=0.08)

# Individual LMV — decline phase
ax.plot(time[strike_time_idx:], individual_lmv[strike_time_idx:],
        color='#ff6688', linewidth=2, alpha=0.7, label='Post-Departure Decline')
for w in [5, 3]:
    ax.plot(time[strike_time_idx:], individual_lmv[strike_time_idx:],
            color='#ff6688', linewidth=w, alpha=0.06)

# Post-exercise surge line with heavy glow
ax.plot(time[exercise_time_idx:], post_exercise_surge[exercise_time_idx:],
        color='#44ff88', linewidth=3, label='New Network Baseline (Post-Surge)')
for w in [8, 6, 4]:
    ax.plot(time[exercise_time_idx:], post_exercise_surge[exercise_time_idx:],
            color='#44ff88', linewidth=w, alpha=0.08)

# --- Event markers with glow rings ---
# Event 1: Leaves on high terms
for s, a in [(600, 0.08), (400, 0.15), (200, 0.25)]:
    ax.scatter(time[strike_time_idx], strike_price, color='#aa66ff', s=s, alpha=a, zorder=4)
ax.scatter(time[strike_time_idx], strike_price, color='#aa66ff', s=130, zorder=5,
           marker='D', edgecolors='white', linewidths=1.2)

# Event 2: Exercises put option
for s, a in [(700, 0.08), (500, 0.15), (300, 0.25)]:
    ax.scatter(time[exercise_time_idx], strike_price, color='#44ff88', s=s, alpha=a, zorder=4)
ax.scatter(time[exercise_time_idx], strike_price, color='#ffcc00', s=180, zorder=5,
           marker='*', edgecolors='#44ff88', linewidths=1.5)

# --- Annotations ---
ax.annotate(
    'LEAVES ON HIGH TERMS\n(Secures Put Option)',
    xy=(time[strike_time_idx], strike_price),
    xytext=(time[strike_time_idx] - 3, strike_price + 14),
    textcoords='data', ha='center', fontsize=10, fontweight='bold', color='#ccaaff',
    arrowprops=dict(arrowstyle='->', color='#ccaaff', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#1a1a2e', ec='#aa66ff', alpha=0.9)
)

ax.annotate(
    'EXERCISES PUT OPTION\n(Network Honors Premium)',
    xy=(time[exercise_time_idx], strike_price),
    xytext=(time[exercise_time_idx] - 0.5, strike_price - 20),
    textcoords='data', ha='center', fontsize=10, fontweight='bold', color='#88ffbb',
    arrowprops=dict(arrowstyle='->', color='#88ffbb', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#1a1a2e', ec='#44ff88', alpha=0.9)
)

# Strike price label
ax.text(0.3, strike_price + 2.5, f'Strike Price: {strike_price:.1f}',
        fontsize=9, color='#aa66ff', alpha=0.7, style='italic')

# --- Formatting ---
ax.set_title("The Mutually Beneficial LMV Surge: Elevating the Network",
             fontsize=16, fontweight='bold', color='white', pad=22)
ax.set_xlabel("Time (Duration of Relationship / Network Lifecycle)", fontsize=11, color='#cccccc')
ax.set_ylabel("Loyalty Marketplace Value (LMV)", fontsize=11, color='#cccccc')
ax.set_ylim(10, max(post_exercise_surge) + 15)
ax.legend(loc='lower right', fontsize=9, framealpha=0.5, ncol=2)
ax.grid(True, alpha=0.12, color='#444444')

plt.tight_layout()
plt.savefig('riskrunners/legacy/loyalty-marketplace/summary.png', dpi=150, bbox_inches='tight')
print('Saved summary.png')
