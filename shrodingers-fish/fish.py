import random
import csv

# Simulation Parameters
NUM_AGENTS = 20
NUM_TURNS = 200
INITIAL_ENERGY = 70
INITIAL_WEALTH = 10
INITIAL_KNOWLEDGE = 5
INITIAL_RESILIENCE = 3
STRESS_THRESHOLD_HIGH = 7 # Above this, performance degrades
STRESS_THRESHOLD_CRITICAL = 9 # Severe negative effects

CRITICAL_ENERGY_THRESHOLD = 20
CRITICAL_WEALTH_THRESHOLD = 5

# Playbook Actions
actions = ["work_alone", "rest", "attempt_knowledge_share", "attempt_collaboration", "seek_help", "strengthen_ties"]

class Agent:
    def __init__(self, id):
        self.id = id
        self.age = 0
        self.energy = INITIAL_ENERGY + random.randint(-10, 10)
        self.wealth = INITIAL_WEALTH + random.randint(-5, 5)
        self.knowledge = INITIAL_KNOWLEDGE + random.randint(-3, 3)
        self.stress = random.randint(1, 3)
        self.resilience = INITIAL_RESILIENCE + random.randint(-1, 1)
        self.posterity_points = 0
        self.connections = {} # {agent_id: social_capital_score}
        self.last_action = "initialized"
        self.is_in_crisis_state = "None" # None, LowEnergy, LowWealth, HighStress

    def _clamp_metrics(self):
        self.energy = max(0, min(100, self.energy))
        self.wealth = max(0, self.wealth) # No upper wealth limit for now
        self.knowledge = max(0, self.knowledge)
        self.stress = max(0, min(10, self.stress))
        self.resilience = max(0, min(10, self.resilience))

    def update_bylaws_status(self):
        self.is_in_crisis_state = "None"
        if self.energy < CRITICAL_ENERGY_THRESHOLD:
            self.stress += 2
            self.is_in_crisis_state = "LowEnergy"
        if self.wealth < CRITICAL_WEALTH_THRESHOLD:
            self.stress += 1
            self.is_in_crisis_state = "LowWealth"
        if self.stress > STRESS_THRESHOLD_CRITICAL:
            self.energy -= 5 # High stress is draining
            self.is_in_crisis_state = "HighStress"
        elif self.stress > STRESS_THRESHOLD_HIGH:
             self.is_in_crisis_state = "HighStress_Moderate"


    def choose_action(self, all_agents):
        # Simplified decision-making based on KPIs and bylaws
        self.update_bylaws_status()

        # Crisis Management
        if self.is_in_crisis_state == "LowEnergy" or self.energy < 30:
            if random.random() < 0.7: # High chance to rest
                 return "rest"
            else: # Try to seek help
                return "seek_help"
        if self.is_in_crisis_state == "LowWealth" or self.wealth < 10:
            if random.random() < 0.5:
                return "work_alone"
            elif self.connections and random.random() < 0.3:
                return "attempt_collaboration"
            else:
                return "seek_help"

        # Opportunistic actions if not in crisis
        # Prioritize actions that might lead to posterity or better social standing
        rand_choice = random.random()
        if rand_choice < 0.3: # Work for resources
            return "work_alone"
        elif rand_choice < 0.5 and self.knowledge > 10: # Share knowledge if has some
            return "attempt_knowledge_share"
        elif rand_choice < 0.7 and self.connections: # Collaborate if connected
            return "attempt_collaboration"
        elif rand_choice < 0.85: # Proactively strengthen ties
            return "strengthen_ties"
        else: # Default to rest or low-impact action
            return "rest"

    def execute_action(self, action, all_agents):
        self.last_action = action
        self.age += 1
        self.energy -= 2 # Base metabolic cost per turn

        action_efficiency_modifier = 1.0
        if self.stress > STRESS_THRESHOLD_HIGH:
            action_efficiency_modifier = 0.7 # Stress reduces efficiency
        if self.stress > STRESS_THRESHOLD_CRITICAL:
            action_efficiency_modifier = 0.4

        # --- Playbook Actions ---
        if action == "work_alone":
            wealth_gain = random.randint(3, 8) * action_efficiency_modifier
            self.wealth += wealth_gain
            self.energy -= random.randint(5, 10)
            self.stress += random.uniform(0, 0.5)

        elif action == "rest":
            energy_gain = random.randint(10, 20)
            self.energy += energy_gain
            self.stress -= random.randint(1, 3)
            if self.stress < 0: self.stress = 0
            # If resting helped overcome a crisis, small resilience boost
            if self.is_in_crisis_state != "None" and self.energy > CRITICAL_ENERGY_THRESHOLD + 10:
                self.resilience += 0.2 * action_efficiency_modifier
                self.posterity_points += 0.1 # Surviving challenges

        elif action == "attempt_knowledge_share":
            self.energy -= random.randint(5, 10)
            if self.connections and self.knowledge > 5:
                target_id = random.choice(list(self.connections.keys()))
                target_agent = next((a for a in all_agents if a.id == target_id), None)
                if target_agent:
                    if self.connections.get(target_id, 0) > 2 and random.random() < 0.7 * action_efficiency_modifier: # Higher social capital helps
                        knowledge_transferred = random.randint(1, int(self.knowledge * 0.2))
                        target_agent.knowledge += knowledge_transferred
                        self.knowledge -= int(knowledge_transferred * 0.3) # Cost of teaching
                        self.posterity_points += knowledge_transferred * 0.5
                        self.social_capital_update(target_id, 1)
                        target_agent.social_capital_update(self.id, 1)
                        target_agent.stress -= 0.5 # Gaining knowledge can be positive
                    else: # Failed attempt or refusal
                        self.stress += 0.5
                        self.social_capital_update(target_id, -0.5)

        elif action == "attempt_collaboration":
            self.energy -= random.randint(8, 15)
            if self.connections:
                target_id = random.choice(list(self.connections.keys()))
                target_agent = next((a for a in all_agents if a.id == target_id), None)
                if target_agent and target_agent.energy > CRITICAL_ENERGY_THRESHOLD + 10 and self.connections.get(target_id,0) > 1:
                    # Assume target accepts if they are not in crisis and some social capital exists
                    target_agent.energy -= random.randint(8, 15)
                    success_chance = (self.connections.get(target_id, 0) / 10.0 + self.resilience / 20.0 + target_agent.resilience / 20.0) * action_efficiency_modifier
                    if random.random() < success_chance:
                        wealth_gain_each = random.randint(10, 25)
                        knowledge_gain_each = random.randint(2, 6)
                        self.wealth += wealth_gain_each
                        target_agent.wealth += wealth_gain_each
                        self.knowledge += knowledge_gain_each
                        target_agent.knowledge += knowledge_gain_each
                        self.posterity_points += knowledge_gain_each * 0.3
                        target_agent.posterity_points += knowledge_gain_each * 0.3
                        self.social_capital_update(target_id, 2)
                        target_agent.social_capital_update(self.id, 2)
                    else: # Collaboration failed
                        self.stress += 1
                        target_agent.stress += 1
                        self.social_capital_update(target_id, -1)
                        target_agent.social_capital_update(self.id, -1)
                else: # Target refuses or is unable
                    self.stress += 0.5
                    if target_agent: self.social_capital_update(target_id, -0.5)


        elif action == "seek_help":
            self.energy -= 3 # Effort of seeking
            self.stress += 1 # Stressful situation
            if self.connections:
                # Seek from highest social capital connection
                sorted_connections = sorted(self.connections.items(), key=lambda item: item[1], reverse=True)
                if sorted_connections:
                    target_id, _ = sorted_connections[0]
                    target_agent = next((a for a in all_agents if a.id == target_id), None)
                    if target_agent and target_agent.wealth > self.wealth + 10 and target_agent.energy > self.energy + 10 and self.connections.get(target_id,0) > 3:
                        # Target helps if they are significantly better off and good social capital
                        if self.is_in_crisis_state == "LowEnergy":
                            transfer = random.randint(5,10)
                            self.energy += transfer
                            target_agent.energy -= int(transfer * 0.5) # Altruism cost
                            self.posterity_points += 1 # Being helped is key
                            self.resilience += 0.1 # Bouncing back
                        if self.is_in_crisis_state == "LowWealth":
                            transfer = random.randint(5,10)
                            self.wealth += transfer
                            target_agent.wealth -= int(transfer * 0.5)
                            self.posterity_points += 1
                            self.resilience += 0.1
                        self.social_capital_update(target_id, 1.5)
                        target_agent.social_capital_update(self.id, 0.5) # Recipient feels gratitude
                    else: # Help refused or target unable
                        self.stress += 1
                        if target_agent: self.social_capital_update(target_id, -1)

        elif action == "strengthen_ties":
            self.energy -= 3
            if self.connections:
                target_id = random.choice(list(self.connections.keys()))
                self.social_capital_update(target_id, random.uniform(0.5, 1.5))
                target_agent = next((a for a in all_agents if a.id == target_id), None)
                if target_agent:
                    target_agent.social_capital_update(self.id, random.uniform(0.1, 0.5)) # Less benefit for receiver unless active
            elif len(all_agents) > 1: # Try to form a new connection
                potential_new_connection = random.choice([a for a in all_agents if a.id != self.id and a.id not in self.connections])
                if potential_new_connection:
                    self.connections[potential_new_connection.id] = random.randint(1,3)
                    potential_new_connection.connections[self.id] = random.randint(1,3)
                    self.last_action = "formed_new_connection"


        # Basic needs and clamping
        if self.energy <= 0: # Exhaustion leading to severe stress/near collapse
            self.stress = 10
            self.energy = 1 # Barely conscious
            # Potential for agent "death" or removal could be implemented here
        self._clamp_metrics()

    def social_capital_update(self, agent_id, amount):
        if agent_id in self.connections:
            self.connections[agent_id] += amount
            self.connections[agent_id] = max(0, min(10, self.connections[agent_id])) # Clamp social capital
        #else: # Can't update if not connected - handled by strengthen_ties for new ones.

    def prune_connections(self):
        # Simple pruning: remove connections with zero or very low social capital
        to_prune = [agent_id for agent_id, sc_score in self.connections.items() if sc_score <= 0.5 and random.random() < 0.2]
        for agent_id_prune in to_prune:
            del self.connections[agent_id_prune]
            # Also need to remove from the other agent's list (simplified here, assumes mutual removal in practice)
            # For a more robust sim, the other agent should also react.
        # Randomly try to form one new connection if not too many already
        if len(self.connections) < NUM_AGENTS / 4 and random.random() < 0.1 and len(all_agents) > len(self.connections) +1 :
            available_agents = [a for a in all_agents if a.id != self.id and a.id not in self.connections]
            if available_agents:
                new_connection = random.choice(available_agents)
                self.connections[new_connection.id] = random.randint(1, 3)
                new_connection.connections[self.id] = random.randint(1, 3) # Mutual


class Simulation:
    def __init__(self):
        self.agents = [Agent(i) for i in range(NUM_AGENTS)]
        self.turn = 0
        self.data_log = []
        # Initial connections (sparse graph)
        for agent in self.agents:
            num_initial_connections = random.randint(1, 3)
            possible_partners = [p for p in self.agents if p.id != agent.id and p.id not in agent.connections]
            random.shuffle(possible_partners)
            for i in range(min(num_initial_connections, len(possible_partners))):
                partner = possible_partners[i]
                initial_sc = random.randint(2,5)
                agent.connections[partner.id] = initial_sc
                partner.connections[agent.id] = initial_sc


    def run_turn(self):
        self.turn += 1
        random.shuffle(self.agents) # Randomize agent execution order

        # Global event (stressor)
        if self.turn % 30 == 0 and random.random() < 0.3: # Periodic potential stressor
            print(f"Turn {self.turn}: Global Stress Event!")
            for agent in self.agents:
                if random.random() < 0.5 : # Affects roughly half the population
                    agent.stress += random.randint(1,3)
                    agent.energy -= random.randint(5,10)
                    agent.last_action = "hit_by_global_stressor"

        for agent in self.agents:
            chosen_action = agent.choose_action(self.agents)
            agent.execute_action(chosen_action, self.agents)

        if self.turn % 10 == 0: # Periodically prune/form connections
            for agent in self.agents:
                agent.prune_connections()

        self.log_data()

    def log_data(self):
        for agent in self.agents:
            self.data_log.append({
                "turn": self.turn,
                "agent_id": agent.id,
                "age": agent.age,
                "energy": agent.energy,
                "wealth": agent.wealth,
                "knowledge": agent.knowledge,
                "stress": agent.stress,
                "resilience": round(agent.resilience, 2),
                "num_connections": len(agent.connections),
                "avg_social_capital": round(sum(agent.connections.values()) / len(agent.connections) if agent.connections else 0, 2),
                "posterity_points": round(agent.posterity_points, 2),
                "last_action": agent.last_action,
                "crisis_state": agent.is_in_crisis_state
            })

    def run_simulation(self):
        print("Starting simulation...")
        for i in range(NUM_TURNS):
            if i % 20 == 0: print(f"Processing turn {i+1}/{NUM_TURNS}")
            self.run_turn()
        print("Simulation finished.")

    def save_to_csv(self, filename="simulation_output.csv"):
        if not self.data_log:
            print("No data to save.")
            return
        keys = self.data_log[0].keys()
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.data_log)
        print(f"Data saved to {filename}")

# --- Main Execution ---
if __name__ == "__main__":
    sim = Simulation()
    all_agents = sim.agents # For functions that need the list of all agents
    sim.run_simulation()
    sim.save_to_csv()