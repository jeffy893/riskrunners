import math

class SolidarityShortSimulation:
    def __init__(self):
        self.initial_mystery_value = 50
        self.initial_dignity_options = 100
        self.ecosystem_antisocial_rate = 0.20  # 20% monthly inflation from complaints
        
    def simulate_12_months(self):
        """Simulate Solidarity Short strategy over 12 months"""
        results = []
        mystery_value = self.initial_mystery_value
        dignity_options = self.initial_dignity_options
        
        for month in range(1, 13):
            # Solidarity Short mechanics
            complaints_refused = self.calculate_complaints_refused(month)
            dignity_investment = self.calculate_dignity_investment(month)
            mystery_appreciation = self.calculate_mystery_appreciation(month, dignity_options)
            
            # Update values
            dignity_options += dignity_investment
            mystery_value += mystery_appreciation
            
            # Calculate ecosystem comparison (what typical member loses)
            ecosystem_loss = self.calculate_ecosystem_member_loss(month)
            
            results.append({
                'month': month,
                'mystery_value': round(mystery_value, 2),
                'dignity_options': round(dignity_options, 2),
                'complaints_refused': complaints_refused,
                'dignity_investment': round(dignity_investment, 2),
                'mystery_appreciation': round(mystery_appreciation, 2),
                'ecosystem_member_loss': round(ecosystem_loss, 2),
                'relative_advantage': round(mystery_appreciation - ecosystem_loss, 2)
            })
            
        return results
    
    def calculate_complaints_refused(self, month):
        """Calculate complaints refused (opportunity cost of not participating in antisocial inflation)"""
        # Typical member complains 3-5 times per month, escalating over time
        return min(3 + (month * 0.5), 8)
    
    def calculate_dignity_investment(self, month):
        """Calculate dignity options appreciation from autonomous behavior"""
        # Dignity appreciates as user demonstrates independence from group-think
        base_investment = 5  # 5% monthly base growth
        autonomy_bonus = month * 0.3  # Increasing returns from consistent autonomous behavior
        return base_investment + autonomy_bonus
    
    def calculate_mystery_appreciation(self, month, current_dignity):
        """Calculate Mystery Value increase from non-participation in complaint culture"""
        # Mystery grows from scarcity (not being like everyone else)
        scarcity_multiplier = 1 + (current_dignity / 1000)  # Dignity enhances mystery
        base_mystery_growth = 4 * scarcity_multiplier  # 4% base growth enhanced by dignity
        
        # Compound effect: mystery becomes more valuable as ecosystem degrades
        ecosystem_degradation_bonus = month * 0.2
        
        return base_mystery_growth + ecosystem_degradation_bonus
    
    def calculate_ecosystem_member_loss(self, month):
        """Calculate what typical ecosystem member loses to antisocial inflation"""
        complaints_per_month = 4  # Average complaints
        monthly_loss = complaints_per_month * (self.ecosystem_antisocial_rate * 100)
        return monthly_loss * month  # Cumulative loss
    
    def generate_summary_report(self):
        """Generate 12-month summary report"""
        monthly_results = self.simulate_12_months()
        final_month = monthly_results[-1]
        
        total_mystery_increase = final_month['mystery_value'] - self.initial_mystery_value
        total_dignity_increase = final_month['dignity_options'] - self.initial_dignity_options
        total_complaints_refused = sum(r['complaints_refused'] for r in monthly_results)
        
        return {
            'strategy': 'Solidarity Short',
            'duration_months': 12,
            'initial_mystery_value': self.initial_mystery_value,
            'final_mystery_value': final_month['mystery_value'],
            'mystery_value_increase': round(total_mystery_increase, 2),
            'mystery_roi_percentage': round((total_mystery_increase / self.initial_mystery_value) * 100, 1),
            'final_dignity_options': final_month['dignity_options'],
            'dignity_increase': round(total_dignity_increase, 2),
            'total_complaints_refused': round(total_complaints_refused, 1),
            'ecosystem_member_total_loss': final_month['ecosystem_member_loss'],
            'relative_advantage': round(total_mystery_increase + final_month['ecosystem_member_loss'], 2),
            'monthly_breakdown': monthly_results
        }

if __name__ == "__main__":
    simulation = SolidarityShortSimulation()
    report = simulation.generate_summary_report()
    
    print("=== SOLIDARITY SHORT: 12-MONTH MYSTERY VALUE PROJECTION ===")
    print(f"Initial Mystery Value: {report['initial_mystery_value']}")
    print(f"Final Mystery Value: {report['final_mystery_value']}")
    print(f"Mystery Value Increase: +{report['mystery_value_increase']} ({report['mystery_roi_percentage']}% ROI)")
    print(f"Final Dignity Options: {report['final_dignity_options']}")
    print(f"Total Complaints Refused: {report['total_complaints_refused']}")
    print(f"Ecosystem Member Loss: -{report['ecosystem_member_total_loss']}")
    print(f"Total Relative Advantage: +{report['relative_advantage']}")
    
    print("\n=== MONTHLY BREAKDOWN ===")
    for month_data in report['monthly_breakdown']:
        print(f"Month {month_data['month']}: Mystery={month_data['mystery_value']}, "
              f"Dignity={month_data['dignity_options']}, "
              f"Advantage=+{month_data['relative_advantage']}")