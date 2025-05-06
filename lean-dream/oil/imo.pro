%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Imperial Oil Ltd. Risk Factors (Based on Item 1A)
%
% Predicate: affects(Cause, Effect).
% Meaning: The 'Cause' factor can lead to or contribute to the 'Effect'.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Oil and Natural Gas Price Volatility
affects(oil_natural_gas_price_volatility, dependency_of_results_on_prices).
affects(global_market_conditions, oil_natural_gas_prices).
affects(north_american_market_conditions, oil_natural_gas_prices).
affects(supply_demand_conditions, oil_natural_gas_prices).
affects(economic_conditions, supply_demand_conditions).
affects(international_political_developments, supply_demand_conditions).
affects(weather, supply_demand_conditions).

affects(material_price_decline, adverse_effect_on_operations).
affects(material_price_decline, adverse_effect_on_financial_condition).
affects(material_price_decline, adverse_effect_on_proven_reserves).
affects(material_price_decline, adverse_effect_on_development_spending).

% Heavy Oil Specifics
affects(heavy_oil_production, dependency_on_heavy_oil_differentials).
affects(higher_transportation_costs_heavy_oil, lower_price_for_heavy_oil).
affects(higher_refining_costs_heavy_oil, lower_price_for_heavy_oil).
affects(limited_heavy_oil_refining_capacity, lower_price_for_heavy_oil).
affects(lower_price_for_heavy_oil, lower_revenue_compared_to_light_oil). % Implied
affects(higher_production_costs_heavy_oil, lower_profitability_compared_to_light_oil). % Implied
affects(uncertain_future_differentials, potential_adverse_effect_on_business).
affects(increases_in_heavy_oil_differentials, adverse_effect_on_business).

% Hedging Policy
% Note: This is a statement of policy, not a direct cause-effect risk in the same way.
% Could be represented differently, e.g., policy(no_hedging).
% For consistency, we can model the *lack* of hedging as a condition:
condition(no_hedging_of_production).

%% Competitive Factors
affects(high_competition_oil_gas_industry, potential_negative_impact).
affects(competition_for_supply_sources, potential_negative_impact).
affects(competition_for_infrastructure, potential_negative_impact).
affects(competition_for_refining_distribution_marketing, potential_negative_impact).
affects(competition_with_other_energy_industries, potential_negative_impact).

affects(competitive_forces, shortages_of_drilling_prospects).
affects(competitive_forces, shortages_of_services).
affects(competitive_forces, shortages_of_infrastructure).
affects(competitive_forces, oversupply_of_crude_oil).
affects(competitive_forces, oversupply_of_natural_gas).
affects(competitive_forces, oversupply_of_petroleum_products).
affects(competitive_forces, oversupply_of_chemicals).

affects(shortages_of_drilling_prospects, negative_impact_on_costs_prices).
affects(shortages_of_services, negative_impact_on_costs_prices).
affects(shortages_of_infrastructure, negative_impact_on_costs_prices).
affects(oversupply_of_crude_oil, negative_impact_on_costs_prices).
affects(oversupply_of_natural_gas, negative_impact_on_costs_prices).
affects(oversupply_of_petroleum_products, negative_impact_on_costs_prices).
affects(oversupply_of_chemicals, negative_impact_on_costs_prices).

affects(negative_impact_on_costs_prices, adverse_financial_results). % Renamed for clarity

%% Environmental Risks
affects(environmental_regulation, restrictions_liabilities_obligations).
affects(environmental_regulation, requirements_for_hazardous_substance_handling).
affects(environmental_regulation, requirements_for_waste_disposal).
affects(environmental_regulation, liability_for_spills_releases_emissions).
affects(environmental_regulation, requirements_for_product_composition).
affects(environmental_regulation, requirements_for_site_reclamation).
affects(environmental_regulation, requirements_for_environmental_impact_assessments).

affects(compliance_with_environmental_legislation, significant_expenditures).
affects(failure_to_comply_with_environmental_legislation, imposition_of_fines_penalties).
affects(failure_to_comply_with_environmental_legislation, liability_for_cleanup_costs).
affects(failure_to_comply_with_environmental_legislation, liability_for_damages).

affects(future_costs_of_compliance, potential_adverse_effect_on_financial_condition). % Uncertainty expressed
affects(future_costs_of_compliance, potential_adverse_effect_on_operations_results). % Uncertainty expressed

affects(changes_in_environmental_legislation, required_emission_reductions).
affects(changes_in_environmental_legislation, increased_capital_expenditures).
affects(changes_in_environmental_legislation, stricter_standards_enforcement).
affects(changes_in_environmental_legislation, larger_fines_liability).
affects(changes_in_environmental_legislation, increased_operating_costs).
affects(increased_capital_expenditures, potential_adverse_effect_on_financial_condition).
affects(increased_operating_costs, potential_adverse_effect_on_operations_results).

%% Kyoto Protocol / Climate Change Regulations
affects(kyoto_protocol_ratification, potential_greenhouse_gas_regulations).
affects(potential_federal_ghg_regulations, mandatory_emission_limits).
affects(potential_provincial_ghg_regulations, mandatory_emission_limits). % e.g., Alberta

affects(mandatory_emission_limits, increased_operating_costs).
affects(mandatory_emission_limits, increased_capital_expenditures).
affects(mandatory_emission_limits, reduced_demand_for_products).
affects(reduced_demand_for_products, adverse_effect_on_business).
affects(increased_operating_costs, adverse_effect_on_financial_condition). % Linking back
affects(increased_capital_expenditures, adverse_effect_on_financial_condition). % Linking back
affects(increased_operating_costs, adverse_effect_on_operations_results). % Linking back

% Uncertainty about specific measures
condition(uncertainty_about_specific_ghg_measures).
affects(uncertainty_about_specific_ghg_measures, speculative_impact_assessment).

%% Other Regulatory Risk
affects(changes_in_legislation_regulation, potential_impact_on_operations).
affects(changes_in_legislation_regulation, potential_impact_on_financial_performance).

%% Need to Replace Reserves
affects(dependency_on_reserve_replacement, risk_to_future_production_cash_flows).
affects(reserve_depletion, decline_in_reserves_production_without_additions).
affects(capital_intensive_nature_of_reserve_replacement, dependency_on_cash_flow_capital).
affects(insufficient_cash_flow, impaired_ability_for_capital_investment).
affects(limited_external_capital, impaired_ability_for_capital_investment).
affects(impaired_ability_for_capital_investment, inability_to_maintain_expand_reserves).
affects(inability_to_find_develop_acquire_reserves_at_acceptable_costs, decline_in_reserves_production).

%% Other Business Risks (Operational Hazards)
affects(inherent_risks_in_exploration_production_transport, potential_operational_hazards).
affects(potential_operational_hazards, fires).
affects(potential_operational_hazards, explosions).
affects(potential_operational_hazards, spills).
affects(potential_operational_hazards, blow_outs).
affects(potential_operational_hazards, other_dangerous_conditions).

affects(operational_hazard_events, personal_injury).
affects(operational_hazard_events, property_damage).
affects(operational_hazard_events, environmental_damage).
affects(operational_hazard_events, interruption_of_operations).
affects(inadequate_insurance_coverage, uncovered_losses_from_hazards).

%% Uncertainty of Reserve Estimates
affects(inherent_uncertainties_in_reserve_estimation, potential_variance_from_actual).
affects(geological_engineering_estimate_uncertainty, inherent_uncertainties_in_reserve_estimation).
affects(assumed_effects_of_regulation, inherent_uncertainties_in_reserve_estimation).
affects(future_commodity_prices, inherent_uncertainties_in_reserve_estimation). % As estimate inputs
affects(future_operating_costs, inherent_uncertainties_in_reserve_estimation). % As estimate inputs

affects(variance_in_estimates, material_difference_in_actual_production).
affects(variance_in_estimates, material_difference_in_actual_revenues).
affects(variance_in_estimates, material_difference_in_actual_taxes).
affects(variance_in_estimates, material_difference_in_actual_expenditures).

affects(estimates_based_on_volumetric_analogy, less_reliable_estimates).
affects(less_reliable_estimates, potential_material_variations_upon_production_history).

%% Project Factors
affects(dependency_on_major_projects, risk_from_project_issues).
affects(events_affecting_project_advancement, adverse_effect_on_results).
affects(events_affecting_project_operation, adverse_effect_on_results).
affects(events_affecting_project_cost, adverse_effect_on_results).
affects(events_affecting_project_results, adverse_effect_on_results).

affects(inability_to_obtain_regulatory_approvals, project_issues).
affects(changes_in_resource_costs, project_issues).
affects(changes_in_operating_costs, project_issues).
affects(availability_of_materials_equipment_personnel, project_issues). % Lack thereof
affects(cost_of_materials_equipment_personnel, project_issues). % High cost
affects(general_economic_conditions, project_issues). % Impact on projects
affects(business_market_conditions, project_issues). % Impact on projects
affects(unforeseen_technical_difficulties, project_issues).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Rule for Transitive Effects (Indirect Effects)
% indirectly_affects(X, Y) is true if X affects Y directly,
% or if X affects some Z which directly or indirectly affects Y.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

indirectly_affects(X, Y) :- affects(X, Y).
indirectly_affects(X, Y) :- affects(X, Z), indirectly_affects(Z, Y).

