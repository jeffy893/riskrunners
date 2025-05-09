%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Apartment Corporation Risk Factors (Based on Item 1A)
%
% Predicate: affects(Cause, Effect).
% Meaning: The 'Cause' factor can lead to or contribute to the 'Effect'.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Development, Redevelopment, and Construction Risks
affects(development_redevelopment_construction_activities, exposure_to_development_risks).

affects(inability_to_obtain_permits, increased_costs).
affects(delays_in_obtaining_permits, increased_costs).
affects(inability_to_obtain_permits, delay_of_opportunities).
affects(delays_in_obtaining_permits, delay_of_opportunities).
affects(inability_to_obtain_permits, abandonment_of_opportunities).
affects(delays_in_obtaining_permits, abandonment_of_opportunities).

affects(abandonment_of_explored_opportunities, failure_to_recover_incurred_expenses).
affects(changes_in_local_market_conditions, abandonment_of_explored_opportunities).
affects(increases_in_construction_costs, abandonment_of_explored_opportunities).
affects(increases_in_financing_costs, abandonment_of_explored_opportunities).

affects(costs_exceeding_original_estimates, adverse_impact_on_profitability). % Implied
affects(increased_material_costs, costs_exceeding_original_estimates).
affects(increased_labor_costs, costs_exceeding_original_estimates).
affects(other_increased_costs, costs_exceeding_original_estimates).

affects(occupancy_rates_fail_expectations, adverse_impact_on_profitability). % Implied
affects(rents_fail_expectations, adverse_impact_on_profitability). % Implied
affects(changes_in_market_conditions_beyond_control, occupancy_rates_fail_expectations).
affects(changes_in_economic_conditions_beyond_control, occupancy_rates_fail_expectations).
affects(development_by_competitors, occupancy_rates_fail_expectations).
affects(changes_in_market_conditions_beyond_control, rents_fail_expectations).
affects(changes_in_economic_conditions_beyond_control, rents_fail_expectations).
affects(development_by_competitors, rents_fail_expectations).

affects(inability_to_complete_construction_on_schedule, increased_construction_costs).
affects(inability_to_complete_construction_on_schedule, increased_financing_costs).
affects(inability_to_complete_construction_on_schedule, decrease_in_expected_rental_revenues).
affects(inability_to_complete_lease_up_on_schedule, increased_construction_costs). % Lease-up part
affects(inability_to_complete_lease_up_on_schedule, increased_financing_costs).
affects(inability_to_complete_lease_up_on_schedule, decrease_in_expected_rental_revenues).

affects(inability_to_obtain_financing_favorable_terms, delay_of_opportunity).
affects(inability_to_obtain_financing_favorable_terms, abandonment_of_opportunity).
affects(inability_to_obtain_financing_at_all, delay_of_opportunity).
affects(inability_to_obtain_financing_at_all, abandonment_of_opportunity).

affects(incurring_liabilities_to_third_parties_during_development, direct_financial_liability).
affects(managing_existing_improvements_pre_demolition, incurring_liabilities_to_third_parties_during_development).
affects(providing_services_to_third_parties_shared_infrastructure, incurring_liabilities_to_third_parties_during_development).

affects(noncompliance_with_accessibility_laws, imposition_of_fines).
affects(noncompliance_with_accessibility_laws, award_of_damages_to_litigants).
affects(noncompliance_with_accessibility_laws, requirement_for_structural_modifications).
affects(communities_not_constructed_operated_in_compliance_accessibility, noncompliance_with_accessibility_laws).

affects(increasing_construction_costs_materials, higher_total_construction_costs_than_budget).
affects(redevelopment_costs_exceeding_estimates, potential_future_cost_overruns).
affects(market_rents_insufficient_to_offset_increased_costs, adverse_effect_on_profitability).

%% Unfavorable Market and Economic Conditions
affects(unfavorable_changes_in_market_conditions, hurt_occupancy_rates).
affects(unfavorable_changes_in_market_conditions, hurt_rental_rates).
affects(unfavorable_changes_in_economic_conditions, hurt_occupancy_rates).
affects(unfavorable_changes_in_economic_conditions, hurt_rental_rates).

affects(plant_closings, adverse_effect_on_local_economy).
affects(industry_slowdowns, adverse_effect_on_local_economy).
affects(other_factors_affecting_local_economy, adverse_effect_on_local_economy).
affects(adverse_effect_on_local_economy, adverse_effect_on_market_conditions).

affects(oversupply_of_apartment_homes, adverse_effect_on_market_conditions).
affects(reduced_demand_for_apartment_homes, adverse_effect_on_market_conditions).
affects(decline_in_household_formation, adverse_effect_on_market_conditions).
affects(decline_in_employment, adverse_effect_on_market_conditions).
affects(lack_of_employment_growth, adverse_effect_on_market_conditions).
affects(inability_of_residents_to_pay_rent_increases, adverse_effect_on_market_conditions).
affects(unwillingness_of_residents_to_pay_rent_increases, adverse_effect_on_market_conditions).
affects(rent_control_laws, adverse_effect_on_market_conditions).
affects(rent_stabilization_laws, adverse_effect_on_market_conditions).
affects(other_laws_regulating_housing, adverse_effect_on_market_conditions).
affects(rent_control_laws, prevents_raising_rents_to_offset_costs). % Specific effect

%% Changes in Applicable Laws or Noncompliance
affects(changes_in_applicable_laws, adverse_effect_on_operations).
affects(changes_in_applicable_laws, exposure_to_liability).
affects(noncompliance_with_applicable_laws, adverse_effect_on_operations).
affects(noncompliance_with_applicable_laws, exposure_to_liability).
affects(noncompliance_with_laws, exposure_to_liability). % General statement

affects(changes_in_environmental_laws, lower_revenue_growth).
affects(changes_in_environmental_laws, significant_unanticipated_expenditures).
affects(changes_in_rent_control_stabilization_laws, lower_revenue_growth).
affects(changes_in_rent_control_stabilization_laws, significant_unanticipated_expenditures).
affects(changes_in_other_governmental_rules_regulations, lower_revenue_growth).
affects(changes_in_other_governmental_rules_regulations, significant_unanticipated_expenditures).
affects(changes_in_building_codes, significant_unanticipated_expenditures). % Example of other gov rules
affects(changes_in_fire_life_safety_codes, significant_unanticipated_expenditures). % Example

%% Short-Term Leases
affects(short_term_leases, rental_revenues_impacted_quickly_by_declining_market_rents).

%% Competition
affects(competition_from_other_housing_alternatives, limit_ability_to_lease_apartments).
affects(competition_from_other_housing_alternatives, limit_ability_to_increase_rents).
affects(competition_from_other_housing_alternatives, limit_ability_to_maintain_rents).
affects(competitive_residential_housing, adverse_effect_on_ability_to_lease).
affects(competitive_residential_housing, adverse_effect_on_ability_to_increase_maintain_rates).

%% Availability of Investment Opportunities
affects(competition_from_other_real_estate_investors, increased_prices_for_properties).
affects(increased_prices_for_properties, adverse_effect_on_profitability).
affects(attractive_investment_opportunities_unavailable, adverse_effect_on_profitability).

%% Insufficient Cash Flow and Debt Financing
affects(insufficient_cash_flow, inability_to_meet_required_payments_of_principal_interest).
affects(reit_dividend_distribution_requirement, limits_cash_flow_for_debt_payments).
affects(unamortized_debt_principal_at_maturity, need_to_refinance_debt).
affects(inability_to_refinance_existing_debt, material_adverse_effect_on_financial_condition).
affects(inability_to_refinance_existing_debt, material_adverse_effect_on_results_of_operations).
affects(refinancing_on_unfavorable_terms, material_adverse_effect_on_financial_condition).
affects(refinancing_on_unfavorable_terms, material_adverse_effect_on_results_of_operations).

%% Rising Interest Rates
affects(rising_interest_rates_with_variable_debt, increased_interest_costs).
affects(increase_in_market_interest_rates, purchasers_demand_greater_annual_dividend_yield).
affects(purchasers_demand_greater_annual_dividend_yield, adverse_effect_on_common_stock_market_price).

%% Bond Financing and Zoning Compliance
affects(tax_exempt_bond_income_restrictions, limit_ability_to_raise_rents_aggressively).
affects(tax_exempt_bond_income_restrictions, limit_increases_in_community_value).
affects(zoning_compliance_income_restrictions, limit_ability_to_raise_rents_aggressively). % Similar effect for zoning
affects(zoning_compliance_income_restrictions, limit_increases_in_community_value).
affects(financial_institution_defaults_on_bond_guarantee, default_under_tax_exempt_bonds).
affects(inability_to_renew_bond_guarantee, default_under_tax_exempt_bonds).
affects(default_under_tax_exempt_bonds, community_could_be_foreclosed_upon).

%% Risks Related to Indebtedness (General)
affects(credit_facility_dividend_restrictions, limits_dividends_over_95_percent_ffo_unless_reit_qualification).
affects(no_organizational_limit_on_debt_incurrence, potential_for_more_debt).
affects(potential_for_more_debt, increased_risk_of_default_on_obligations).
affects(potential_for_more_debt, increase_in_debt_service_requirements).
affects(increase_in_debt_service_requirements, adverse_effect_on_financial_condition).
affects(increase_in_debt_service_requirements, adverse_effect_on_results_of_operations).
affects(debt_covenant_restrictions, limit_flexibility).
affects(default_in_debt_covenants_uncured, requirement_to_repay_indebtedness).
affects(requirement_to_repay_indebtedness, severely_affect_liquidity).
affects(requirement_to_repay_indebtedness, increase_financing_costs).

%% Failure to Generate Sufficient Revenue
affects(decrease_in_rental_revenue, adverse_effect_on_ability_to_pay_distributions).
affects(decrease_in_rental_revenue, adverse_effect_on_ability_to_maintain_reit_status).
affects(fixed_community_expenditures_not_reduced_with_income_reduction, pressure_on_cash_flow).

%% Availability of Debt and Equity Financing
affects(debt_financing_unavailable, impacts_business_strategy_execution).
affects(debt_financing_on_unfavorable_terms, impacts_business_strategy_execution).
affects(issuing_additional_equity_securities, dilution_to_existing_stockholders).

%% Difficulty Selling Apartment Communities
affects(tax_laws_limiting_gain_on_sale_if_held_for_resale, affects_ability_to_sell_communities_profitably).
affects(real_estate_hard_to_sell_in_poor_market, limits_ability_to_change_portfolio_promptly).
affects(potential_difficulties_in_selling_real_estate, limits_ability_to_change_portfolio_promptly).

%% Acquisitions Not Yielding Anticipated Results
affects(acquired_property_fails_to_perform_as_expected, negative_acquisition_results).
affects(inaccurate_estimate_of_repositioning_costs, negative_acquisition_results).
affects(inaccurate_estimate_of_redeveloping_costs, negative_acquisition_results).
affects(acquisitions_not_yield_anticipated_results, adverse_consequences). % General

%% Failure to Succeed in New Markets or Other Activities
affects(commencing_activity_outside_existing_markets, exposure_to_new_market_risks).
affects(historical_experience_not_ensure_success_in_new_markets, risk_of_failure_in_new_markets).
affects(historical_experience_not_ensure_success_in_other_activities, risk_of_failure_in_other_activities).
affects(inability_to_evaluate_local_market_conditions, risk_factor_for_new_markets).
affects(inability_to_obtain_land_for_development_in_new_markets, risk_factor_for_new_markets).
affects(inability_to_identify_acquisition_opportunities_in_new_markets, risk_factor_for_new_markets).
affects(inability_to_hire_retain_key_personnel_in_new_markets, risk_factor_for_new_markets).
affects(lack_of_familiarity_with_local_procedures_in_new_markets, risk_factor_for_new_markets).
affects(unsuccessful_in_owning_operating_retail_space, adverse_consequences).
affects(unsuccessful_in_developing_real_estate_for_sale, adverse_consequences).

%% Real Estate Activity Through Joint Ventures
affects(joint_venture_investments, exposure_to_jv_risks).
affects(jv_partner_insolvency, jv_investment_risk).
affects(jv_partner_refuses_capital_contributions, jv_investment_risk).
affects(responsible_for_jv_partner_indemnifiable_losses, jv_investment_risk).
affects(jv_partner_inconsistent_business_goals, jv_investment_risk).
affects(jv_partner_action_contrary_to_requests, jv_investment_risk).
affects(jv_buy_sell_arrangement_trigger, forced_sale_or_acquisition_at_inopportune_time).

%% Risks Associated with Discretionary Investment Fund
affects(investment_in_discretionary_fund, exposure_to_fund_risks).
affects(fund_investors_fail_capital_contributions, fund_unable_to_execute_investment_objectives).
affects(general_partner_subsidiary_liable_for_fund_debts, liability_risk_for_company).
affects(removal_as_general_partner_by_fund_investors, loss_of_management_fees).
affects(removal_as_general_partner_by_fund_investors, potential_forced_property_acquisition).
affects(fund_investor_approval_needed_for_certain_matters, unable_to_implement_beneficial_decisions).
affects(prohibition_on_acquisitions_outside_fund, limits_company_acquisition_activity).
affects(liability_if_fund_or_its_reit_fails_tax_regulatory_compliance, liability_risk_for_company).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Rule for Transitive Effects (Indirect Effects)
% indirectly_affects(X, Y) is true if X affects Y directly,
% or if X affects some Z which directly or indirectly affects Y.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

indirectly_affects(X, Y) :- affects(X, Y).
indirectly_affects(X, Y) :- affects(X, Z), indirectly_affects(Z, Y).

