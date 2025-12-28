from espresso_art_ecosystem import EspressoArtEcosystem
from solidarity_short import SolidarityShort
from behavioral_models import VulnerabilityArbitrage, ProspectTheory

class EconomicOverture:
    def __init__(self):
        self.ecosystem = EspressoArtEcosystem()
        self.strategy = SolidarityShort()
        self.vulnerability = VulnerabilityArbitrage()
        self.prospect = ProspectTheory()
        
    def run_full_simulation(self):
        """Execute complete economic overture simulation"""
        
        # Phase 1: Market Analysis
        typical_member_roi = self.ecosystem.investment_roi(12, 15, 50)  # Heavy complainer
        
        # Phase 2: Solidarity Short Strategy
        strategy_results = self.strategy.execute_strategy(12)
        
        # Phase 3: Vulnerability Arbitrage
        trust_boost = self.vulnerability.karaoke_poetry_effect(85, 80)
        barbie_trust = self.vulnerability.barbie_group_trust()
        
        # Phase 4: Prospect Theory Analysis
        dating_analysis = self.prospect.captive_audience_dilemma()
        velocity_effect = self.prospect.coming_in_hot_effect()
        
        # Phase 5: Market Exit Report
        exit_report = self.generate_exit_report(strategy_results, trust_boost)
        
        return {
            'ecosystem_analysis': {
                'typical_member_roi': typical_member_roi,
                'recommendation': 'AVOID INVESTMENT'
            },
            'solidarity_short': strategy_results,
            'vulnerability_arbitrage': {
                'trust_index': trust_boost,
                'barbie_comparison': trust_boost - barbie_trust
            },
            'prospect_theory': {
                'standard_dating': dating_analysis,
                'velocity_override': velocity_effect
            },
            'exit_report': exit_report
        }
    
    def generate_exit_report(self, strategy_results, trust_index):
        """Generate final market exit report"""
        respect_earned = min(trust_index / 10, 10)  # The Wave/Smile metric
        dignity_retained = strategy_results['dignity_final']
        energy_conserved = 100 - (12 * 2)  # Energy saved by not commiserating
        
        total_roi = respect_earned + dignity_retained + energy_conserved - 200
        
        return {
            'respect_earned': respect_earned,
            'dignity_retained': dignity_retained,
            'energy_conserved': energy_conserved,
            'total_roi_percentage': total_roi,
            'exit_status': 'SUCCESSFUL' if total_roi > 0 else 'BREAK_EVEN'
        }

if __name__ == "__main__":
    simulation = EconomicOverture()
    results = simulation.run_full_simulation()
    
    print("=== ECONOMIC OVERTURE SIMULATION RESULTS ===")
    print(f"Ecosystem ROI: {results['ecosystem_analysis']['typical_member_roi']:.1f}%")
    print(f"Solidarity Short ROI: {results['solidarity_short']['total_roi']:.1f}%")
    print(f"Trust Index Boost: {results['vulnerability_arbitrage']['trust_index']:.1f}")
    print(f"Velocity Dating Success: {results['prospect_theory']['velocity_override']['velocity_acceptance']}")
    print(f"Final Exit ROI: {results['exit_report']['total_roi_percentage']:.1f}%")
    print(f"Exit Status: {results['exit_report']['exit_status']}")