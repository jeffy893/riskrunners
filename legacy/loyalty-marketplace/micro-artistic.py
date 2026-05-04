import matplotlib.pyplot as plt
import numpy as np

# Scenario: Borrowed trust, shorted market, market dropped due to headwinds.
# Bought back in (covered short) by becoming House Poet.

plt.style.use('dark_background')

time = np.linspace(0, 10, 200)
lmv = 50 - time * 2 + np.sin(time * 3) * 2  # Wavy downtrend

# Post-cover rally starting at ~time=8
idx_short = 20   # ~time=1
idx_cover = 160  # ~time=8
lmv_rally = lmv[idx_cover] + (time[idx_cover:] - time[idx_cover]) * 4
# Glow on rally
rally_glow = lmv_rally + np.sin(time[idx_cover:] * 5) * 1.5

fig, ax = plt.subplots(figsize=(12, 7))

# Fill the "damage zone" between short and cover
ax.fill_between(time[idx_short:idx_cover], lmv[idx_short:idx_cover], lmv[idx_short],
                alpha=0.08, color='red', label='Social Capital Bleed')

# Main downtrend line
ax.plot(time[:idx_cover+1], lmv[:idx_cover+1], color='#ff4466', linewidth=2, label='Community LMV')
for w in [5, 3]:
    ax.plot(time[:idx_cover+1], lmv[:idx_cover+1], color='#ff4466', linewidth=w, alpha=0.08)

# Rally line with glow
ax.plot(time[idx_cover:], rally_glow, color='#44ff88', linewidth=2.5, label='Post-Transaction Value Boost')
for w in [6, 4]:
    ax.plot(time[idx_cover:], rally_glow, color='#44ff88', linewidth=w, alpha=0.1)

# Event markers with glow rings
for s, a in [(500, 0.1), (300, 0.2)]:
    ax.scatter(time[idx_short], lmv[idx_short], color='#ff6666', s=s, alpha=a, zorder=4)
ax.scatter(time[idx_short], lmv[idx_short], color='#ff4444', s=100, zorder=5, edgecolors='white', linewidths=1)

for s, a in [(500, 0.1), (300, 0.2)]:
    ax.scatter(time[idx_cover], lmv[idx_cover], color='#44aaff', s=s, alpha=a, zorder=4)
ax.scatter(time[idx_cover], lmv[idx_cover], color='#44aaff', s=100, zorder=5, edgecolors='white', linewidths=1)

# Annotations — positioned to avoid overlap
ax.annotate(
    'SHORTED MARKET\n(Borrowed Trust)',
    xy=(time[idx_short], lmv[idx_short]), xytext=(2.5, lmv[idx_short] + 12),
    textcoords='data', ha='center', fontsize=9, fontweight='bold', color='#ff8888',
    arrowprops=dict(arrowstyle='->', color='#ff8888', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#ff6666', alpha=0.85)
)

ax.annotate(
    'COVERED SHORT\n(House Poet — Karma Neutral)',
    xy=(time[idx_cover], lmv[idx_cover]), xytext=(7, lmv[idx_cover] - 18),
    textcoords='data', ha='center', fontsize=9, fontweight='bold', color='#88ffcc',
    arrowprops=dict(arrowstyle='->', color='#88ffcc', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#44ff88', alpha=0.85)
)

ax.set_title("Artistic Community: Shorting Social Capital & Covering",
             fontsize=15, fontweight='bold', color='white', pad=20)
ax.set_xlabel("Time", fontsize=11, color='#cccccc')
ax.set_ylabel("Loyalty Marketplace Value (LMV)", fontsize=11, color='#cccccc')
ax.set_ylim(15, 70)
ax.legend(loc='upper right', fontsize=9, framealpha=0.6)
ax.grid(True, alpha=0.15, color='#444444')

plt.tight_layout()
plt.savefig('riskrunners/legacy/loyalty-marketplace/micro-artistic.png', dpi=150, bbox_inches='tight')
print('Saved micro-artistic.png')
