import math

class CaptiveAudienceDilemma:
    def __init__(self):
        # Standard behavioral economics parameters
        self.standard_loss_aversion = 2.25  # Kahneman & Tversky standard coefficient
        
    def model_captive_audience_scenario(self):
        """Model the Target Female's decision using Prospect Theory"""
        
        # Scenario parameters
        orbiters_count = 10
        orbiter_retention_prob = 0.90  # 90% chance of keeping orbiters
        relationship_success_prob = 0.10  # 10% chance of high-value relationship
        
        # Utility values (subjective value units)
        orbiter_utility_each = 3  # Low but consistent validation per orbiter
        high_value_relationship_utility = 100  # High utility from successful relationship
        
        # Current state utility (reference point)
        current_utility = orbiters_count * orbiter_utility_each * orbiter_retention_prob
        print(f"Current Utility (Orbiters): {orbiters_count} × {orbiter_utility_each} × {orbiter_retention_prob} = {current_utility}")
        
        # Potential gain from relationship
        potential_gain = high_value_relationship_utility * relationship_success_prob
        print(f"Potential Gain (Relationship): {high_value_relationship_utility} × {relationship_success_prob} = {potential_gain}")
        
        # Potential loss (losing orbiters for failed relationship attempt)
        potential_loss = current_utility * (1 - relationship_success_prob)  # 90% chance of losing orbiters
        print(f"Potential Loss (Failed Attempt): {current_utility} × {1 - relationship_success_prob} = {potential_loss}")
        
        return {
            'current_utility': current_utility,
            'potential_gain': potential_gain,
            'potential_loss': potential_loss,
            'orbiters_count': orbiters_count,
            'relationship_prob': relationship_success_prob
        }
    
    def calculate_loss_aversion_threshold(self, scenario_data):
        """Calculate the loss aversion coefficient that prevents date acceptance"""
        
        current_utility = scenario_data['current_utility']
        potential_gain = scenario_data['potential_gain']
        potential_loss = scenario_data['potential_loss']
        
        # Prospect Theory Value Function
        # V = π(p) × v(x)
        # Where v(x) = x^α for gains, -λ × (-x)^β for losses
        # Simplified: gains are linear, losses are multiplied by loss aversion coefficient λ
        
        # Expected value calculation
        expected_gain = potential_gain  # Already probability-weighted
        expected_loss_unweighted = potential_loss
        
        print(f"\n=== PROSPECT THEORY CALCULATION ===")
        print(f"Expected Gain: {expected_gain}")
        print(f"Expected Loss (before loss aversion): {expected_loss_unweighted}")
        
        # For decision neutrality: Expected Gain = Loss Aversion × Expected Loss
        # λ = Expected Gain / Expected Loss
        loss_aversion_threshold = expected_gain / expected_loss_unweighted
        
        print(f"Loss Aversion Threshold: {expected_gain} ÷ {expected_loss_unweighted} = {loss_aversion_threshold:.3f}")
        
        # Compare with standard loss aversion coefficient
        standard_perceived_loss = self.standard_loss_aversion * expected_loss_unweighted
        
        print(f"\nStandard Loss Aversion (λ = {self.standard_loss_aversion}):")
        print(f"Perceived Loss: {self.standard_loss_aversion} × {expected_loss_unweighted} = {standard_perceived_loss}")
        print(f"Decision: {'REJECT DATE' if standard_perceived_loss > expected_gain else 'ACCEPT DATE'}")
        
        return {
            'loss_aversion_threshold': loss_aversion_threshold,
            'standard_loss_aversion': self.standard_loss_aversion,
            'expected_gain': expected_gain,
            'expected_loss': expected_loss_unweighted,
            'standard_perceived_loss': standard_perceived_loss,
            'decision_with_standard_la': standard_perceived_loss > expected_gain,
            'decision_margin': standard_perceived_loss - expected_gain
        }
    
    def sensitivity_analysis(self):
        """Analyze how different parameters affect the decision"""
        
        base_scenario = self.model_captive_audience_scenario()
        base_analysis = self.calculate_loss_aversion_threshold(base_scenario)
        
        print(f"\n=== SENSITIVITY ANALYSIS ===")
        
        # Test different orbiter counts
        orbiter_scenarios = [5, 10, 15, 20]
        for orbiter_count in orbiter_scenarios:
            current_utility = orbiter_count * 3 * 0.90
            potential_loss = current_utility * 0.90
            threshold = 10 / potential_loss  # 10 is the expected gain
            
            print(f"Orbiters: {orbiter_count}, Loss Aversion Threshold: {threshold:.3f}")
        
        # Test different relationship success probabilities
        print(f"\nRelationship Success Probability Impact:")
        success_probs = [0.05, 0.10, 0.15, 0.20]
        for prob in success_probs:
            expected_gain = 100 * prob
            threshold = expected_gain / base_scenario['potential_loss']
            print(f"Success Prob: {prob:.0%}, Expected Gain: {expected_gain}, Threshold: {threshold:.3f}")
    
    def calculate_break_even_scenarios(self):
        """Calculate scenarios where the decision would flip"""
        
        base_scenario = self.model_captive_audience_scenario()
        
        print(f"\n=== BREAK-EVEN SCENARIOS ===")
        
        # Scenario 1: What relationship success probability would make her accept?
        required_gain = self.standard_loss_aversion * base_scenario['potential_loss']
        required_success_prob = required_gain / 100  # 100 is relationship utility
        
        print(f"Required relationship success probability: {required_success_prob:.1%}")
        
        # Scenario 2: What orbiter count would make her accept?
        max_acceptable_loss = base_scenario['potential_gain'] / self.standard_loss_aversion
        max_current_utility = max_acceptable_loss / 0.90  # 90% loss probability
        max_orbiters = max_current_utility / (3 * 0.90)  # 3 utility per orbiter, 90% retention
        
        print(f"Maximum orbiter count for acceptance: {max_orbiters:.1f}")
        
        return {
            'required_success_probability': required_success_prob,
            'max_acceptable_orbiters': max_orbiters
        }

if __name__ == "__main__":
    model = CaptiveAudienceDilemma()
    
    print("=== CAPTIVE AUDIENCE DILEMMA: PROSPECT THEORY MODEL ===")
    
    # Main scenario analysis
    scenario = model.model_captive_audience_scenario()
    analysis = model.calculate_loss_aversion_threshold(scenario)
    
    print(f"\n=== KEY FINDINGS ===")
    print(f"Loss Aversion Threshold for Neutrality: {analysis['loss_aversion_threshold']:.3f}")
    print(f"Standard Loss Aversion Coefficient: {analysis['standard_loss_aversion']}")
    print(f"Decision Margin: {analysis['decision_margin']:.1f} utility units")
    print(f"Predicted Decision: {'REJECT DATE' if analysis['decision_with_standard_la'] else 'ACCEPT DATE'}")
    
    # Additional analyses
    model.sensitivity_analysis()
    break_even = model.calculate_break_even_scenarios()
    
    print(f"\n=== MATHEMATICAL PROOF ===")
    print(f"Prospect Theory Formula: V = π(p_gain) × v(gain) - λ × π(p_loss) × v(loss)")
    print(f"Where λ = Loss Aversion Coefficient")
    print(f"")
    print(f"For our scenario:")
    print(f"V = 0.10 × 100 - λ × 0.90 × 27")
    print(f"V = 10 - λ × 24.3")
    print(f"")
    print(f"At λ = 2.25 (standard): V = 10 - 2.25 × 24.3 = 10 - 54.675 = -44.675")
    print(f"Negative value → REJECT DATE")
    print(f"")
    print(f"Threshold λ for neutrality: 10 ÷ 24.3 = {10/24.3:.3f}")
    print(f"Since 2.25 > 0.412, loss aversion prevents date acceptance.")