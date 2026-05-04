import matplotlib.pyplot as plt
import numpy as np

# Scenario: Hosted hackathon, bought put, left. Attempting to exercise now.

plt.style.use('dark_background')

time = np.linspace(0, 10, 200)
lmv = 15 + time * 2 + np.sin(time * 2.5) * 2  # Organic growth
idx_hack = 120  # ~time=6
lmv[idx_hack] = 45  # Spike from Hackathon
lmv[idx_hack+1:] = 45 - (time[idx_hack+1:] - time[idx_hack]) * 3 + np.sin(time[idx_hack+1:] * 4) * 1.5
strike_price = 45

fig, ax = plt.subplots(figsize=(12, 7))

# Strike price line with glow
ax.axhline(y=strike_price, color='#44ff88', linestyle=':', linewidth=1.5, alpha=0.6, label='Strike Price')
ax.fill_between(time, strike_price - 0.5, strike_price + 0.5, color='#44ff88', alpha=0.05)

# Fill the drop zone
ax.fill_between(time[idx_hack:], lmv[idx_hack:], strike_price,
                where=lmv[idx_hack:] < strike_price,
                alpha=0.12, color='#ff4444', label='Absence Decay')

# Pre-hackathon growth
ax.plot(time[:idx_hack+1], lmv[:idx_hack+1], color='#44ddcc', linewidth=2.5, label='Your LMV')
for w in [5, 3]:
    ax.plot(time[:idx_hack+1], lmv[:idx_hack+1], color='#44ddcc', linewidth=w, alpha=0.08)

# Post-hackathon decline
ax.plot(time[idx_hack:], lmv[idx_hack:], color='#ff6688', linewidth=2, label='Post-Departure Drop')
for w in [5, 3]:
    ax.plot(time[idx_hack:], lmv[idx_hack:], color='#ff6688', linewidth=w, alpha=0.08)

# Hackathon spike marker with glow
for s, a in [(600, 0.1), (400, 0.15), (200, 0.25)]:
    ax.scatter(time[idx_hack], 45, color='#44ff88', s=s, alpha=a, zorder=4)
ax.scatter(time[idx_hack], 45, color='#44ff88', s=120, zorder=5, marker='D', edgecolors='white', linewidths=1)

# Pending exercise marker — pulsing red
idx_pending = -1
for s, a in [(600, 0.1), (400, 0.15), (200, 0.25)]:
    ax.scatter(time[idx_pending], lmv[idx_pending], color='#ff4444', s=s, alpha=a, zorder=4)
ax.scatter(time[idx_pending], lmv[idx_pending], color='#ffcc00', s=100, zorder=5, marker='*', edgecolors='#ff4444', linewidths=1.5)

# Annotations
ax.annotate(
    'HOSTED HACKATHON\n(Bought Put Option)',
    xy=(time[idx_hack], 45), xytext=(time[idx_hack] - 2.5, 55),
    textcoords='data', ha='center', fontsize=9, fontweight='bold', color='#88ffbb',
    arrowprops=dict(arrowstyle='->', color='#88ffbb', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#44ff88', alpha=0.85)
)

ax.annotate(
    'PENDING EXERCISE\n(Book Event)',
    xy=(time[idx_pending], lmv[idx_pending]), xytext=(time[idx_pending] - 2, lmv[idx_pending] + 15),
    textcoords='data', ha='center', fontsize=9, fontweight='bold', color='#ffcc00',
    arrowprops=dict(arrowstyle='->', color='#ffcc00', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#ff6644', alpha=0.85)
)

ax.set_title("Business Network: The Pending Put Exercise",
             fontsize=15, fontweight='bold', color='white', pad=20)
ax.set_xlabel("Time", fontsize=11, color='#cccccc')
ax.set_ylabel("Loyalty Marketplace Value (LMV)", fontsize=11, color='#cccccc')
ax.set_ylim(5, 65)
ax.legend(loc='upper left', fontsize=9, framealpha=0.6)
ax.grid(True, alpha=0.15, color='#444444')

plt.tight_layout()
plt.savefig('riskrunners/legacy/loyalty-marketplace/micro-business.png', dpi=150, bbox_inches='tight')
print('Saved micro-business.png')
