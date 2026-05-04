import matplotlib.pyplot as plt
import numpy as np

# Scenario: Sold a put option at a high value to a friend.
# Friend exercises it, rolling the ROI back into the community.

plt.style.use('dark_background')

time = np.linspace(0, 10, 200)
lmv_base = 20 + time * 2 + np.sin(time * 2) * 2  # Wavy general market
my_lmv = 20 + time * 4 + np.sin(time * 1.5) * 3  # Accelerated with organic feel
idx_sold = 100  # ~time=5
idx_exercise = 140  # ~time=7
my_lmv[idx_sold:] = my_lmv[idx_sold]  # Plateaus when moving away

# Post-exercise community boost
community_boost = np.copy(lmv_base)
community_boost[idx_exercise:] = lmv_base[idx_exercise:] + 8 * (1 - np.exp(-0.8 * (time[idx_exercise:] - time[idx_exercise])))

fig, ax = plt.subplots(figsize=(12, 7))

# Fill between your LMV and market to show premium
ax.fill_between(time[:idx_sold+1], lmv_base[:idx_sold+1], my_lmv[:idx_sold+1],
                alpha=0.08, color='#aa66ff', label='Loyalty Premium')

# Fill the community boost zone
ax.fill_between(time[idx_exercise:], lmv_base[idx_exercise:], community_boost[idx_exercise:],
                alpha=0.15, color='#ffaa44', label='Community ROI Rollback')

# General market line
ax.plot(time, lmv_base, linestyle='--', color='#666666', linewidth=1.5, label='General Market LMV')

# Your LMV — rise phase
ax.plot(time[:idx_sold+1], my_lmv[:idx_sold+1], color='#8866ff', linewidth=2.5, label='Your LMV Shares')
for w in [5, 3]:
    ax.plot(time[:idx_sold+1], my_lmv[:idx_sold+1], color='#8866ff', linewidth=w, alpha=0.08)

# Your LMV — plateau
ax.plot(time[idx_sold:], my_lmv[idx_sold:], color='#8866ff', linewidth=2, linestyle='--', alpha=0.5)

# Community boost line
ax.plot(time[idx_exercise:], community_boost[idx_exercise:], color='#ffaa44', linewidth=2.5, label='Community Boost')
for w in [6, 4]:
    ax.plot(time[idx_exercise:], community_boost[idx_exercise:], color='#ffaa44', linewidth=w, alpha=0.1)

# Event markers with glow
for s, a in [(500, 0.1), (300, 0.2)]:
    ax.scatter(time[idx_sold], my_lmv[idx_sold], color='#44ff88', s=s, alpha=a, zorder=4)
ax.scatter(time[idx_sold], my_lmv[idx_sold], color='#44ff88', s=120, zorder=5, marker='D', edgecolors='white', linewidths=1)

for s, a in [(500, 0.1), (300, 0.2)]:
    ax.scatter(time[idx_exercise], my_lmv[idx_exercise], color='#ffaa44', s=s, alpha=a, zorder=4)
ax.scatter(time[idx_exercise], my_lmv[idx_exercise], color='#ffaa44', s=120, zorder=5, marker='*', edgecolors='white', linewidths=1.5)

# Annotations
ax.annotate(
    'SOLD PUT OPTION\nTO FRIEND',
    xy=(time[idx_sold], my_lmv[idx_sold]), xytext=(time[idx_sold] - 2.5, my_lmv[idx_sold] + 10),
    textcoords='data', ha='center', fontsize=9, fontweight='bold', color='#88ffbb',
    arrowprops=dict(arrowstyle='->', color='#88ffbb', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#44ff88', alpha=0.85)
)

ax.annotate(
    'FRIEND EXERCISES PUT\n(High Strike Price)',
    xy=(time[idx_exercise], my_lmv[idx_exercise]), xytext=(time[idx_exercise] + 1.5, my_lmv[idx_exercise] - 18),
    textcoords='data', ha='center', fontsize=9, fontweight='bold', color='#ffcc88',
    arrowprops=dict(arrowstyle='->', color='#ffcc88', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#ffaa44', alpha=0.85)
)

ax.set_title("Spiritual Community: Selling Puts on Loyalty",
             fontsize=15, fontweight='bold', color='white', pad=20)
ax.set_xlabel("Time", fontsize=11, color='#cccccc')
ax.set_ylabel("Loyalty Marketplace Value (LMV)", fontsize=11, color='#cccccc')
ax.set_ylim(10, my_lmv[idx_sold] + 25)
ax.legend(loc='upper left', fontsize=9, framealpha=0.6)
ax.grid(True, alpha=0.15, color='#444444')

plt.tight_layout()
plt.savefig('riskrunners/legacy/loyalty-marketplace/micro-spiritual.png', dpi=150, bbox_inches='tight')
print('Saved micro-spiritual.png')
