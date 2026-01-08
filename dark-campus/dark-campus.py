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