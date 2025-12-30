import math

class ComingInHotModel:
    def __init__(self):
        self.standard_loss_aversion = 2.25
        self.base_scenario = {
            'current_utility': 27.0,  # 10 orbiters × 3 utility × 0.9 retention
            'potential_gain': 10.0,   # 100 utility × 0.1 success prob
            'potential_loss': 24.3    # 27.0 × 0.9 loss prob
        }
        
    def calculate_velocity_effect(self, decision_time_reduction):
        """Calculate how reduced decision time affects loss aversion processing"""
        
        # Cognitive processing model: Loss aversion requires deliberative thinking
        # Fast decisions bypass System 2 (analytical) and rely on System 1 (intuitive)
        
        # Base loss aversion coefficient modification
        # As decision time → 0, loss aversion processing → minimal
        velocity_loss_aversion = self.standard_loss_aversion * (1 - decision_time_reduction)
        
        # Calculate decision value with modified loss aversion
        expected_gain = self.base_scenario['potential_gain']
        expected_loss = self.base_scenario['potential_loss']
        
        # Standard decision (full deliberation time)
        standard_perceived_loss = self.standard_loss_aversion * expected_loss
        standard_value = expected_gain - standard_perceived_loss
        
        # Velocity decision (reduced deliberation time)
        velocity_perceived_loss = velocity_loss_aversion * expected_loss
        velocity_value = expected_gain - velocity_perceived_loss
        
        return {
            'decision_time_reduction': decision_time_reduction,
            'velocity_loss_aversion': velocity_loss_aversion,
            'standard_value': standard_value,
            'velocity_value': velocity_value,
            'value_improvement': velocity_value - standard_value,
            'standard_decision': standard_value > 0,
            'velocity_decision': velocity_value > 0,
            'decision_flip': (standard_value <= 0) and (velocity_value > 0)
        }
    
    def model_kinetic_energy_spectrum(self):
        """Model decision outcomes across different kinetic energy levels"""
        
        print("=== COMING IN HOT: KINETIC ENERGY SPECTRUM ===")
        print("Decision Time Reduction | Loss Aversion | Decision Value | Accept Date?")
        print("-" * 70)
        
        results = []
        
        # Test different velocity levels
        velocity_levels = [0.0, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
        
        for velocity in velocity_levels:
            result = self.calculate_velocity_effect(velocity)
            results.append(result)
            
            print(f"{velocity:>18.0%} | {result['velocity_loss_aversion']:>11.2f} | "
                  f"{result['velocity_value']:>12.1f} | {'YES' if result['velocity_decision'] else 'NO':>10}")
        
        return results
    
    def find_velocity_threshold(self):
        """Find the minimum velocity needed to flip the decision"""
        
        # Binary search for the exact threshold
        low, high = 0.0, 1.0
        threshold = None
        
        for _ in range(50):  # Precision iterations
            mid = (low + high) / 2
            result = self.calculate_velocity_effect(mid)
            
            if result['velocity_value'] > 0:
                threshold = mid
                high = mid
            else:
                low = mid
                
            if high - low < 0.0001:  # Sufficient precision
                break
        
        return threshold
    
    def analyze_cognitive_mechanisms(self):
        """Analyze the cognitive mechanisms behind velocity override"""
        
        print("\n=== COGNITIVE MECHANISMS ANALYSIS ===")
        
        # System 1 vs System 2 processing
        system1_characteristics = {
            'processing_speed': 'Fast (milliseconds)',
            'cognitive_load': 'Low',
            'loss_aversion_activation': 'Minimal',
            'decision_basis': 'Intuitive/Emotional',
            'energy_required': 'Low'
        }
        
        system2_characteristics = {
            'processing_speed': 'Slow (seconds to minutes)',
            'cognitive_load': 'High',
            'loss_aversion_activation': 'Full',
            'decision_basis': 'Analytical/Rational',
            'energy_required': 'High'
        }
        
        print("System 1 (Fast/Intuitive):")
        for key, value in system1_characteristics.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
            
        print("\nSystem 2 (Slow/Analytical):")
        for key, value in system2_characteristics.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    def calculate_approach_strategies(self):
        """Calculate optimal approach strategies using velocity"""
        
        print("\n=== OPTIMAL APPROACH STRATEGIES ===")
        
        strategies = {
            'standard_approach': {
                'velocity': 0.0,
                'description': 'Traditional courtship, gives time to think',
                'success_factors': ['Comfort building', 'Logical persuasion'],
                'failure_points': ['Activates loss aversion', 'Overthinking']
            },
            'medium_velocity': {
                'velocity': 0.50,
                'description': 'Confident but not rushed',
                'success_factors': ['Reduces analysis paralysis', 'Shows decisiveness'],
                'failure_points': ['May seem pushy', 'Partial loss aversion']
            },
            'high_velocity': {
                'velocity': 0.90,
                'description': 'Decisive, immediate action',
                'success_factors': ['Bypasses loss aversion', 'Creates urgency'],
                'failure_points': ['May seem aggressive', 'Requires perfect timing']
            },
            'maximum_velocity': {
                'velocity': 0.99,
                'description': 'Instantaneous decision required',
                'success_factors': ['Pure System 1 response', 'No deliberation time'],
                'failure_points': ['High risk if mistimed', 'Requires exceptional confidence']
            }
        }
        
        for strategy_name, strategy_data in strategies.items():
            result = self.calculate_velocity_effect(strategy_data['velocity'])
            print(f"\n{strategy_name.replace('_', ' ').title()}:")
            print(f"  Velocity: {strategy_data['velocity']:.0%}")
            print(f"  Decision Value: {result['velocity_value']:.1f}")
            print(f"  Success Probability: {'HIGH' if result['velocity_decision'] else 'LOW'}")
            print(f"  Description: {strategy_data['description']}")
    
    def mathematical_proof(self):
        """Provide mathematical proof of velocity override"""
        
        print("\n=== MATHEMATICAL PROOF: COMING IN HOT OVERRIDE ===")
        
        threshold = self.find_velocity_threshold()
        
        print(f"Standard Prospect Theory:")
        print(f"V = Expected Gain - λ × Expected Loss")
        print(f"V = 10.0 - 2.25 × 24.3 = -44.675 (REJECT)")
        
        print(f"\nVelocity-Modified Prospect Theory:")
        print(f"V = Expected Gain - λ(1-v) × Expected Loss")
        print(f"Where v = velocity (decision time reduction)")
        
        print(f"\nThreshold Calculation:")
        print(f"For V = 0: 10.0 = λ(1-v) × 24.3")
        print(f"10.0 = 2.25(1-v) × 24.3")
        print(f"10.0 = 54.675(1-v)")
        print(f"1-v = 10.0/54.675 = 0.183")
        print(f"v = 1 - 0.183 = 0.817")
        
        print(f"\nVelocity Threshold: {threshold:.1%}")
        print(f"At v ≥ {threshold:.1%}, velocity overrides loss aversion")
        
        return threshold

if __name__ == "__main__":
    model = ComingInHotModel()
    
    # Main analysis
    spectrum_results = model.model_kinetic_energy_spectrum()
    
    # Find threshold
    threshold = model.find_velocity_threshold()
    print(f"\nVELOCITY THRESHOLD FOR SUCCESS: {threshold:.1%}")
    
    # Cognitive analysis
    model.analyze_cognitive_mechanisms()
    
    # Strategy analysis
    model.calculate_approach_strategies()
    
    # Mathematical proof
    model.mathematical_proof()
    
    # Key findings summary
    print(f"\n=== KEY FINDINGS ===")
    print(f"1. Velocity Threshold: {threshold:.1%} decision time reduction")
    print(f"2. At 90% velocity: Decision flips from REJECT to ACCEPT")
    print(f"3. Mechanism: Fast decisions bypass System 2 loss aversion processing")
    print(f"4. Optimal Strategy: Coming in hot approach (90%+ velocity)")
    print(f"5. Mathematical Proof: v ≥ 0.817 overrides λ = 2.25 loss aversion")