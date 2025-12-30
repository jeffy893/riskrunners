import math

class VulnerabilityArbitrage:
    def __init__(self):
        self.trust_index_base = 30
        
    def karaoke_poetry_effect(self, competence_level, vulnerability_level):
        """Calculate trust index from high-competence + high-vulnerability mix"""
        # Typing for elders = high competence (80-90)
        # Karaoke = high vulnerability (70-85)
        trust_multiplier = (competence_level * vulnerability_level) / 10000
        return self.trust_index_base * (1 + trust_multiplier)
    
    def barbie_group_trust(self):
        """Low-trust environment baseline"""
        return 15  # Barbie group trust index

class ProspectTheory:
    def __init__(self):
        self.loss_aversion_coefficient = 2.25  # Standard behavioral economics value
        
    def captive_audience_dilemma(self, orbiters_count=10, relationship_prob=0.1):
        """Model the captive audience vs high-value relationship decision"""
        # Current utility from orbiters (certain)
        current_utility = orbiters_count * 0.3  # Low but certain validation
        
        # Potential utility from relationship (uncertain)
        potential_utility = 100 * relationship_prob  # High but uncertain value
        
        # Loss aversion calculation
        perceived_loss = current_utility * self.loss_aversion_coefficient
        
        return {
            'current_utility': current_utility,
            'potential_utility': potential_utility,
            'perceived_loss': perceived_loss,
            'decision_threshold': perceived_loss - potential_utility,
            'will_accept_date': potential_utility > perceived_loss
        }
    
    def coming_in_hot_effect(self, decision_time_reduction=0.9):
        """High kinetic energy approach reducing decision time"""
        # Velocity override: less time to calculate loss aversion
        modified_loss_aversion = self.loss_aversion_coefficient * (1 - decision_time_reduction)
        
        original_result = self.captive_audience_dilemma()
        modified_perceived_loss = original_result['current_utility'] * modified_loss_aversion
        
        return {
            'original_acceptance': original_result['will_accept_date'],
            'velocity_acceptance': original_result['potential_utility'] > modified_perceived_loss,
            'velocity_improvement': modified_loss_aversion < self.loss_aversion_coefficient
        }