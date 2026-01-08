### Date
## 2025-05-05
### Company
# Imperial Oil LTD

## Takeaways
- Canadian Greenhouse Gas Regulation has limited the value of oil companies
- When sourcing crude / hard oil, the refinery is expensive
- Public sentiment about consumption of oil in Canada impacts...

### Hypothesis
## Do canadians on average prefer electric vehicles to gasoline vehicles?


```sql
?- indirectly_affects(Factor, adverse_effect_on_financial_condition).
Factor = material_price_decline ;
Factor = increased_operating_costs ;
Factor = increased_capital_expenditures ;
Factor = changes_in_environmental_legislation ;
Factor = changes_in_environmental_legislation ;
Factor = potential_federal_ghg_regulations ;
Factor = potential_federal_ghg_regulations ;
Factor = potential_provincial_ghg_regulations ;
Factor = potential_provincial_ghg_regulations ;
Factor = mandatory_emission_limits ;
Factor = mandatory_emission_limits ;
false.

?- affects(material_price_decline, Consequence).
Consequence = adverse_effect_on_operations ;
Consequence = adverse_effect_on_financial_condition ;
Consequence = adverse_effect_on_proven_reserves ;
Consequence = adverse_effect_on_development_spending.

?- indirectly_affects(environmental_regulation, Effect).
Effect = restrictions_liabilities_obligations ;
Effect = requirements_for_hazardous_substance_handling ;
Effect = requirements_for_waste_disposal ;
Effect = liability_for_spills_releases_emissions ;
Effect = requirements_for_product_composition ;
Effect = requirements_for_site_reclamation ;
Effect = requirements_for_environmental_impact_assessments ;
false.

?- affects(Factor, inherent_uncertainties_in_reserve_estimation).
Factor = geological_engineering_estimate_uncertainty ;
Factor = assumed_effects_of_regulation ;
Factor = future_commodity_prices ;
Factor = future_operating_costs.

?- (affects(mandatory_emission_limits, Effect); affects(Effect, adverse_effect_on_business)).
Effect = increased_operating_costs ;
Effect = increased_capital_expenditures ;
Effect = reduced_demand_for_products ;
Effect = increases_in_heavy_oil_differentials ;
Effect = reduced_demand_for_products.


?- indirectly_affects(Factor, decline_in_reserves_production).
true.

?- affects(Factor, project_issues).
Factor = inability_to_obtain_regulatory_approvals ;
Factor = changes_in_resource_costs ;
Factor = changes_in_operating_costs ;
Factor = availability_of_materials_equipment_personnel ;
Factor = cost_of_materials_equipment_personnel ;
Factor = general_economic_conditions ;
Factor = business_market_conditions ;
Factor = unforeseen_technical_difficulties.

?- (affects(Factor, Effect), (sub_atom(Factor, _, _, _, heavy_oil); sub_atom(Effect, _, _, _, heavy_oil))).
Factor = heavy_oil_production,
Effect = dependency_on_heavy_oil_differentials .

?- ffects(Factor, interruption_of_operations).
Correct to: "affects(Factor,interruption_of_operations)"? yes
Factor = operational_hazard_events.
```