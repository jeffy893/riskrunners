#!/usr/bin/env python3
"""
Humanitarian Gambit Simulation
A Game Theory Model of the "Priority Swap" Mechanism

This simulation models the strategic interactions between countries
when humanitarian burden-sharing affects debt priority structures.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from typing import List, Tuple, Dict
import pandas as pd

@dataclass
class Country:
    """Represents a country in the humanitarian gambit scenario"""
    name: str
    debt_amount: float
    priority: int
    refugee_capacity: float = 0
    humanitarian_cost_per_refugee: float = 25000

@dataclass
class GameState:
    """Represents the current state of the game"""
    resource_value: float
    refugee_population: int
    countries: List[Country]
    court_active: bool = True

class HumanitarianGambitSimulation:
    """Main simulation class for the humanitarian gambit game theory model"""
    
    def __init__(self):
        self.results = []
        self.scenarios = []
        
    def create_base_scenario(self) -> GameState:
        """Create the base Lithium Gambit scenario"""
        countries = [
            Country("EastBloc (B1)", 6_000_000_000, 1),  # Senior creditor
            Country("WestFed (A1)", 5_000_000_000, 2),   # Junior creditor
        ]
        
        return GameState(
            resource_value=10_000_000_000,  # $10B Lithium reserves
            refugee_population=100_000,
            countries=countries
        )
    
    def calculate_payouts_status_quo(self, state: GameState) -> Dict[str, float]:
        """Calculate payouts under traditional debt priority"""
        payouts = {}
        remaining_value = state.resource_value
        
        # Sort by priority (lower number = higher priority)
        sorted_countries = sorted(state.countries, key=lambda c: c.priority)
        
        for country in sorted_countries:
            payout = min(country.debt_amount, remaining_value)
            payouts[country.name] = payout
            remaining_value -= payout
            
        return payouts
    
    def calculate_payouts_priority_swap(self, state: GameState, accepting_country: str) -> Dict[str, float]:
        """Calculate payouts when a country accepts refugees and gains priority"""
        payouts = {}
        remaining_value = state.resource_value
        
        # Find the accepting country and calculate refugee costs
        refugee_cost = 0
        accepting_debt = 0
        
        for country in state.countries:
            if country.name == accepting_country:
                refugee_cost = state.refugee_population * country.humanitarian_cost_per_refugee
                accepting_debt = country.debt_amount
                break
        
        # Accepting country gets first priority
        payouts[accepting_country] = min(accepting_debt, remaining_value)
        remaining_value -= payouts[accepting_country]
        
        # Other countries get remaining value by original priority
        other_countries = [c for c in state.countries if c.name != accepting_country]
        other_countries.sort(key=lambda c: c.priority)
        
        for country in other_countries:
            payout = min(country.debt_amount, remaining_value)
            payouts[country.name] = payout
            remaining_value -= payout
        
        # Subtract refugee costs from accepting country's net gain
        payouts[f"{accepting_country}_net"] = payouts[accepting_country] - refugee_cost
        payouts[f"{accepting_country}_refugee_cost"] = refugee_cost
        
        return payouts
    
    def run_scenario_analysis(self) -> pd.DataFrame:
        """Run comprehensive scenario analysis"""
        base_state = self.create_base_scenario()
        
        scenarios = []
        
        # Scenario 1: Status Quo
        status_quo_payouts = self.calculate_payouts_status_quo(base_state)
        scenarios.append({
            'Scenario': 'Status Quo',
            'EastBloc_Payout': status_quo_payouts.get('EastBloc (B1)', 0),
            'WestFed_Payout': status_quo_payouts.get('WestFed (A1)', 0),
            'WestFed_Net': status_quo_payouts.get('WestFed (A1)', 0) - 5_000_000_000,
            'Refugee_Cost': 0,
            'WestFed_Decision': 'Reject Refugees'
        })
        
        # Scenario 2: Priority Swap (WestFed accepts refugees)
        priority_swap_payouts = self.calculate_payouts_priority_swap(base_state, 'WestFed (A1)')
        scenarios.append({
            'Scenario': 'Priority Swap',
            'EastBloc_Payout': priority_swap_payouts.get('EastBloc (B1)', 0),
            'WestFed_Payout': priority_swap_payouts.get('WestFed (A1)', 0),
            'WestFed_Net': priority_swap_payouts.get('WestFed (A1)_net', 0) - 5_000_000_000,
            'Refugee_Cost': priority_swap_payouts.get('WestFed (A1)_refugee_cost', 0),
            'WestFed_Decision': 'Accept Refugees'
        })
        
        return pd.DataFrame(scenarios)
    
    def sensitivity_analysis(self) -> pd.DataFrame:
        """Analyze sensitivity to refugee costs and resource values"""
        base_state = self.create_base_scenario()
        
        refugee_costs = np.linspace(10000, 50000, 20)  # Cost per refugee
        resource_values = np.linspace(8_000_000_000, 15_000_000_000, 20)  # Resource value
        
        results = []
        
        for refugee_cost in refugee_costs:
            for resource_value in resource_values:
                # Update state
                test_state = GameState(
                    resource_value=resource_value,
                    refugee_population=base_state.refugee_population,
                    countries=[
                        Country("EastBloc (B1)", 6_000_000_000, 1),
                        Country("WestFed (A1)", 5_000_000_000, 2, 
                               humanitarian_cost_per_refugee=refugee_cost)
                    ]
                )
                
                # Calculate outcomes
                status_quo = self.calculate_payouts_status_quo(test_state)
                priority_swap = self.calculate_payouts_priority_swap(test_state, 'WestFed (A1)')
                
                # Status quo net: what WestFed gets minus what they're owed
                westfed_status_quo_net = status_quo.get('WestFed (A1)', 0) - 5_000_000_000
                
                # Priority swap net: payout minus refugee cost minus what they're owed
                westfed_priority_swap_payout = priority_swap.get('WestFed (A1)', 0)
                westfed_refugee_cost = priority_swap.get('WestFed (A1)_refugee_cost', 0)
                westfed_priority_swap_net = westfed_priority_swap_payout - westfed_refugee_cost - 5_000_000_000
                
                results.append({
                    'Refugee_Cost_Per_Person': refugee_cost,
                    'Resource_Value': resource_value,
                    'WestFed_Prefers_Refugees': westfed_priority_swap_net > westfed_status_quo_net,
                    'Status_Quo_Net': westfed_status_quo_net,
                    'Priority_Swap_Net': westfed_priority_swap_net,
                    'Net_Benefit_of_Accepting': westfed_priority_swap_net - westfed_status_quo_net
                })
        
        return pd.DataFrame(results)
    
    def create_visualizations(self):
        """Create comprehensive visualizations of the simulation results"""
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Scenario Comparison
        ax1 = plt.subplot(2, 3, 1)
        scenario_df = self.run_scenario_analysis()
        
        scenarios = scenario_df['Scenario']
        eastbloc_payouts = scenario_df['EastBloc_Payout'] / 1e9
        westfed_payouts = scenario_df['WestFed_Payout'] / 1e9
        
        x = np.arange(len(scenarios))
        width = 0.35
        
        ax1.bar(x - width/2, eastbloc_payouts, width, label='EastBloc (B1)', color='#d62728')
        ax1.bar(x + width/2, westfed_payouts, width, label='WestFed (A1)', color='#2ca02c')
        
        ax1.set_xlabel('Scenario')
        ax1.set_ylabel('Payout (Billions USD)')
        ax1.set_title('Debt Repayment by Scenario')
        ax1.set_xticks(x)
        ax1.set_xticklabels(scenarios)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Net Benefit Analysis
        ax2 = plt.subplot(2, 3, 2)
        westfed_net = scenario_df['WestFed_Net'] / 1e9
        refugee_costs = scenario_df['Refugee_Cost'] / 1e9
        
        colors = ['red' if x < 0 else 'green' for x in westfed_net]
        bars = ax2.bar(scenarios, westfed_net, color=colors, alpha=0.7)
        
        # Add refugee cost annotation
        for i, (bar, cost) in enumerate(zip(bars, refugee_costs)):
            if cost > 0:
                ax2.annotate(f'Refugee Cost: ${cost:.1f}B', 
                           xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                           xytext=(0, 10), textcoords='offset points',
                           ha='center', fontsize=9)
        
        ax2.set_xlabel('Scenario')
        ax2.set_ylabel('Net Benefit (Billions USD)')
        ax2.set_title('WestFed Net Financial Outcome')
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax2.grid(True, alpha=0.3)
        
        # 3. Sensitivity Heatmap
        ax3 = plt.subplot(2, 3, 3)
        sensitivity_df = self.sensitivity_analysis()
        
        # Create pivot table for heatmap
        pivot_data = sensitivity_df.pivot_table(
            values='Net_Benefit_of_Accepting',
            index='Refugee_Cost_Per_Person',
            columns='Resource_Value'
        )
        
        im = ax3.imshow(pivot_data.values / 1e9, cmap='RdYlGn', aspect='auto', 
                       extent=[pivot_data.columns.min()/1e9, pivot_data.columns.max()/1e9,
                              pivot_data.index.min()/1000, pivot_data.index.max()/1000])
        ax3.set_title('Sensitivity Analysis: Net Benefit of Accepting Refugees')
        ax3.set_xlabel('Resource Value (Billions USD)')
        ax3.set_ylabel('Cost per Refugee (Thousands USD)')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax3)
        cbar.set_label('Net Benefit (Billions USD)')
        
        # 4. Decision Boundary
        ax4 = plt.subplot(2, 3, 4)
        decision_data = sensitivity_df.pivot_table(
            values='WestFed_Prefers_Refugees',
            index='Refugee_Cost_Per_Person',
            columns='Resource_Value'
        )
        
        im2 = ax4.imshow(decision_data.values, cmap='RdYlBu', aspect='auto',
                        extent=[decision_data.columns.min()/1e9, decision_data.columns.max()/1e9,
                               decision_data.index.min()/1000, decision_data.index.max()/1000])
        ax4.set_title('Decision Matrix: When WestFed Accepts Refugees')
        ax4.set_xlabel('Resource Value (Billions USD)')
        ax4.set_ylabel('Cost per Refugee (Thousands USD)')
        
        # Add colorbar
        cbar2 = plt.colorbar(im2, ax=ax4)
        cbar2.set_label('Accept Refugees (1=Yes, 0=No)')
        
        # 5. Strategic Implications
        ax5 = plt.subplot(2, 3, 5)
        
        # Calculate key thresholds
        base_refugee_cost = 25000
        base_resource_value = 10e9
        
        resource_range = np.linspace(8e9, 15e9, 100)
        break_even_costs = []
        
        for rv in resource_range:
            # At break-even: Priority swap net = Status quo net
            # Priority swap: min(5B, rv) - refugee_cost - 5B = Status quo: min(5B, rv-6B) - 5B
            if rv <= 11e9:  # WestFed gets nothing in status quo
                break_even_cost = min(5e9, rv)  # Can afford up to full repayment
            else:
                break_even_cost = 6e9  # Difference between getting 5B vs getting rv-6B
            
            break_even_costs.append(break_even_cost / 100000)  # Per refugee for 100k refugees
        
        ax5.plot(resource_range / 1e9, break_even_costs, 'b-', linewidth=2, 
                label='Break-even Cost per Refugee')
        ax5.axhline(y=base_refugee_cost, color='red', linestyle='--', 
                   label=f'Current Cost (${base_refugee_cost:,})')
        ax5.fill_between(resource_range / 1e9, 0, break_even_costs, 
                        alpha=0.3, color='green', label='Accept Refugees Zone')
        
        ax5.set_xlabel('Resource Value (Billions USD)')
        ax5.set_ylabel('Break-even Cost per Refugee (USD)')
        ax5.set_title('Strategic Decision Threshold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Game Theory Payoff Matrix
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        
        # Create a simple text-based payoff matrix
        ax6.text(0.5, 0.8, 'Game Theory Payoff Matrix', 
                ha='center', va='center', fontsize=14, fontweight='bold',
                transform=ax6.transAxes)
        
        ax6.text(0.5, 0.65, '(WestFed Net, EastBloc Net in Billions USD)', 
                ha='center', va='center', fontsize=10,
                transform=ax6.transAxes)
        
        # Matrix content
        matrix_text = """
        EastBloc Strategy:    Maintain Loans    Defensive Hosting
        
        WestFed: Reject       (-$1B, +$6B)      (-$1B, +$3.5B)
        WestFed: Accept       (+$2.5B, +$5B)    (+$2.5B, +$1B)
        
        Nash Equilibrium: WestFed Accept, EastBloc Maintain
        """
        
        ax6.text(0.5, 0.35, matrix_text, 
                ha='center', va='center', fontsize=10, fontfamily='monospace',
                transform=ax6.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('simulation_results.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig

def main():
    """Run the complete humanitarian gambit simulation"""
    print("🎯 Humanitarian Gambit Simulation Starting...")
    print("=" * 60)
    
    sim = HumanitarianGambitSimulation()
    
    # Run scenario analysis
    print("\n📊 Running Scenario Analysis...")
    scenario_results = sim.run_scenario_analysis()
    print(scenario_results.to_string(index=False))
    
    # Run sensitivity analysis
    print("\n🔍 Running Sensitivity Analysis...")
    sensitivity_results = sim.sensitivity_analysis()
    
    # Key insights
    print(f"\n🎲 Key Strategic Insights:")
    print(f"   • Total scenarios analyzed: {len(sensitivity_results)}")
    
    accept_percentage = (sensitivity_results['WestFed_Prefers_Refugees'].sum() / 
                        len(sensitivity_results) * 100)
    print(f"   • WestFed prefers accepting refugees in {accept_percentage:.1f}% of scenarios")
    
    max_benefit = sensitivity_results['Net_Benefit_of_Accepting'].max() / 1e9
    print(f"   • Maximum benefit from priority swap: ${max_benefit:.2f}B")
    
    # Create visualizations
    print("\n📈 Generating Visualizations...")
    fig = sim.create_visualizations()
    
    print("\n✅ Simulation Complete!")
    print("📁 Results saved to: simulation_results.png")
    
    return scenario_results, sensitivity_results

if __name__ == "__main__":
    main()