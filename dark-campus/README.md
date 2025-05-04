### 2025-05-03
# Dark Campus

## Metpahor:

```sql
the city lights drown out the stars

so it makes it tough to see the stars that don't shine bright

not only that, we may see the same stars, but not connect the stars into the same constellations



a dark city in Colorado self-imposes bylaws

such that the lights are not allowed to be above a certain lumen

and the lights have to be aimed downward

it makes it tough for businesses to put up signage with lights
```

### Gemini-Generated (Prompt Engineering)

Okay, that's a fantastic metaphor for framing the challenges of achieving collective goals in diverse groups, especially where existing structures or loud narratives dominate. Let's break it down and see where it points us next in our conversation about agent-based modeling:

* **"City lights drown out the stars..."**: This perfectly captures how dominant factors (existing power structures, loud narratives, short-term incentives – the "micro hegemony" perhaps) can obscure the visibility and perceived importance of other elements (quieter voices, diverse needs, long-term goals – the "heterogenous pride").
* **"...tough to see stars that don't shine bright..."**: Emphasizes that the least powerful or least obvious perspectives/needs are the most likely to be overlooked.
* **"...see the same stars, but not connect the stars into the same constellations."**: This is key. Even if people perceive the same basic facts or agents, they interpret the relationships, patterns, and priorities differently. There's a lack of shared understanding or a shared "map" leading towards the "vertical objective."
* **"Dark city... self-imposes bylaws..."**: This represents the desired outcome – a community recognizing the problem ("light pollution" / obscured stars / lack of shared vision) and collectively agreeing on rules (the "bylaws") to mitigate it, enabling the collective goal (seeing the stars / achieving the vertical objective). This directly links to your interest in self-imposed rules and norms.
* **"...tough for business to put up signage..."**: This highlights the inherent trade-offs. Implementing rules for the collective good often imposes costs or constraints on individuals or sub-groups, creating tension that needs to be managed.

Based on this metaphor and our previous discussion, here are some potential next steps for our conversation, focusing on how Agent-Based Modeling (ABM) with NetLogo can help explore these dynamics:

1.  **Focusing on Visibility (Seeing Dim Stars):**
    * **How ABM Helps:** We can explicitly model agent heterogeneity not just in simple terms (like strategy or wealth) but in terms of influence, communication frequency, access to information, or vulnerability to negative outcomes.
    * **Next Step:** We could select a model (perhaps `Cooperation` or `Rebellion`) and discuss *specific ways* to add agent attributes that represent "dim stars" (e.g., lower initial resources, less network connectivity, higher susceptibility to negative consequences) and see how their presence affects the overall system dynamics and the success of collective goals.

2.  **Focusing on Interpretation (Connecting Constellations):**
    * **How ABM Helps:** We can model how agents perceive their environment and each other differently. This could involve agents having incomplete information, different internal models for decision-making, or being influenced differently by neighbors or media analogues.
    * **Next Step:** We could discuss incorporating mechanisms for social influence, information diffusion (maybe drawing from `Rumor Mill`), or even basic cognitive biases into agents within a model like `Ethnocentrism` or a `PD` variant. How do different ways agents "connect the stars" affect group cohesion and goal alignment?

3.  **Focusing on Rule/Norm Emergence (The Dark Sky Bylaw Process):**
    * **How ABM Helps:** We can simulate the *process* by which rules might emerge or be adopted. This could involve agents "voting," learning successful strategies from others, sanctioning those who break proto-rules, or adapting rules based on collective outcomes.
    * **Next Step:** We could explore how to implement rule-making dynamics in a model. For instance, in the `Cooperation` model, could agents vote on a "conservation threshold"? Could agents in `PD` models develop punishment strategies for defectors (like in the Norms/Metanorms community models)? This directly addresses simulating "self-imposing bylaws."

4.  **Focusing on Trade-offs (The Business Signage Problem):**
    * **How ABM Helps:** We can explicitly model the costs and benefits associated with certain actions or rules, and importantly, how these costs/benefits are distributed across different types of agents.
    * **Next Step:** We could take a model involving resource use or collective action (like `Recycling` or `Cooperation`) and discuss how to assign different costs/benefits to adhering to a potential "bylaw" (e.g., "recyclers" gain long-term benefits but incur short-term costs, while "wastefuls" might face penalties if a bylaw is enforced). We can then track the impact on different agent populations.



### APplication to NIL

Okay, this is a fascinating and socially relevant application of the metaphor! Let's translate the "Commons Pollution Model" into this "NIL Attention Saturation" scenario on campus.

**Scenario: NIL Attention Saturation & Overlooked Needs**

* **Goal:** Model how the rise of NIL and promotional efforts (especially by high-visibility groups like Athletes) creates "attention pollution" on campus, making it harder for less visible groups with important needs (like Mathletes needing wellness support) to get noticed and receive resources/support. We'll explore how a hypothetical "bylaw" (a rule promoting fairness or redirecting attention) impacts this dynamic.

* **Agents:** `StudentGroup` instances representing different campus groups.
    * Types: 'Athlete', 'Mathlete', 'DramaClub', 'DebateTeam', etc.
* **Activity/Goal:** Engage in `promotional_effort` (posting, events, NIL deals) to gain "Attention" (representing recognition, social capital, funding, NIL value).
* **Negative Externality:** High total promotional effort across campus leads to "Attention Saturation," reducing the effectiveness of everyone's efforts and making it especially hard for specific, important needs of less visible groups to be seen and met.
* **Heterogeneity:**
    * `group_type`: Categorical (Athlete, Mathlete...).
    * `inherent_visibility`: Base level of attention the group gets regardless of effort (e.g., Athletes high, Mathletes low).
    * `promotional_effectiveness`: How well their effort translates to potential attention.
    * `resource_need_level`: An indicator (e.g., 0-1) representing how much the group relies on campus attention/resources for a critical need (high for Mathletes' wellness initiative, perhaps lower for a well-funded group).
* **The "Bylaw" (Introduced mid-simulation):** Let's model a "Fairness Policy" or "Spotlight Sharing" rule.
    * **Mechanism:** Groups whose generated attention (`inherent_visibility + promotional_effort * effectiveness`) exceeds a certain `threshold` must contribute a percentage (`tax_rate`) of their generated attention/resources. This "taxed" attention/resource is then redistributed to support the explicitly defined needs of groups with high `resource_need_level` but low `inherent_visibility`.
* **The Trade-off:**
    * High-visibility/high-effort groups (likely Athletes) face a direct cost – a portion of their earned attention/resources is redirected.
    * Low-visibility/high-need groups (like Mathletes) potentially receive a direct benefit – increased chance their needs are met.
    * The overall "campus health" (measured by the proportion of critical needs being met) might improve, even if total promotional "noise" doesn't decrease.

**Python Code Outline (Conceptual):**

We'll use `pandas` for easy data handling and CSV output.

```python
import random
import pandas as pd
import math

# --- Parameters ---
NUM_AGENTS_PER_TYPE = {'Athlete': 20, 'Mathlete': 15, 'DramaClub': 10, 'DebateTeam': 10}
TOTAL_AGENTS = sum(NUM_AGENTS_PER_TYPE.values())
SIMULATION_STEPS = 100
BYLAW_START_TIME = 50
BYLAW_ATTENTION_THRESHOLD = 0.7 # Attention level above which bylaw applies
BYLAW_TAX_RATE = 0.15 # Percentage of attention/resource redirected
# --- NEW: Parameter for fixed probability boost for eligible agents ---
BYLAW_NEED_MET_PROBABILITY_BOOST = 0.15 # Add this probability if eligible and bylaw active
BYLAW_ELIGIBILITY_NEED_THRESHOLD = 0.5 # Need level required to potentially receive benefit

# Parameters controlling attention saturation
SATURATION_MIDPOINT = TOTAL_AGENTS * 0.6
SATURATION_STEEPNESS = 0.1
# --- NEW: Option to print debug info ---
DEBUG_PRINT = False

# --- Agent Definition ---
class StudentGroup:
    def __init__(self, agent_id, group_type, visibility, need, effectiveness):
        self.id = agent_id
        self.group_type = group_type
        self.inherent_visibility = visibility
        self.resource_need_level = need
        self.promotional_effectiveness = effectiveness

        self.promotional_effort = random.uniform(0.1, 1.0)
        self.potential_attention = 0
        self.actual_attention_received = 0
        self.need_met_probability = 0 # This will store the FINAL probability for logging
        self.need_met_this_step = False
        self.bylaw_cost = 0
        self.bylaw_benefit_received_flag = False # Flag if they received *any* benefit boost
        self.satisfaction = 0.5

    def update_effort(self, saturation):
        reduction_factor = max(0, 1 - saturation * 0.5)
        self.promotional_effort = max(0.1, self.promotional_effort * reduction_factor * random.uniform(0.95, 1.05))

    def calculate_potential_attention(self):
        self.potential_attention = self.inherent_visibility + self.promotional_effort * self.promotional_effectiveness
        self.potential_attention = min(1.0, self.potential_attention)

    def apply_saturation_and_bylaw_cost(self, saturation, bylaw_active):
        # Reset cost for the step
        self.bylaw_cost = 0
        attention_after_saturation = self.potential_attention * (1 - saturation)
        taxed_attention = 0

        if bylaw_active and self.potential_attention > BYLAW_ATTENTION_THRESHOLD:
            taxed_attention = attention_after_saturation * BYLAW_TAX_RATE
            self.bylaw_cost = taxed_attention
            attention_after_saturation -= taxed_attention

        self.actual_attention_received = max(0, attention_after_saturation)
        return taxed_attention # Return amount contributed to pool

    def determine_need_met(self, saturation, bylaw_active, bylaw_benefit_applicable):
        # Reset benefit flag and outcome
        self.bylaw_benefit_received_flag = False
        self.need_met_this_step = False

        # Calculate base probability (Removed * 0.8 scaling)
        base_prob_need_met = self.actual_attention_received * (1 - saturation)
        final_prob = base_prob_need_met

        # Apply fixed benefit boost if applicable
        if bylaw_active and bylaw_benefit_applicable and self.resource_need_level >= BYLAW_ELIGIBILITY_NEED_THRESHOLD:
             final_prob += BYLAW_NEED_MET_PROBABILITY_BOOST
             self.bylaw_benefit_received_flag = True # Mark that benefit was applied

        # Ensure probability is valid (0 to 1) and store it
        self.need_met_probability = max(0, min(1.0, final_prob))

        # Determine outcome based on final probability
        if random.random() < self.need_met_probability:
            self.need_met_this_step = True

    def update_satisfaction(self):
        # Satisfaction increases with attention and if need is met, decreases otherwise
        # Made penalty for unmet need harsher if need level is high
        need_met_impact = 0
        if self.need_met_this_step:
            need_met_impact = 0.2
        elif self.resource_need_level > 0.5: # Penalty only if need was high and unmet
             need_met_impact = -0.2 * self.resource_need_level # Larger penalty for higher need

        target_satisfaction = 0.1 + (self.actual_attention_received * 0.7) + need_met_impact
        self.satisfaction += (target_satisfaction - self.satisfaction) * 0.1
        self.satisfaction = max(0, min(1, self.satisfaction))

# --- Simulation Model ---
class CampusModel:
    def __init__(self):
        self.agents = []
        agent_id_counter = 0
        # ... (agent creation loop remains the same as before) ...
        for group_type, count in NUM_AGENTS_PER_TYPE.items():
            for _ in range(count):
                # Define characteristics per group type (customize these)
                if group_type == 'Athlete':
                    visibility = random.uniform(0.5, 0.8)
                    need = random.uniform(0.1, 0.4)
                    effectiveness = random.uniform(0.6, 0.9)
                elif group_type == 'Mathlete':
                    visibility = random.uniform(0.05, 0.2)
                    need = random.uniform(0.7, 1.0) # High need for wellness support
                    effectiveness = random.uniform(0.3, 0.6)
                elif group_type == 'DramaClub':
                    visibility = random.uniform(0.2, 0.4)
                    need = random.uniform(0.4, 0.7)
                    effectiveness = random.uniform(0.5, 0.8)
                else: # DebateTeam etc.
                    visibility = random.uniform(0.1, 0.3)
                    need = random.uniform(0.3, 0.6)
                    effectiveness = random.uniform(0.4, 0.7)

                self.agents.append(StudentGroup(agent_id_counter, group_type, visibility, need, effectiveness))
                agent_id_counter += 1


        self.time_step = 0
        self.current_attention_saturation = 0
        self.bylaw_active = False
        self.simulation_data = []

    def calculate_saturation(self):
        total_potential_demand = sum(agent.potential_attention for agent in self.agents)
        saturation_raw = 1 / (1 + math.exp(-SATURATION_STEEPNESS * (total_potential_demand - SATURATION_MIDPOINT)))
        self.current_attention_saturation = saturation_raw


    def step(self):
        self.bylaw_active = self.time_step >= BYLAW_START_TIME

        # Agents update effort
        for agent in self.agents:
            agent.update_effort(self.current_attention_saturation)

        # Agents calculate potential attention
        for agent in self.agents:
            agent.calculate_potential_attention()

        # Calculate saturation
        self.calculate_saturation()

        # Apply saturation, calculate bylaw costs and pool
        total_taxed_pool = 0
        for agent in self.agents:
            total_taxed_pool += agent.apply_saturation_and_bylaw_cost(
                self.current_attention_saturation, self.bylaw_active
            )

        # Determine if benefit is applicable (is pool > 0?)
        bylaw_benefit_applicable_this_step = self.bylaw_active and total_taxed_pool > 0.01 # Check if pool is non-negligible

        if DEBUG_PRINT and self.bylaw_active:
             print(f"Step {self.time_step}: Bylaw Active. Total Taxed Pool: {total_taxed_pool:.2f}, Benefit Applicable: {bylaw_benefit_applicable_this_step}")

        # Agents determine if needs met (applying fixed boost if applicable)
        for agent in self.agents:
            agent.determine_need_met(
                self.current_attention_saturation,
                self.bylaw_active,
                bylaw_benefit_applicable_this_step # Pass simple flag
            )

        # Agents update satisfaction
        for agent in self.agents:
            agent.update_satisfaction()

        # Log data
        self.log_step_data(total_taxed_pool) # Pass pool size for logging if needed

        self.time_step += 1

    def log_step_data(self, total_taxed_pool): # Added pool logging capability
        total_needs_met = sum(1 for agent in self.agents if agent.need_met_this_step)
        total_critical_needs = sum(1 for agent in self.agents if agent.resource_need_level >= BYLAW_ELIGIBILITY_NEED_THRESHOLD)
        needs_met_ratio = total_needs_met / total_critical_needs if total_critical_needs > 0 else 0

        for agent in self.agents:
            self.simulation_data.append({
                'Time_Step': self.time_step,
                'Agent_ID': agent.id,
                'Group_Type': agent.group_type,
                'Inherent_Visibility': agent.inherent_visibility,
                'Resource_Need_Level': agent.resource_need_level,
                'Promotional_Effort': agent.promotional_effort,
                'Potential_Attention': agent.potential_attention,
                'Actual_Attention_Received': agent.actual_attention_received,
                # --- Log the final probability ---
                'Need_Met_Probability': agent.need_met_probability,
                'Need_Met_This_Step': agent.need_met_this_step,
                'Bylaw_Cost_Incurred': agent.bylaw_cost,
                # --- Log benefit flag instead of value ---
                'Bylaw_Benefit_Received_Flag': agent.bylaw_benefit_received_flag,
                'Agent_Satisfaction': agent.satisfaction,
                'Overall_Attention_Saturation': self.current_attention_saturation,
                'Bylaw_Active': self.bylaw_active,
                'Total_Needs_Met_Ratio': needs_met_ratio,
                'Bylaw_Pool_Size': total_taxed_pool # Log the pool size this step
            })

    def run_simulation(self):
        # ... (run loop remains the same) ...
        print("Starting Simulation...")
        for i in range(SIMULATION_STEPS):
            self.step()
            if (i + 1) % 10 == 0:
                print(f"  Completed step {i+1}/{SIMULATION_STEPS}")
        print("Simulation Complete.")
        return pd.DataFrame(self.simulation_data)


# --- Main Execution ---
if __name__ == "__main__":
    model = CampusModel()
    simulation_results_df = model.run_simulation()

    output_filename = "campus_attention_model_output_v2.csv"
    simulation_results_df.to_csv(output_filename, index=False)
    print(f"Simulation data saved to {output_filename}")

    # Display basic summary info (optional)
    print("\nSample Output Data (first 5 rows):")
    print(simulation_results_df.head())
    print("\nFinal Step Summary Stats (Mathletes vs Athletes):")
    final_step_data = simulation_results_df[simulation_results_df['Time_Step'] == SIMULATION_STEPS - 1]
    groups_of_interest = ['Athlete', 'Mathlete']
    print(final_step_data[final_step_data['Group_Type'].isin(groups_of_interest)].groupby('Group_Type')[
        ['Actual_Attention_Received', 'Need_Met_Probability', 'Need_Met_This_Step', 'Bylaw_Cost_Incurred', 'Bylaw_Benefit_Received_Flag', 'Agent_Satisfaction']
    ].mean())
    print(f"\nFinal Needs Met Ratio: {final_step_data['Total_Needs_Met_Ratio'].iloc[0]:.2f}")

```

**Explanation and How it Addresses Your Desires:**

1.  **Metaphor Mapping:** Agents are `StudentGroup`s (Athletes, Mathletes, etc.). Activity is `promotional_effort`. "Pollution" is `Overall_Attention_Saturation`. The "cost" of pollution is implicitly modeled by the reduced probability (`need_met_probability`) that critical needs (`resource_need_level`) are met, especially for low-visibility groups when saturation is high.
2.  **NIL Analogy:** High `inherent_visibility` and `promotional_effectiveness` for 'Athletes' models their advantage in the NIL era. Their high `potential_attention` contributes significantly to saturation.
3.  **Drowning Out Stars:** The `(1 - saturation)` term reduces `actual_attention_received` for everyone. The `need_met_probability` calculation specifically links attention and saturation to the chance of addressing needs – high saturation directly "drowns out" the chance for needs to be met, hitting low-visibility groups hardest.
4.  **Mathletes' Needs:** 'Mathletes' are modeled with low visibility but high `resource_need_level`. The simulation tracks if their needs are met (`Need_Met_This_Step`).
5.  **Bylaw & Trade-off:** The "Fairness Policy" kicks in at `BYLAW_START_TIME`. High-attention groups pay a "tax" (`bylaw_cost`). This pool is redistributed (`bylaw_benefit`) specifically to boost the `need_met_probability` for high-need groups like Mathletes. This explicitly models the trade-off.
6.  **Python & CSV Output:** The code defines classes and a simulation loop in Python. It uses `pandas` to collect data at each step into a structured format and saves it as a CSV file (`campus_attention_model_output.csv`), ready for Tableau.
7.  **Tableau Analysis:** The CSV contains metrics over time for each agent: their type, effort, attention gained, costs/benefits from the bylaw, whether their needs were met, and overall saturation. This allows you to visualize:
    * How attention saturation builds over time.
    * The distribution of attention among different group types.
    * The impact of the bylaw: showing the drop in attention/rise in cost for Athletes vs. the rise in benefit/needs-met chance for Mathletes.
    * Comparing the overall "campus health" (e.g., `Total_Needs_Met_Ratio`) before and after the bylaw.

You can run this Python script, generate the CSV, and then load it into Tableau to create visualizations exploring these trade-offs and the effectiveness of the hypothetical "bylaw." Remember to adjust the parameters at the top (`NUM_AGENTS_PER_TYPE`, `BYLAW_*` settings, `SATURATION_*` settings, etc.) to explore different scenarios.