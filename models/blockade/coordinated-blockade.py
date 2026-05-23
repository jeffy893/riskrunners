import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson
import matplotlib.patches as patches

# Mesa for Agent-Based Modeling
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

# ReportLab for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

# ==========================================
# 1. ABM Component: The Coordinated Blockade Model
# ==========================================

def _grid_distance(pos1, pos2):
    """Chebyshev (Moore) distance between two grid positions."""
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

class CarAgent(Agent):
    """
    An agent representing a self-driving car.
    It moves toward the nearest city exit but can be commanded to stop.
    """
    STATE_DRIVING = 0
    STATE_ORCHESTRATED_STOP = 1
    STATE_BLOCKED_BY_TRAFFIC = 2 # Secondary effect

    def __init__(self, unique_id, model, initial_pos, final_exits):
        super().__init__(model)
        self.state = CarAgent.STATE_DRIVING
        self.final_exits = final_exits
        self.current_pos = initial_pos
        # Determine the nearest exit this car is 'assigned' to for exit flow
        self.nearest_exit = min(final_exits, key=lambda x: _grid_distance(initial_pos, x))

    def step(self):
        # 1. Check for Orchestration Command
        # If the attack is active and this agent is within the 'blocking zone' of an exit, stop.
        if self.model.attack_active:
            # Check proximity to ANY exit for blocking purposes
            dist_to_any_exit = min([_grid_distance(self.current_pos, e) for e in self.final_exits])
            if dist_to_any_exit < self.model.blocking_proximity:
                # 58% - 75% bias noted by user applied to attack susceptibility/sync likelihood
                if self.random.random() < 0.85: # High likelihood of coordinated behavior (sync attack)
                    self.state = CarAgent.STATE_ORCHESTRATED_STOP
                    return # Stop moving

        # 2. Movement Logic if still driving
        if self.state == CarAgent.STATE_DRIVING:
            # Move towards assigned nearest exit
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            
            # Simple pathfinding: move to the step closest to nearest_exit
            next_step = min(possible_steps, key=lambda x: _grid_distance(x, self.nearest_exit))
            
            # Check if cell is occupied (simulate basic traffic collision avoidance)
            if self.model.grid.is_cell_empty(next_step):
                 self.model.grid.move_agent(self, next_step)
                 self.current_pos = next_step
            else:
                 # If we are near an exit and blocked by another stopped agent, we contribute to blockade
                 dist_to_exit_blocked = min([_grid_distance(self.current_pos, e) for e in self.final_exits])
                 if dist_to_exit_blocked <= self.model.blocking_proximity + 1:
                     cell_contents = self.model.grid.get_cell_list_contents([next_step])
                     # If occupant is stopped, I am now secondary blockage
                     if len(cell_contents) > 0 and cell_contents[0].state == CarAgent.STATE_ORCHESTRATED_STOP:
                          self.state = CarAgent.STATE_BLOCKED_BY_TRAFFIC


class BlockadeModel(Model):
    """
    Model simulating the concentric city and orchestrated blockade attack.
    """
    def __init__(self, N, width, height, num_rings, attack_time, blocking_proximity=2):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.attack_time = attack_time
        self.attack_active = False
        self.blocking_proximity = blocking_proximity
        self.current_step = 0
        self.exits = []

        # 1. Define City Exits (Concentric Circles)
        center_x, center_y = width // 2, height // 2
        max_radius = min(center_x, center_y) - 2
        # Exits are defined as points on the outer ring of the grid/concentric map
        num_exits = 12 # Like a clock face
        for i in range(num_exits):
            angle = (2 * np.pi / num_exits) * i
            exit_x = int(center_x + max_radius * np.cos(angle))
            exit_y = int(center_y + max_radius * np.sin(angle))
            self.exits.append((exit_x, exit_y))
            # Also define intermediate "rings" of concentric points (for visualization, not movement exits)
            # which agents naturally cross.
            
        self.grid_visual_map = {
            "center": (center_x, center_y),
            "max_radius": max_radius,
            "num_rings": num_rings
        }

        # 2. Populate agents (dispersed randomly in the 'inner city')
        inner_radius = max_radius // 2
        for i in range(self.num_agents):
            # Generate random points within inner radius
            angle = self.random.random() * 2 * np.pi
            radius = self.random.random() * inner_radius
            
            a_x = int(center_x + radius * np.cos(angle))
            a_y = int(center_y + radius * np.sin(angle))
            
            # Place agent
            # Mesa position uses integers, we clip to grid bounds
            a_x = max(0, min(width - 1, a_x))
            a_y = max(0, min(height - 1, a_y))

            a = CarAgent(i, self, (a_x, a_y), self.exits)
            self.schedule.add(a)
            self.grid.place_agent(a, (a_x, a_y))

        # 3. Data Collection
        self.datacollector = DataCollector(
            model_reporters={
                "Orchestrated_Stops": lambda m: self.count_agents_by_state(m, CarAgent.STATE_ORCHESTRATED_STOP),
                "Secondary_Blocked": lambda m: self.count_agents_by_state(m, CarAgent.STATE_BLOCKED_BY_TRAFFIC),
                "Exits_Blockaded": lambda m: self.count_blockaded_exits(m)
            }
        )

    def count_agents_by_state(self, model, state):
        return sum([1 for a in model.schedule.agents if a.state == state])

    def count_blockaded_exits(self, model):
        """ An exit is blockaded if at least one agent is stopped within proximity. """
        count = 0
        for e in self.exits:
            neighbors = self.grid.get_neighbors(e, moore=True, include_center=True, radius=self.blocking_proximity)
            if any([a.state == CarAgent.STATE_ORCHESTRATED_STOP for a in neighbors]):
                count += 1
        return count

    def step(self):
        # Trigger attack at specific step
        if self.current_step == self.attack_time:
            self.attack_active = True
            print(f"[{time.strftime('%H:%M:%S')}] ATTACK ACTIVE: Coordinated Stoppage Initiated.")

        self.datacollector.collect(self)
        self.schedule.step()
        self.current_step += 1

# ==========================================
# 2. Simulation Execution & Visualization
# ==========================================

def run_blockade_simulation():
    # Model parameters
    N = 800 # Number of AVs in city
    WIDTH = 60
    HEIGHT = 60
    NUM_RINGS = 5
    ATTACK_STEP = 25
    MAX_STEPS = 65

    # Run Simulation
    print(f"[{time.strftime('%H:%M:%S')}] Starting Unsupervised ABM (Agent-Based Model)...")
    blockade_model = BlockadeModel(N, WIDTH, HEIGHT, NUM_RINGS, ATTACK_STEP)
    for i in range(MAX_STEPS):
        blockade_model.step()
    print(f"[{time.strftime('%H:%M:%S')}] Simulation complete. Data collected.")

    return blockade_model

def generate_dashboard_and_math(blockade_model):
    """ Generates visualization, fits mathematics over the emergent data, and combines for output. """
    print(f"[{time.strftime('%H:%M:%S')}] Fitting Mathematics ('Supervised Layer') to ABM Output...")
    
    # Extract data
    data = blockade_model.datacollector.get_model_vars_dataframe()
    data['Total_Blockage'] = data['Orchestrated_Stops'] + data['Secondary_Blocked']
    
    # --- Color Palette & Style ---
    BG_COLOR = '#1a1a2e'
    PANEL_COLOR = '#16213e'
    ACCENT_RED = '#e94560'
    ACCENT_BLUE = '#0f3460'
    ACCENT_CYAN = '#00d2d3'
    TEXT_COLOR = '#eaeaea'
    GRID_COLOR = '#2d3561'
    
    plt.rcParams.update({
        'text.color': TEXT_COLOR,
        'axes.labelcolor': TEXT_COLOR,
        'xtick.color': TEXT_COLOR,
        'ytick.color': TEXT_COLOR,
        'axes.edgecolor': GRID_COLOR,
        'figure.facecolor': BG_COLOR,
        'axes.facecolor': PANEL_COLOR,
        'font.family': 'sans-serif',
    })

    # Landscape figure
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(BG_COLOR)
    
    # Title
    fig.text(0.5, 0.96, "COORDINATED AV BLOCKADE — EMERGENCY MANAGEMENT DASHBOARD",
             fontsize=16, fontweight='bold', color=TEXT_COLOR, ha='center', va='top',
             fontfamily='monospace')
    fig.text(0.5, 0.93, "Synthetic Concentric City  |  Agent-Based Model + Queuing Theory Overlay  |  2026-05-23 08:17 MST",
             fontsize=9, color='#888888', ha='center', va='top')

    # --- 1. ABM Time Series (Top Left) ---
    ax_abm = plt.subplot2grid((2, 3), (0, 0), colspan=1)
    ax_abm.set_title("Emergent Blockage Over Time", fontsize=11, fontweight='bold', pad=10)
    ax_abm.plot(data['Orchestrated_Stops'], color=ACCENT_RED, linewidth=2, label='Primary (Orchestrated)')
    ax_abm.plot(data['Total_Blockage'], color=ACCENT_CYAN, linewidth=2, label='Total Cascade')
    ax_abm.fill_between(data.index, data['Orchestrated_Stops'], alpha=0.15, color=ACCENT_RED)
    ax_abm.fill_between(data.index, data['Total_Blockage'], alpha=0.1, color=ACCENT_CYAN)
    ax_abm.axvline(x=blockade_model.attack_time, color=ACCENT_RED, linestyle='--', alpha=0.7, label='Attack Trigger')
    ax_abm.set_ylabel("Agent Count", fontsize=9)
    ax_abm.set_xlabel("Simulation Step", fontsize=9)
    ax_abm.grid(True, alpha=0.15, color=GRID_COLOR)
    ax_abm.legend(fontsize=7, loc='upper left', framealpha=0.3)
    ax_abm.tick_params(labelsize=8)

    # --- 2. Map Visualization (Top Center) ---
    ax_map = plt.subplot2grid((2, 3), (0, 1), colspan=1)
    ax_map.set_title("City Grid — Final State", fontsize=11, fontweight='bold', pad=10)
    
    center_x, center_y = blockade_model.grid_visual_map["center"]
    max_r = blockade_model.grid_visual_map["max_radius"]
    
    # Draw Concentric Rings
    for r in np.linspace(5, max_r, blockade_model.grid_visual_map["num_rings"]):
        circle = patches.Circle((center_x, center_y), r, linewidth=0.6, edgecolor='#3d5a80', facecolor='none', linestyle='--', alpha=0.5)
        ax_map.add_patch(circle)

    # Draw Exits
    for idx, e in enumerate(blockade_model.exits):
        ax_map.plot(e[0], e[1], 's', color=ACCENT_RED, markersize=7, 
                    label='Exit Point' if idx == 0 else "")
        circle_prox = patches.Circle((e[0], e[1]), blockade_model.blocking_proximity, 
                                     linewidth=0.8, edgecolor=ACCENT_RED, facecolor=ACCENT_RED, alpha=0.08)
        ax_map.add_patch(circle_prox)

    # Plot Agents by state
    for a in blockade_model.schedule.agents:
        if a.state == CarAgent.STATE_ORCHESTRATED_STOP:
            ax_map.plot(a.pos[0], a.pos[1], 'o', color=ACCENT_RED, markersize=2.5, alpha=0.8)
        elif a.state == CarAgent.STATE_BLOCKED_BY_TRAFFIC:
            ax_map.plot(a.pos[0], a.pos[1], 'o', color='#ffa500', markersize=2, alpha=0.6)
        else:
            ax_map.plot(a.pos[0], a.pos[1], 'o', color=ACCENT_CYAN, markersize=1.2, alpha=0.25)

    ax_map.set_xlim(0, blockade_model.grid.width)
    ax_map.set_ylim(0, blockade_model.grid.height)
    ax_map.set_aspect('equal')
    ax_map.set_xticks([])
    ax_map.set_yticks([])
    ax_map.legend(loc='upper right', fontsize=7, framealpha=0.3)
    
    # --- 3. Mathematical Fitting (Top Right) ---
    ax_math = plt.subplot2grid((2, 3), (0, 2), colspan=1)
    ax_math.set_title("Poisson Fit — Exit Blockade Rate", fontsize=11, fontweight='bold', pad=10)
    
    attack_window = data.iloc[blockade_model.attack_time:]
    mean_exits_blocked = attack_window['Exits_Blockaded'].mean()
    
    ax_math.hist(attack_window['Exits_Blockaded'], bins=range(0, len(blockade_model.exits) + 1), 
                 density=True, alpha=0.5, color=ACCENT_BLUE, edgecolor='#4a6fa5', label='ABM Emergent Data')
    
    x_poisson = np.arange(0, len(blockade_model.exits) + 1)
    poisson_pd = poisson.pmf(x_poisson, mu=mean_exits_blocked)
    ax_math.plot(x_poisson, poisson_pd, 'o-', color=ACCENT_CYAN, ms=5, linewidth=2,
                 label=f'Poisson Fit (λ={mean_exits_blocked:.2f})')

    ax_math.set_xlabel("Exits Blockaded Simultaneously", fontsize=9)
    ax_math.set_ylabel("Probability", fontsize=9)
    ax_math.legend(fontsize=7, framealpha=0.3)
    ax_math.grid(True, alpha=0.15, color=GRID_COLOR)
    ax_math.tick_params(labelsize=8)

    # --- 4. Exits Blockaded Over Time (Bottom Left) ---
    ax_exits = plt.subplot2grid((2, 3), (1, 0), colspan=1)
    ax_exits.set_title("Exits Blockaded Over Time", fontsize=11, fontweight='bold', pad=10)
    ax_exits.plot(data['Exits_Blockaded'], color='#ffa500', linewidth=2)
    ax_exits.fill_between(data.index, data['Exits_Blockaded'], alpha=0.15, color='#ffa500')
    ax_exits.axhline(y=len(blockade_model.exits), color=ACCENT_RED, linestyle=':', alpha=0.5, label=f'Max Exits ({len(blockade_model.exits)})')
    ax_exits.axvline(x=blockade_model.attack_time, color=ACCENT_RED, linestyle='--', alpha=0.5)
    ax_exits.set_ylabel("Count", fontsize=9)
    ax_exits.set_xlabel("Simulation Step", fontsize=9)
    ax_exits.grid(True, alpha=0.15, color=GRID_COLOR)
    ax_exits.legend(fontsize=7, framealpha=0.3)
    ax_exits.tick_params(labelsize=8)

    # --- 5. Risk Assessment Panel (Bottom Center + Right) ---
    ax_text = plt.subplot2grid((2, 3), (1, 1), colspan=2)
    ax_text.set_facecolor(PANEL_COLOR)
    ax_text.axis('off')
    
    final_blocked_total = data['Total_Blockage'].iloc[-1]
    final_exits_blocked = data['Exits_Blockaded'].iloc[-1]
    percent_av_blocked = (final_blocked_total / blockade_model.num_agents) * 100
    percent_exits_blocked = (final_exits_blocked / len(blockade_model.exits)) * 100
    prob_all_blocked = poisson.pmf(len(blockade_model.exits), mu=mean_exits_blocked) * 100

    # Header
    ax_text.text(0.02, 0.95, "SYNTHESIS & RISK ASSESSMENT", fontsize=12, fontweight='bold',
                 color=ACCENT_CYAN, va='top', ha='left', fontfamily='monospace')
    
    # Divider line
    ax_text.axhline(y=0.88, xmin=0.02, xmax=0.98, color=GRID_COLOR, linewidth=0.8)
    
    col1_x = 0.02
    col2_x = 0.52
    
    # Left column - ABM Outcomes
    ax_text.text(col1_x, 0.82, "I. ABM EMERGENT OUTCOMES", fontsize=9, fontweight='bold',
                 color=ACCENT_RED, va='top')
    outcomes = (
        f"  Vehicles Blocked:  {final_blocked_total:.0f} / {blockade_model.num_agents}\n"
        f"  Grid Paralysis:    {percent_av_blocked:.1f}%\n"
        f"  Exits Blockaded:   {final_exits_blocked:.0f} / {len(blockade_model.exits)} ({percent_exits_blocked:.0f}%)\n"
        f"  Attack Trigger:    Step {blockade_model.attack_time}"
    )
    ax_text.text(col1_x, 0.72, outcomes, fontsize=9, color=TEXT_COLOR, va='top',
                 fontfamily='monospace', linespacing=1.6)
    
    # Left column - Math
    ax_text.text(col1_x, 0.38, "II. MATHEMATICAL FITTING", fontsize=9, fontweight='bold',
                 color=ACCENT_RED, va='top')
    math_text = (
        f"  Model:             Poisson (Queuing Theory)\n"
        f"  Arrival Rate (λ):  {mean_exits_blocked:.2f} exits/step\n"
        f"  P(Total Gridlock): {prob_all_blocked:.2f}% steady-state"
    )
    ax_text.text(col1_x, 0.28, math_text, fontsize=9, color=TEXT_COLOR, va='top',
                 fontfamily='monospace', linespacing=1.6)
    
    # Right column - Mitigation
    ax_text.text(col2_x, 0.82, "III. SOP MITIGATION RECOMMENDATIONS", fontsize=9, fontweight='bold',
                 color=ACCENT_RED, va='top')
    mitigation = (
        "  ELIMINATE: Update AV protocols to reject\n"
        "  synchronized stop commands near critical\n"
        "  infrastructure unless multi-source validated.\n\n"
        "  MINIMIZE: Deploy decentralized community\n"
        "  protocols (FCRM) to coordinate resilient\n"
        "  neighborhood logistics via alternate routes.\n\n"
        "  DETECT: Real-time anomaly detection on\n"
        "  fleet-wide velocity telemetry to flag\n"
        "  coordinated deceleration patterns."
    )
    ax_text.text(col2_x, 0.72, mitigation, fontsize=9, color=TEXT_COLOR, va='top',
                 fontfamily='monospace', linespacing=1.5)

    plt.tight_layout(rect=[0.01, 0.02, 0.99, 0.91])
    
    return fig

# ==========================================
# 4. Final Output: Generate Dashboard PDF
# ==========================================

def export_dashboard_to_pdf(fig, filename=None):
    """
    Saves the matplotlib figure to a landscape PDF using ReportLab.
    Output goes to the blockade model folder.
    """
    import os
    from reportlab.lib.pagesizes import landscape, letter
    
    if filename is None:
        # Write into the same folder as this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, "CoordinatedBlockadeReport.pdf")
    
    print(f"[{time.strftime('%H:%M:%S')}] Generating PDF Report (ReportLab)...")
    
    # Save fig to buffer at high DPI
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    img_buffer.seek(0)
    
    # Create PDF canvas in LANDSCAPE
    page_size = landscape(letter)  # 792 x 612 pts
    c = canvas.Canvas(filename, pagesize=page_size)
    page_w, page_h = page_size
    
    # Draw image filling the landscape page with small margins
    margin = 18
    image = ImageReader(img_buffer)
    img_draw_w = page_w - 2 * margin
    img_draw_h = page_h - 2 * margin
    c.drawImage(image, margin, margin, width=img_draw_w, height=img_draw_h, preserveAspectRatio=True, anchor='c')
    
    c.save()
    print(f"[{time.strftime('%H:%M:%S')}] Report successfully exported to '{filename}'.")


def export_dashboard_to_png(fig, filename=None):
    """
    Saves the matplotlib figure as a high-resolution PNG.
    Output goes to the blockade model folder.
    """
    import os
    
    if filename is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, "CoordinatedBlockadeReport.png")
    
    print(f"[{time.strftime('%H:%M:%S')}] Generating PNG Report...")
    fig.savefig(filename, format='png', dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"[{time.strftime('%H:%M:%S')}] Report successfully exported to '{filename}'.")

# ==========================================
# Main Execution
# ==========================================

if __name__ == "__main__":
    # 1. Run Unsupervised ABM
    model_data = run_blockade_simulation()
    
    # 2. Generate Supervised/Math Layer and Visual Dashboard
    fig = generate_dashboard_and_math(model_data)
    
    # 3. Export to PDF and PNG
    export_dashboard_to_pdf(fig)
    export_dashboard_to_png(fig)
    
    # plt.show() # Uncomment if running locally to see visual
    print(f"[{time.strftime('%H:%M:%S')}] Dashboard process finalized.")