import sqlite3
import networkx as nx
import matplotlib.pyplot as plt # Optional: for visualizing the graph

# --- 1. Define the Risk Factor Data ---
# Transcribed from the Microchip affects/2 Prolog predicates
microchip_risk_factors = [
    ('changes_in_demand', 'fluctuating_operating_results'),
    ('market_acceptance_issues', 'fluctuating_operating_results'),
    ('customer_inventory_levels', 'fluctuating_operating_results'),
    ('inventory_mix_issues', 'fluctuating_operating_results'),
    ('inability_to_satisfy_orders', 'fluctuating_operating_results'),
    ('manufacturing_capacity_utilization_changes', 'fluctuating_operating_results'),
    ('manufacturing_yield_fluctuations', 'fluctuating_operating_results'),
    ('insufficient_assembly_testing_capacity', 'fluctuating_operating_results'),
    ('raw_material_availability_issues', 'fluctuating_operating_results'),
    ('equipment_availability_issues', 'fluctuating_operating_results'),
    ('competitive_developments', 'fluctuating_operating_results'),
    ('pricing_pressures', 'fluctuating_operating_results'),
    ('order_level_fluctuations', 'fluctuating_operating_results'),
    ('sell_through_distribution_levels', 'fluctuating_operating_results'),
    ('customer_order_pattern_changes', 'fluctuating_operating_results'),
    ('seasonality', 'fluctuating_operating_results'),
    ('supplier_constraints_on_customers', 'fluctuating_operating_results'),
    ('tax_audit_costs_outcomes', 'fluctuating_operating_results'),
    ('litigation_costs_outcomes', 'fluctuating_operating_results'),
    ('business_disruptions', 'fluctuating_operating_results'),
    ('uninsured_property_damage_losses', 'fluctuating_operating_results'),
    ('general_economic_conditions', 'fluctuating_operating_results'),
    ('industry_conditions', 'fluctuating_operating_results'),
    ('political_conditions', 'fluctuating_operating_results'),
    ('fluctuating_operating_results', 'potential_results_below_guidance'),
    ('potential_results_below_guidance', 'negative_stock_price_effect'),
    ('ineffective_manufacturing_utilization', 'adverse_operating_results'),
    ('failure_to_maintain_yields', 'adverse_operating_results'),
    ('manufacturing_complexity', 'potential_low_yields'),
    ('contaminants', 'potential_low_yields'),
    ('material_impurities', 'potential_low_yields'),
    ('personnel_performance', 'potential_low_yields'),
    ('equipment_performance', 'potential_low_yields'),
    ('quality_issues', 'potential_low_yields'),
    ('potential_low_yields', 'failure_to_maintain_yields'),
    ('failure_to_maintain_yields', 'revenue_recognition_delays'),
    ('failure_to_maintain_yields', 'loss_of_revenue'),
    ('failure_to_maintain_yields', 'loss_of_future_orders'),
    ('failure_to_maintain_yields', 'customer_penalties'),
    ('low_capacity_utilization', 'ineffective_manufacturing_utilization'),
    ('low_capacity_utilization', 'costs_charged_to_expense'),
    ('low_capacity_utilization', 'lower_gross_margins'),
    ('lower_gross_margins', 'adverse_operating_results'),
    ('dependency_on_turns_orders', 'potential_revenue_shortfall'),
    ('short_lead_times', 'high_percentage_of_turns_orders'),
    ('high_percentage_of_turns_orders', 'reduced_backlog_visibility'),
    ('industry_conditions', 'turns_orders_level'),
    ('difficulty_predicting_turns', 'potential_revenue_shortfall'),
    ('insufficient_turns_orders', 'potential_revenue_shortfall'),
    ('insufficient_turns_orders', 'adverse_operating_results'),
    ('intense_competition', 'pricing_pressures'),
    ('intense_competition', 'reduced_sales'),
    ('intense_competition', 'reduced_market_share'),
    ('intense_competition', 'harm_to_business'),
    ('pricing_pressures', 'adverse_operating_results'),
    ('price_erosion', 'pricing_pressures'),
    ('rapid_technological_change', 'intense_competition'),
    ('inability_to_compete', 'harm_to_business'),
    ('product_quality', 'ability_to_compete'),
    ('product_performance', 'ability_to_compete'),
    ('product_reliability', 'ability_to_compete'),
    ('product_features', 'ability_to_compete'),
    ('ease_of_use', 'ability_to_compete'),
    ('pricing', 'ability_to_compete'),
    ('product_diversity', 'ability_to_compete'),
    ('success_in_new_product_design', 'ability_to_compete'),
    ('rate_of_customer_adoption', 'ability_to_compete'),
    ('competitor_product_introductions', 'inability_to_compete'),
    ('number_nature_success_of_competitors', 'inability_to_compete'),
    ('ability_to_obtain_supplies', 'ability_to_compete'),
    ('ability_to_protect_ip', 'ability_to_compete'),
    ('quality_of_customer_service', 'ability_to_compete'),
    ('general_market_conditions', 'ability_to_compete'),
    ('economic_conditions', 'ability_to_compete'),
    ('average_selling_price_declines', 'adverse_operating_results'),
    ('inability_to_maintain_average_selling_prices', 'adverse_operating_results'),
    ('dependency_on_distributors', 'risk_from_distributor_issues'),
    ('loss_of_distributor', 'reduced_net_sales'),
    ('disruption_in_distributor_operations', 'reduced_net_sales'),
    ('loss_of_distributor', 'increased_inventory_returns'),
    ('disruption_in_distributor_operations', 'increased_inventory_returns'),
    ('distributor_margin_reduction', 'potential_relationship_impact'),
    ('inability_to_introduce_new_products_timely', 'adverse_future_operating_results'),
    ('delays_in_development', 'inability_to_introduce_new_products_timely'),
    ('new_products_lack_market_acceptance', 'adverse_future_operating_results'),
    ('proper_product_selection', 'new_product_success'),
    ('timely_design_completion', 'new_product_success'),
    ('development_of_support_tools', 'new_product_success'),
    ('market_acceptance', 'new_product_success'),
    ('new_product_success', 'positive_operating_results'),
    ('dependency_on_new_tech', 'risk_from_tech_transition_failure'),
    ('delayed_or_inefficient_tech_transition', 'adverse_future_operating_results'),
    ('difficulties_in_tech_transitions', 'reduced_manufacturing_yields'),
    ('difficulties_in_tech_transitions', 'delivery_delays'),
    ('reduced_manufacturing_yields', 'adverse_operating_results'),
    ('dependency_on_qualified_personnel', 'risk_from_personnel_issues'),
    ('loss_of_key_personnel', 'harm_to_business'),
    ('inability_to_attract_key_personnel', 'harm_to_business'),
    ('intense_competition_for_personnel', 'inability_to_attract_key_personnel'),
    ('intense_competition_for_personnel', 'potential_loss_of_key_personnel'),
    ('dependency_on_contractors', 'risk_from_contractor_issues'),
    ('disruption_of_contractor', 'harm_to_business'),
    ('termination_of_contractor', 'harm_to_business'),
    ('contractor_financial_difficulties', 'harm_to_business'),
    ('contractor_operational_difficulties', 'harm_to_business'),
    ('contractor_production_difficulties', 'harm_to_business'),
    ('contractor_demand_exceeds_capacity', 'harm_to_business'),
    ('contractor_unable_to_maintain_yields', 'harm_to_business'),
    ('contractor_unable_to_maintain_costs', 'harm_to_business'),
    ('contractor_political_upheaval', 'harm_to_business'),
    ('contractor_infrastructure_disruption', 'harm_to_business'),
    ('contractor_unwilling_to_deliver', 'harm_to_business'),
    ('contractor_quality_issues', 'harm_to_business'),
    ('contractor_issues', 'interruption_in_production'),
    ('contractor_issues', 'increased_manufacturing_costs'),
    ('contractor_issues', 'decline_in_product_reliability'),
    ('contractor_issues', 'harm_to_business'),
    ('dependency_on_suppliers', 'risk_from_supplier_issues'),
    ('suppliers_fail_to_meet_needs', 'harm_to_business'),
    ('raw_material_shortages', 'harm_to_business'),
    ('equipment_shortages', 'harm_to_business'),
    ('supplier_delays', 'harm_to_business'),
    ('supplier_stops_support', 'harm_to_business'),
    ('interruption_of_raw_material_sources', 'harm_to_business'),
    ('interruption_of_equipment_sources', 'harm_to_business'),
    ('seasonality', 'period_to_period_fluctuations_in_results'),
    ('industry_supply_demand_fluctuations', 'period_to_period_fluctuations_in_results'),
    ('economic_downturns', 'period_to_period_fluctuations_in_results'),
    ('diminished_product_demand', 'period_to_period_fluctuations_in_results'),
    ('production_overcapacity', 'period_to_period_fluctuations_in_results'),
    ('general_industry_conditions', 'period_to_period_fluctuations_in_results'),
    ('general_economic_conditions', 'period_to_period_fluctuations_in_results'),
    ('legal_proceedings', 'substantial_cost'),
    ('legal_proceedings', 'diversion_of_resources'),
    ('patent_infringement_claims', 'potential_legal_harm'),
    ('ip_rights_claims', 'potential_legal_harm'),
    ('contract_claims', 'potential_legal_harm'),
    ('indemnification_claims', 'potential_legal_harm'),
    ('warranty_claims', 'potential_legal_harm'),
    ('product_liability_claims', 'potential_legal_harm'),
    ('potential_legal_harm', 'uninsured_liability'),
    ('potential_legal_harm', 'charge_to_operations'),
    ('potential_legal_harm', 'injunction_on_sales'),
    ('potential_legal_harm', 'injunction_on_processes'),
    ('potential_legal_harm', 'reduction_in_inventory_value'),
    ('potential_legal_harm', 'harm_to_business_financials_operations'),
    ('warranty_claims', 'increased_replacement_costs'),
    ('warranty_claims', 'damages_claims'),
    ('product_liability_claims', 'increased_replacement_costs'),
    ('product_liability_claims', 'damages_claims'),
    ('sales_into_critical_applications', 'increased_product_liability_exposure'),
    ('failure_to_protect_ip', 'lost_revenue'),
    ('failure_to_protect_ip', 'lost_market_opportunities'),
    ('long_expensive_patent_process', 'potential_failure_to_protect_ip'),
    ('patents_not_issued', 'potential_failure_to_protect_ip'),
    ('patents_insufficient_scope_strength', 'potential_failure_to_protect_ip'),
    ('interference_proceedings', 'potential_failure_to_protect_ip'),
    ('weak_foreign_ip_laws', 'potential_failure_to_protect_ip'),
    ('infringement_by_third_parties', 'potential_failure_to_protect_ip'),
    ('no_long_term_contracts', 'uncertainty_in_order_levels'),
    ('cancellation_of_contracts', 'adverse_financial_impact'),
    ('inability_to_supply_customer_under_contract', 'material_adverse_impact'),
    ('manufacturing_facility_disruption', 'harm_to_business'),
    ('subcontractor_facility_disruption', 'harm_to_business'),
    ('work_stoppages', 'potential_facility_disruption'),
    ('power_loss', 'potential_facility_disruption'),
    ('terrorism', 'potential_facility_disruption'),
    ('security_risk', 'potential_facility_disruption'),
    ('political_instability', 'potential_facility_disruption'),
    ('public_health_issues', 'potential_facility_disruption'),
    ('telecom_failure', 'potential_facility_disruption'),
    ('transport_failure', 'potential_facility_disruption'),
    ('infrastructure_failure', 'potential_facility_disruption'),
    ('fire', 'potential_facility_disruption'),
    ('earthquake', 'potential_facility_disruption'),
    ('floods', 'potential_facility_disruption'),
    ('natural_disasters', 'potential_facility_disruption'),
    ('potential_facility_disruption', 'delays_in_shipments'),
    ('potential_facility_disruption', 'reduced_revenues'),
    ('potential_facility_disruption', 'reduced_profits'),
    ('potential_facility_disruption', 'cancellation_of_orders'),
    ('potential_facility_disruption', 'loss_of_customers'),
    ('inadequate_insurance_coverage', 'uncompensated_losses'),
    ('dependency_on_foreign_sales_ops', 'exposure_to_foreign_risks'),
    ('exposure_to_foreign_risks', 'sales_decrease'),
    ('exposure_to_foreign_risks', 'adverse_operating_results'),
    # ('political_instability', 'exposure_to_foreign_risks'), # Already listed above for potential_facility_disruption
    ('social_instability', 'exposure_to_foreign_risks'),
    ('economic_instability', 'exposure_to_foreign_risks'),
    ('public_health_conditions', 'exposure_to_foreign_risks'),
    ('trade_restrictions', 'exposure_to_foreign_risks'),
    ('tariff_changes', 'exposure_to_foreign_risks'),
    ('import_export_license_issues', 'exposure_to_foreign_risks'),
    ('difficulty_staffing_managing_international', 'exposure_to_foreign_risks'),
    ('employment_regulations', 'exposure_to_foreign_risks'),
    ('international_transport_disruptions', 'exposure_to_foreign_risks'),
    ('currency_exchange_rate_fluctuations', 'exposure_to_foreign_risks'),
    ('difficulty_collecting_receivables', 'exposure_to_foreign_risks'),
    ('economic_slowdown_worldwide', 'exposure_to_foreign_risks'),
    ('adverse_tax_consequences', 'exposure_to_foreign_risks'),
    ('dependency_on_it_systems', 'risk_from_it_disruption'),
    ('it_system_disruption', 'adverse_impact_operations'),
    ('it_system_disruption', 'adverse_impact_sales'),
    ('it_system_disruption', 'adverse_impact_results'),
    ('network_disruption', 'adverse_impact_operations'),
    ('computer_viruses', 'potential_it_disruption'),
    ('security_breach', 'potential_it_disruption'),
    ('energy_blackouts', 'potential_it_disruption'),
    ('potential_it_disruption', 'it_system_disruption'),
    ('potential_it_disruption', 'additional_remedy_costs'),
    ('self_insurance_for_risks', 'potential_uncovered_losses'),
    ('loss_in_self_insured_area', 'adverse_financial_effect'),
    ('adverse_judgment_in_self_insured_area', 'adverse_financial_effect'),
    ('failure_to_comply_with_environmental_regs', 'imposition_of_fines'),
    ('failure_to_comply_with_environmental_regs', 'suspension_of_production'),
    ('failure_to_comply_with_environmental_regs', 'cessation_of_operations'),
    ('failure_to_comply_with_environmental_regs', 'future_costs_or_liabilities'),
    ('new_environmental_regs', 'need_to_acquire_costly_equipment'),
    ('need_to_acquire_costly_equipment', 'significant_expenses'),
    ('failure_to_control_hazardous_discharge', 'future_liabilities'),
    ('customer_inability_to_use_non_rohs_products', 'adverse_operating_results'),
    ('compliance_with_securities_laws', 'increased_costs'),
    ('future_changes_in_laws', 'additional_costs'),
    ('discovery_of_material_weaknesses', 'loss_of_investor_confidence'),
    ('loss_of_investor_confidence', 'adverse_stock_price_effect'),
    ('ongoing_sox_404_compliance', 'costly_and_challenging'),
    ('sfas_123r_expensing', 'negatively_impact_earnings'),
    ('changes_in_valuation_assumptions', 'compensation_expense_changes'),
    ('compensation_expense_changes', 'adverse_operating_results'),
    ('difficulty_granting_equity', 'difficulty_attracting_retaining_personnel'),
    ('difficulty_granting_equity', 'increased_compensation_costs'),
    ('difficulty_granting_equity', 'productivity_losses'),
    ('difficulty_attracting_retaining_personnel', 'adverse_effect_on_business'),
    ('quarterly_variations_in_results', 'stock_price_fluctuation'),
    ('competitor_results', 'stock_price_fluctuation'),
    ('tech_innovation_announcements', 'stock_price_fluctuation'),
    ('competitor_product_announcements', 'stock_price_fluctuation'),
    ('analyst_estimate_changes', 'stock_price_fluctuation'),
    ('analyst_recommendation_changes', 'stock_price_fluctuation'),
    ('changes_in_financial_guidance', 'stock_price_fluctuation'),
    ('failure_to_meet_guidance', 'stock_price_fluctuation'),
    ('general_semiconductor_industry_conditions', 'stock_price_fluctuation'),
    ('worldwide_economic_conditions', 'stock_price_fluctuation'),
    ('financial_conditions', 'stock_price_fluctuation'),
    ('broad_market_fluctuations', 'stock_price_fluctuation'),
    ('dependency_on_tax_assessments', 'risk_from_tax_audits'),
    ('adverse_outcomes_from_tax_examinations', 'adverse_operating_results'),
    ('integration_of_acquisitions', 'diversion_of_management_attention'),
    ('integration_of_acquisitions', 'potential_adverse_integration_effects'),
    ('integration_of_acquisitions', 'potential_operational_inefficiencies'),
    ('failure_to_profitably_integrate_acquisition', 'adverse_operating_results')
]

# --- 2. SQLite Database Operations ---
DATABASE_FILE = 'microchip_risks_analysis.sqlite'

def setup_database():
    """Creates the database and the risk_factors table if they don't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_factors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cause TEXT NOT NULL,
                effect TEXT NOT NULL,
                UNIQUE(cause, effect) 
            )
        ''') # UNIQUE constraint prevents duplicate pairs
        conn.commit()
        print(f"Database '{DATABASE_FILE}' setup complete. Table 'risk_factors' is ready.")
    except sqlite3.Error as e:
        print(f"SQLite error during setup: {e}")
    finally:
        if conn:
            conn.close()

def populate_database(risk_data):
    """Populates the risk_factors table with data, ignoring duplicates."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Using INSERT OR IGNORE to avoid errors if a pair already exists due to the UNIQUE constraint
        cursor.executemany('''
            INSERT OR IGNORE INTO risk_factors (cause, effect) VALUES (?, ?)
        ''', risk_data)
        
        conn.commit()
        print(f"Populated 'risk_factors' table with {len(risk_data)} potential entries ({cursor.rowcount} new rows inserted).")
    except sqlite3.Error as e:
        print(f"SQLite error during population: {e}")
    finally:
        if conn:
            conn.close()

def fetch_all_risks_from_db():
    """Fetches all risk factor pairs from the database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT cause, effect FROM risk_factors")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error fetching data: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- 3. NetworkX Graph Operations ---
def build_risk_graph(risk_data):
    """Builds a directed graph from the risk factor data."""
    G = nx.DiGraph()
    for cause, effect in risk_data:
        G.add_edge(cause, effect)
    print(f"Built NetworkX graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

def get_direct_effects(graph, risk_node):
    """Finds direct effects (successors) of a given risk node."""
    if graph.has_node(risk_node):
        return list(graph.successors(risk_node))
    return []

def get_indirect_effects(graph, risk_node):
    """Finds all reachable nodes (indirect effects/transitive closure) from a risk node."""
    if graph.has_node(risk_node):
        return list(nx.descendants(graph, risk_node))
    return []

def get_direct_causes(graph, risk_node):
    """Finds direct causes (predecessors) of a given risk node."""
    if graph.has_node(risk_node):
        return list(graph.predecessors(risk_node))
    return []

def get_indirect_causes(graph, risk_node):
    """Finds all nodes that can reach (indirectly cause) a given risk node."""
    if graph.has_node(risk_node):
        # For indirect causes, we can reverse the graph and find descendants,
        # or find ancestors in the original graph.
        return list(nx.ancestors(graph, risk_node))
    return []

def find_root_causes(graph):
    """Finds nodes with no incoming edges (potential root causes)."""
    return [node for node, in_degree in graph.in_degree() if in_degree == 0]

def find_final_effects(graph):
    """Finds nodes with no outgoing edges (potential final effects)."""
    return [node for node, out_degree in graph.out_degree() if out_degree == 0]

# --- Main Execution ---
if __name__ == "__main__":
    # Step 1: Setup and populate the SQLite database
    setup_database()
    populate_database(microchip_risk_factors)

    # Step 2: Fetch data from DB (optional, could also use original list)
    # For this example, we'll use the original list to build the graph,
    # but in a real application, you might fetch from DB if data changes.
    # risk_data_from_db = fetch_all_risks_from_db()
    
    # Step 3: Build the NetworkX graph
    risk_graph = build_risk_graph(microchip_risk_factors)

    # Step 4: Demonstrate NetworkX queries
    print("\n--- NetworkX Query Examples ---")

    example_cause = 'manufacturing_complexity'
    if risk_graph.has_node(example_cause):
        print(f"\nDirect effects of '{example_cause}':")
        for effect in get_direct_effects(risk_graph, example_cause):
            print(f"  - {effect}")

        print(f"\nIndirect effects (all downstream impacts) of '{example_cause}':")
        indirect_fx = get_indirect_effects(risk_graph, example_cause)
        if indirect_fx:
            for effect in indirect_fx:
                print(f"  - {effect}")
        else:
            print("  (None)")
    else:
        print(f"Node '{example_cause}' not found in the graph.")

    example_effect = 'negative_stock_price_effect'
    if risk_graph.has_node(example_effect):
        print(f"\nDirect causes of '{example_effect}':")
        for cause in get_direct_causes(risk_graph, example_effect):
            print(f"  - {cause}")

        print(f"\nIndirect causes (all upstream contributors) to '{example_effect}':")
        indirect_cz = get_indirect_causes(risk_graph, example_effect)
        if indirect_cz:
            for cause in indirect_cz:
                print(f"  - {cause}")
        else:
            print("  (None)")
    else:
        print(f"Node '{example_effect}' not found in the graph.")

    print("\nPotential Root Causes (risks with no listed antecedents in this dataset):")
    roots = find_root_causes(risk_graph)
    if roots:
        for root in roots:
            print(f"  - {root}")
    else:
        print("  (None or all nodes have causes within the dataset)")


    print("\nPotential Final Effects (risks with no listed consequences in this dataset):")
    finals = find_final_effects(risk_graph)
    if finals:
        for final in finals:
            print(f"  - {final}")
    else:
        print("  (None or all nodes lead to further effects within the dataset)")

    # --- Optional: Visualize the graph (can be very large and cluttered for this dataset) ---
    # Make sure matplotlib is installed: pip install matplotlib
    # For large graphs, visualization might not be very informative without careful layout and filtering.
    # Consider visualizing subgraphs for specific analyses.
    #
    # try:
    #     print("\nAttempting to draw graph (this may take a moment and open a new window)...")
    #     plt.figure(figsize=(20, 20)) # Adjust figure size as needed
    #     # Using a layout that might be better for directed graphs, but still can be dense
    #     pos = nx.spring_layout(risk_graph, k=0.15, iterations=20, seed=42) 
    #     nx.draw(risk_graph, pos, with_labels=True, node_size=50, font_size=8, arrows=True, alpha=0.7, edge_color='gray')
    #     plt.title("Microchip Risk Factor Graph (Simplified Layout)")
    #     # plt.savefig("microchip_risk_graph.png") # Uncomment to save the image
    #     plt.show()
    # except Exception as e:
    #     print(f"Could not draw graph (matplotlib might not be installed or display issue): {e}")
    #     print("To install matplotlib, run: pip install matplotlib")

