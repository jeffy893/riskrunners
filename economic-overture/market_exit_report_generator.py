import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from datetime import datetime
import json

class MarketExitReport:
    def __init__(self):
        self.initial_investment = 100  # Starting social capital
        self.months_in_ecosystem = 12
        
    def calculate_final_roi(self):
        """Calculate final ROI components for market exit"""
        
        # 1. Respect Earned (The Wave/Smile metric)
        # Based on vulnerability arbitrage trust index and consistent dignity
        base_respect = 15  # Baseline respect in community
        vulnerability_arbitrage_bonus = 25  # From karaoke + poetry performance
        consistency_multiplier = 1.8  # 12 months of consistent behavior
        respect_earned = (base_respect + vulnerability_arbitrage_bonus) * consistency_multiplier
        
        # 2. Dignity Retained
        # Avoided complaint currency, maintained autonomous behavior
        initial_dignity = 100
        dignity_appreciation = 83.4  # From solidarity short simulation
        dignity_retained = initial_dignity + dignity_appreciation
        
        # 3. Energy Conserved by Not Commiserating
        # Energy saved by refusing to participate in complaint culture
        typical_commiseration_cost = 5  # Energy units per month
        months = 12
        energy_conserved = typical_commiseration_cost * months * 2  # 2x multiplier for compound effect
        
        # Calculate total ROI
        total_gains = respect_earned + dignity_retained + energy_conserved
        total_investment = self.initial_investment * 3  # Initial investment across all categories
        roi_percentage = ((total_gains - total_investment) / total_investment) * 100
        
        return {
            'respect_earned': respect_earned,
            'dignity_retained': dignity_retained,
            'energy_conserved': energy_conserved,
            'total_gains': total_gains,
            'total_investment': total_investment,
            'roi_percentage': roi_percentage,
            'exit_status': 'HIGHLY SUCCESSFUL' if roi_percentage > 50 else 'SUCCESSFUL' if roi_percentage > 0 else 'BREAK_EVEN'
        }
    
    def generate_visual_dashboard(self):
        """Generate comprehensive visual dashboard"""
        
        # Set up the figure with subplots
        fig = plt.figure(figsize=(20, 14))
        fig.suptitle('ECONOMIC OVERTURE: MARKET EXIT REPORT\nEspresso Art Ecosystem Analysis', 
                     fontsize=24, fontweight='bold', y=0.97)
        
        # Calculate all metrics
        exit_data = self.calculate_final_roi()
        
        # Create grid layout - more compact
        gs = fig.add_gridspec(3, 4, hspace=0.25, wspace=0.25)
        
        # 1. ROI Summary (top left)
        ax1 = fig.add_subplot(gs[0, :2])
        self.create_roi_summary(ax1, exit_data)
        
        # 2. Strategy Performance (top right)
        ax2 = fig.add_subplot(gs[0, 2:])
        self.create_strategy_performance(ax2)
        
        # 3. Trust Index Comparison (middle left)
        ax3 = fig.add_subplot(gs[1, :2])
        self.create_trust_comparison(ax3)
        
        # 4. Velocity Override Analysis (middle right)
        ax4 = fig.add_subplot(gs[1, 2:])
        self.create_velocity_analysis(ax4)
        
        # 5. Timeline Analysis (bottom left)
        ax5 = fig.add_subplot(gs[2, :2])
        self.create_timeline_analysis(ax5)
        
        # 6. Final Metrics Dashboard (bottom right)
        ax6 = fig.add_subplot(gs[2, 2:])
        self.create_metrics_dashboard(ax6, exit_data)
        
        # Add exit summary as text box
        exit_summary_text = f"""MARKET EXIT: Moving to Chandler | SOLIDARITY SHORT CLOSED
Final ROI: {exit_data['roi_percentage']:.1f}% - {exit_data['exit_status']}
Strategy Validated: Dignity preserved, energy conserved"""
        
        fig.text(0.5, 0.02, exit_summary_text, fontsize=12, ha='center',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.8))
        
        plt.tight_layout()
        return fig
    
    def create_roi_summary(self, ax, exit_data):
        """Create ROI summary visualization"""
        ax.set_title('SOLIDARITY SHORT: FINAL ROI', fontweight='bold', fontsize=14)
        
        categories = ['Respect\nEarned', 'Dignity\nRetained', 'Energy\nConserved']
        values = [exit_data['respect_earned'], exit_data['dignity_retained'], exit_data['energy_conserved']]
        colors = ['#2E8B57', '#4169E1', '#FF6347']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.8)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                   f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Value Units')
        ax.grid(True, alpha=0.3)
        
        # Add ROI percentage
        ax.text(0.5, 0.95, f'Total ROI: {exit_data["roi_percentage"]:.1f}%', 
                transform=ax.transAxes, ha='center', va='top', 
                fontsize=16, fontweight='bold', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8))
    
    def create_strategy_performance(self, ax):
        """Create strategy performance comparison"""
        ax.set_title('STRATEGY PERFORMANCE COMPARISON', fontweight='bold', fontsize=14)
        
        strategies = ['Typical\nMember', 'Solidarity\nShort', 'Vulnerability\nArbitrage']
        performance = [-64.9, 62.8, 140.1]  # ROI percentages
        colors = ['#DC143C', '#32CD32', '#FFD700']
        
        bars = ax.bar(strategies, performance, color=colors, alpha=0.8)
        
        # Add value labels
        for bar, value in zip(bars, performance):
            height = bar.get_height()
            y_pos = height + 5 if height > 0 else height - 10
            ax.text(bar.get_x() + bar.get_width()/2., y_pos,
                   f'{value:.1f}%', ha='center', va='bottom' if height > 0 else 'top', 
                   fontweight='bold')
        
        ax.set_ylabel('ROI Percentage')
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax.grid(True, alpha=0.3)
    
    def create_trust_comparison(self, ax):
        """Create trust index comparison"""
        ax.set_title('TRUST INDEX: VULNERABILITY ARBITRAGE EFFECT', fontweight='bold', fontsize=14)
        
        groups = ['Barbie\nGroup', 'General\nAudience', 'Espresso\nArt', 'Elder\nObservers']
        trust_values = [28.3, 70.8, 49.6, 92.0]
        colors = ['#FF69B4', '#87CEEB', '#8B4513', '#DAA520']
        
        bars = ax.bar(groups, trust_values, color=colors, alpha=0.8)
        
        # Add value labels
        for bar, value in zip(bars, trust_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Trust Index')
        ax.grid(True, alpha=0.3)
    
    def create_velocity_analysis(self, ax):
        """Create velocity override analysis"""
        ax.set_title('COMING IN HOT: VELOCITY OVERRIDE PRINCIPLE', fontweight='bold', fontsize=14)
        
        velocities = [0, 25, 50, 75, 90, 95, 99]
        decision_values = [-44.7, -31.0, -17.3, -3.7, 4.5, 7.3, 9.5]
        
        colors = ['red' if x < 0 else 'green' for x in decision_values]
        ax.bar(velocities, decision_values, color=colors, alpha=0.7)
        
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.8, label='Decision Threshold')
        ax.axvline(x=81.7, color='orange', linestyle='--', alpha=0.8, label='Coming In Hot Threshold (81.7%)')
        
        ax.set_xlabel('Velocity (% Decision Time Reduction)')
        ax.set_ylabel('Decision Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def create_timeline_analysis(self, ax):
        """Create 12-month timeline analysis"""
        ax.set_title('12-MONTH MYSTERY VALUE PROGRESSION', fontweight='bold', fontsize=14)
        
        months = list(range(1, 13))
        mystery_values = [54.6, 59.4, 64.5, 69.7, 75.2, 80.9, 86.9, 93.1, 99.5, 106.1, 113.0, 120.1]
        ecosystem_loss = [80, 160, 240, 320, 400, 480, 560, 640, 720, 800, 880, 960]
        
        ax.plot(months, mystery_values, 'g-', linewidth=3, marker='o', label='Mystery Value (Solidarity Short)')
        ax.plot(months, [100 - x for x in ecosystem_loss], 'r--', linewidth=2, label='Typical Member Loss')
        
        ax.set_xlabel('Months')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.fill_between(months, mystery_values, alpha=0.3, color='green')
    
    def create_metrics_dashboard(self, ax, exit_data):
        """Create final metrics dashboard"""
        ax.set_title('FINAL METRICS DASHBOARD', fontweight='bold', fontsize=14)
        ax.axis('off')
        
        # Create metric boxes
        metrics = [
            ('Total ROI', f"{exit_data['roi_percentage']:.1f}%", '#32CD32'),
            ('Exit Status', exit_data['exit_status'], '#FFD700'),
            ('Respect Earned', f"{exit_data['respect_earned']:.1f}", '#4169E1'),
            ('Dignity Retained', f"{exit_data['dignity_retained']:.1f}", '#FF6347'),
            ('Energy Conserved', f"{exit_data['energy_conserved']:.1f}", '#9370DB'),
            ('Total Gains', f"{exit_data['total_gains']:.1f}", '#2E8B57')
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            x = (i % 3) * 0.33
            y = 0.7 if i < 3 else 0.2
            
            # Create fancy box
            bbox = FancyBboxPatch((x, y), 0.28, 0.25, 
                                boxstyle="round,pad=0.02", 
                                facecolor=color, alpha=0.3, 
                                edgecolor=color, linewidth=2)
            ax.add_patch(bbox)
            
            # Add text
            ax.text(x + 0.14, y + 0.18, label, ha='center', va='center', 
                   fontweight='bold', fontsize=10)
            ax.text(x + 0.14, y + 0.08, value, ha='center', va='center', 
                   fontweight='bold', fontsize=14)
    
    def create_exit_summary(self, ax, exit_data):
        """Create market exit summary"""
        ax.set_title('MARKET EXIT SUMMARY: MOVING TO CHANDLER', fontweight='bold', fontsize=16)
        ax.axis('off')
        
        summary_text = f"""
SOLIDARITY SHORT POSITION CLOSED - FINAL RESULTS:

✓ STRATEGY: Refused to trade in 'complaining currency' (Antisocial Inflation)
✓ INVESTMENT: Dignity Options (autonomous behavior) + Vulnerability Arbitrage
✓ DURATION: 12 months in Espresso Art ecosystem
✓ EXIT TRIGGER: Geographic relocation to Chandler

FINAL ROI BREAKDOWN:
• Respect Earned (The Wave/Smile): {exit_data['respect_earned']:.1f} units
• Dignity Retained: {exit_data['dignity_retained']:.1f} units  
• Energy Conserved: {exit_data['energy_conserved']:.1f} units
• Total Investment: {exit_data['total_investment']:.1f} units
• Total Gains: {exit_data['total_gains']:.1f} units

FINAL ROI: {exit_data['roi_percentage']:.1f}% - {exit_data['exit_status']}

RECOMMENDATION: Strategy validated. Solidarity Short approach generated positive returns
while preserving dignity and avoiding ecosystem degradation effects.
        """
        
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, 
               fontsize=11, va='top', ha='left', 
               bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))
    
    def generate_html_report(self):
        """Generate HTML report"""
        exit_data = self.calculate_final_roi()
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Economic Overture: Market Exit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; }}
        .metric-box {{ display: inline-block; margin: 10px; padding: 15px; border-radius: 8px; text-align: center; min-width: 150px; }}
        .success {{ background-color: #d4edda; border: 1px solid #c3e6cb; }}
        .warning {{ background-color: #fff3cd; border: 1px solid #ffeaa7; }}
        .info {{ background-color: #d1ecf1; border: 1px solid #bee5eb; }}
        .metric-value {{ font-size: 24px; font-weight: bold; }}
        .metric-label {{ font-size: 14px; color: #666; }}
        .section {{ margin: 30px 0; padding: 20px; border-left: 4px solid #3498db; }}
        .roi-positive {{ color: #27ae60; font-weight: bold; }}
        .roi-negative {{ color: #e74c3c; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>ECONOMIC OVERTURE: MARKET EXIT REPORT</h1>
        <h2>Espresso Art Ecosystem Analysis - Final Results</h2>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="container">
        <div class="section">
            <h2>Executive Summary</h2>
            <p>The Solidarity Short position has been successfully closed following the user's relocation to Chandler. 
            The strategy of refusing to trade in 'complaining currency' while investing in Dignity Options has generated 
            substantial positive returns across all measured categories.</p>
            
            <div class="metric-box success">
                <div class="metric-value roi-positive">{exit_data['roi_percentage']:.1f}%</div>
                <div class="metric-label">Total ROI</div>
            </div>
            
            <div class="metric-box info">
                <div class="metric-value">{exit_data['exit_status']}</div>
                <div class="metric-label">Exit Status</div>
            </div>
            
            <div class="metric-box success">
                <div class="metric-value">{exit_data['total_gains']:.0f}</div>
                <div class="metric-label">Total Gains</div>
            </div>
        </div>
        
        <div class="section">
            <h2>ROI Component Analysis</h2>
            <table>
                <tr>
                    <th>Component</th>
                    <th>Value</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>Respect Earned (The Wave/Smile)</td>
                    <td class="roi-positive">{exit_data['respect_earned']:.1f}</td>
                    <td>Trust index from vulnerability arbitrage + consistent dignity</td>
                </tr>
                <tr>
                    <td>Dignity Retained</td>
                    <td class="roi-positive">{exit_data['dignity_retained']:.1f}</td>
                    <td>Autonomous behavior investment + appreciation</td>
                </tr>
                <tr>
                    <td>Energy Conserved</td>
                    <td class="roi-positive">{exit_data['energy_conserved']:.1f}</td>
                    <td>Energy saved by refusing to commiserate</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Strategy Performance Summary</h2>
            <ul>
                <li><strong>Solidarity Short ROI:</strong> <span class="roi-positive">+62.8%</span></li>
                <li><strong>Vulnerability Arbitrage ROI:</strong> <span class="roi-positive">+140.1%</span></li>
                <li><strong>Typical Ecosystem Member:</strong> <span class="roi-negative">-64.9%</span></li>
                <li><strong>Velocity Override Success:</strong> 90% kinetic energy threshold achieved</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Key Findings</h2>
            <ol>
                <li><strong>Ecosystem Avoidance Validated:</strong> Refusing to participate in complaint culture prevented -64.9% losses</li>
                <li><strong>Vulnerability Arbitrage Effective:</strong> High-competence + high-vulnerability combination generated 3.25x trust premium</li>
                <li><strong>Velocity Override Confirmed:</strong> 90% decision time reduction successfully bypassed loss aversion</li>
                <li><strong>Mystery Value Appreciation:</strong> 140.1% ROI from scarcity and non-participation</li>
                <li><strong>Dignity Options Successful:</strong> Autonomous behavior investment yielded consistent returns</li>
            </ol>
        </div>
        
        <div class="section">
            <h2>Market Exit Recommendation</h2>
            <p><strong>POSITION CLOSED SUCCESSFULLY</strong></p>
            <p>The Solidarity Short strategy has been validated through 12 months of execution. 
            The user exits with preserved dignity, enhanced social capital, and substantial energy reserves. 
            The geographic relocation to Chandler provides a natural exit point with all gains realized.</p>
            
            <p><strong>Future Strategy:</strong> Apply learned principles in new environment while maintaining 
            dignity-focused investment approach and vulnerability arbitrage techniques.</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html_content

if __name__ == "__main__":
    # Generate market exit report
    report = MarketExitReport()
    
    # Create visual dashboard
    fig = report.generate_visual_dashboard()
    
    # Save PNG
    plt.savefig('/Users/jefferson/000_coderepo/riskrunners/economic-overture/market_exit_dashboard.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    
    # Generate and save HTML report
    html_content = report.generate_html_report()
    with open('/Users/jefferson/000_coderepo/riskrunners/economic-overture/market_exit_report.html', 'w') as f:
        f.write(html_content)
    
    # Calculate and display final results
    exit_data = report.calculate_final_roi()
    
    print("=== MARKET EXIT REPORT: SOLIDARITY SHORT CLOSED ===")
    print(f"Exit Status: {exit_data['exit_status']}")
    print(f"Total ROI: {exit_data['roi_percentage']:.1f}%")
    print(f"Respect Earned: {exit_data['respect_earned']:.1f}")
    print(f"Dignity Retained: {exit_data['dignity_retained']:.1f}")
    print(f"Energy Conserved: {exit_data['energy_conserved']:.1f}")
    print(f"Total Gains: {exit_data['total_gains']:.1f}")
    print("\nFiles generated:")
    print("- market_exit_dashboard.png")
    print("- market_exit_report.html")
    
    plt.show()