import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm, norm

# 1. Define the age range (12 to 52, with 32 as the anchor point)
ages = np.linspace(12, 52, 400)
current_age = 32

# Logistic function (Standard S-Curve formula)
def logistic(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

# S-Curve parameters
k = 0.2
offset = np.log(2 + np.sqrt(3)) / k

# --- Aligning life stages to the curves based on the new associations ---

# Physical (Scope Capital): Highest deceleration at age 32
x0_physical = current_age - offset

# Career (Social Capital): Highest velocity at age 32
x0_career = current_age

# Wealth (Material Capital): Highest acceleration at age 32
x0_wealth = current_age + offset

# Generate the curves
physical_curve = logistic(ages, 100, k, x0_physical)
career_curve = logistic(ages, 100, k, x0_career)
wealth_curve = logistic(ages, 100, k, x0_wealth)

# Colors linked to Capital types: 
# Scope = Green, Social = Orange, Material = Blue
color_scope = 'green'
color_social = 'orange'
color_material = 'blue'

# 2. Plotting the dual-graph visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# --- TOP PLOT: S-Curves over Life Cycle ---
ax1.plot(ages, physical_curve, label='Physical (Scope) S-Curve', color=color_scope, lw=2.5)
ax1.plot(ages, career_curve, label='Career (Social) S-Curve', color=color_social, lw=2.5)
ax1.plot(ages, wealth_curve, label='Wealth (Material) S-Curve', color=color_material, lw=2.5)

# Mark current age
ax1.axvline(x=current_age, color='red', linestyle='--', alpha=0.6, label='Age 32 (Present)')

# Mark specific dynamic points at age 32
ax1.scatter([current_age], [logistic(current_age, 100, k, x0_physical)], color=color_scope, zorder=5, s=80)
ax1.text(current_age - 1, logistic(current_age, 100, k, x0_physical) + 3, 'Highest Deceleration\n(Physical)', ha='right', color=color_scope, weight='bold')

ax1.scatter([current_age], [logistic(current_age, 100, k, x0_career)], color=color_social, zorder=5, s=80)
ax1.text(current_age + 1, logistic(current_age, 100, k, x0_career) - 5, 'Highest Velocity\n(Career)', ha='left', color=color_social, weight='bold')

ax1.scatter([current_age], [logistic(current_age, 100, k, x0_wealth)], color=color_material, zorder=5, s=80)
ax1.text(current_age + 1, logistic(current_age, 100, k, x0_wealth) - 5, 'Highest Acceleration\n(Wealth)', ha='left', color=color_material, weight='bold')

ax1.set_title('Life Cycle S-Curves: Physical, Career, and Wealth (Ages 12 to 52)', fontsize=14)
ax1.set_xlabel('Age', fontsize=12)
ax1.set_ylabel('Development / Attainment Level (%)', fontsize=12)
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# --- BOTTOM PLOT: Capital Distributions ---
x_dist = np.linspace(-4, 4, 400)

# Scope Capital (Normally Distributed - Linked to Physical)
scope_dist = norm.pdf(x_dist, loc=0, scale=1)
ax2.plot(x_dist, scope_dist, label='Scope Capital (Normally Distributed)', color=color_scope, lw=2.5)
ax2.fill_between(x_dist, scope_dist, alpha=0.1, color=color_scope)

# Social Capital (Left Skewed - Linked to Career)
social_dist = skewnorm.pdf(x_dist, a=-5, loc=1.5, scale=1.5)
ax2.plot(x_dist, social_dist, label='Social Capital (Left Skewed)', color=color_social, lw=2.5)
ax2.fill_between(x_dist, social_dist, alpha=0.1, color=color_social)

# Material Capital (Right Skewed - Linked to Wealth)
material_dist = skewnorm.pdf(x_dist, a=5, loc=-1.5, scale=1.5)
ax2.plot(x_dist, material_dist, label='Material Capital (Right Skewed)', color=color_material, lw=2.5)
ax2.fill_between(x_dist, material_dist, alpha=0.1, color=color_material)

ax2.set_title('Conceptual Population Distributions of Capital', fontsize=14)
ax2.set_xlabel('Capital Quantity (Relative Scale)', fontsize=12)
ax2.set_ylabel('Frequency / Population Density', fontsize=12)
ax2.set_yticks([]) # Hide y-axis
ax2.set_xticks([])

# Add dunbar number note
ax2.text(2.2, np.max(social_dist)*0.8, "Near Dunbar's ~150", ha='center', color=color_social, fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig('life_capital_curves.png')