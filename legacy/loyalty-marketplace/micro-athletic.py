import matplotlib.pyplot as plt
import numpy as np

# Scenario: Built high loyalty, left on great terms (bought put).
# Market dipped, exercised put later for business ROI.

plt.style.use('dark_background')

time = np.linspace(0, 12, 200)
lmv = 10 + time * 3 + np.sin(time * 2) * 2  # Organic rise
idx_peak = 66   # ~time=4
idx_exercise = 133  # ~time=8
lmv[idx_peak:] = lmv[idx_peak] - (time[idx_peak:] - time[idx_peak]) * 1.5 + np.sin(time[idx_peak:] * 3) * 1.5
strike_price = lmv[idx_peak]

fig, ax = plt.subplots(figsize=(12, 7))

# Strike price line with subtle glow
ax.axhline(y=strike_price, color='#44ff88', linestyle=':', linewidth=1.5, alpha=0.6, label='Strike Price (Esteem Base)')
ax.fill_between(time, strike_price - 0.5, strike_price + 0.5, color='#44ff88', alpha=0.05)

# Fill the "value erosion" zone below strike after leaving
ax.fill_between(time[idx_peak:], lmv[idx_peak:], strike_price,
                where=lmv[idx_peak:] < strike_price,
                alpha=0.12, color='#ff4444', label='Value Erosion')

# Main LMV line — rise phase
ax.plot(time[:idx_peak+1], lmv[:idx_peak+1], color='#aa66ff', linewidth=2.5, label='Network LMV')
for w in [5, 3]:
    ax.plot(time[:idx_peak+1], lmv[:idx_peak+1], color='#aa66ff', linewidth=w, alpha=0.08)

# Main LMV line — decline phase
ax.plot(time[idx_peak:], lmv[idx_peak:], color='#ff6688', linewidth=2, label='Post-Departure Decline')
for w in [5, 3]:
    ax.plot(time[idx_peak:], lmv[idx_peak:], color='#ff6688', linewidth=w, alpha=0.08)

# Event markers with glow
for s, a in [(500, 0.1), (300, 0.2)]:
    ax.scatter(time[idx_peak], lmv[idx_peak], color='#44ff88', s=s, alpha=a, zorder=4)
ax.scatter(time[idx_peak], lmv[idx_peak], color='#44ff88', s=120, zorder=5, marker='D', edgecolors='white', linewidths=1)

for s, a in [(500, 0.1), (300, 0.2)]:
    ax.scatter(time[idx_exercise], lmv[idx_exercise], color='#44aaff', s=s, alpha=a, zorder=4)
ax.scatter(time[idx_exercise], lmv[idx_exercise], color='#44aaff', s=120, zorder=5, marker='*', edgecolors='white', linewidths=1)

# Annotations
ax.annotate(
    'LEFT ON HIGH TERMS\n(Bought Put Option)',
    xy=(time[idx_peak], lmv[idx_peak]), xytext=(time[idx_peak] - 2, lmv[idx_peak] + 10),
    textcoords='data', ha='center', fontsize=9, fontweight='bold', color='#88ffbb',
    arrowprops=dict(arrowstyle='->', color='#88ffbb', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#44ff88', alpha=0.85)
)

ax.annotate(
    'EXERCISED PUT OPTION\n(Claimed ROI at Strike Price)',
    xy=(time[idx_exercise], lmv[idx_exercise]), xytext=(time[idx_exercise] + 0.5, lmv[idx_exercise] - 14),
    textcoords='data', ha='center', fontsize=9, fontweight='bold', color='#88ccff',
    arrowprops=dict(arrowstyle='->', color='#88ccff', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#44aaff', alpha=0.85)
)

ax.set_title("Athletic Club: Buying Puts and Harvesting ROI",
             fontsize=15, fontweight='bold', color='white', pad=20)
ax.set_xlabel("Time", fontsize=11, color='#cccccc')
ax.set_ylabel("Loyalty Marketplace Value (LMV)", fontsize=11, color='#cccccc')
ax.set_ylim(0, strike_price + 20)
ax.legend(loc='lower left', fontsize=9, framealpha=0.6)
ax.grid(True, alpha=0.15, color='#444444')

plt.tight_layout()
plt.savefig('riskrunners/legacy/loyalty-marketplace/micro-athletic.png', dpi=150, bbox_inches='tight')
print('Saved micro-athletic.png')
