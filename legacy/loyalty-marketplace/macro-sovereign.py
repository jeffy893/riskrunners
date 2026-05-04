import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Scenario: Israel exercises a put option on US loyalty.
# World market watches the US honor the high strike price.

plt.style.use('dark_background')

time = np.linspace(0, 10, 200)
global_baseline = 40 - time + np.sin(time * 2) * 3  # Wavy global deflation
us_isr_loyalty = np.full(200, 80)  # High historical strike price

# Post-exercise divergence — loyalty spikes then settles
post_exercise = np.copy(us_isr_loyalty)
idx_event = 140  # ~time=7
post_exercise[idx_event:] = 80 + 15 * np.exp(-0.5 * (time[idx_event:] - time[idx_event]))

fig, ax = plt.subplots(figsize=(12, 7))

# Gradient fill between the two lines to show the "loyalty gap"
ax.fill_between(time, global_baseline, us_isr_loyalty, alpha=0.08, color='cyan', label='Loyalty Gap')

# Main lines
ax.plot(time, global_baseline, label="Global Solidarity Index", linestyle="--", color="#888888", linewidth=1.5)
ax.plot(time, us_isr_loyalty, label="Historical LMV Strike Price", color="#4488ff", alpha=0.6, linewidth=2)
ax.plot(time[idx_event:], post_exercise[idx_event:], color='#ff4444', linewidth=2.5, label="Post-Exercise Spike")

# Glow effect on the spike
for w in [6, 4, 2]:
    ax.plot(time[idx_event:], post_exercise[idx_event:], color='#ff4444', linewidth=w, alpha=0.1)

# Event marker with glow
for s, a in [(600, 0.1), (400, 0.15), (200, 0.3)]:
    ax.scatter(7, 80, color='#ff6600', zorder=4, s=s, alpha=a)
ax.scatter(7, 80, color='#ffcc00', zorder=5, s=120, marker='*', edgecolors='#ff6600', linewidths=1.5)

# Annotation — pushed well below the strike line so it's not scrunched
ax.annotate(
    'SOVEREIGN PUT EXERCISED\n(High Esteem Transaction)',
    xy=(7, 80), xytext=(7, 55),
    textcoords='data',
    ha='center', fontsize=10, fontweight='bold', color='#ffcc00',
    arrowprops=dict(arrowstyle='->', color='#ffcc00', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.4', fc='#222222', ec='#ffcc00', alpha=0.85)
)

# Title and labels
ax.set_title("Macro Geopolitics: Exercising the Sovereign Put",
             fontsize=15, fontweight='bold', color='white', pad=20)
ax.set_xlabel("Time", fontsize=11, color='#cccccc')
ax.set_ylabel("Loyalty Marketplace Value (LMV)", fontsize=11, color='#cccccc')
ax.set_ylim(15, 105)
ax.legend(loc='lower left', fontsize=9, framealpha=0.6)
ax.grid(True, alpha=0.15, color='#444444')

plt.tight_layout()
plt.savefig('riskrunners/legacy/loyalty-marketplace/macro-sovereign.png', dpi=150, bbox_inches='tight')
print('Saved macro-sovereign.png')
