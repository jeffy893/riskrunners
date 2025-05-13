% Load the SQLite3 library
:- use_module(library(sqlite3)).

% --- Database Configuration ---
% Defines the name of the SQLite database file.
database_file('microchip_risks.sqlite'). % Using a .sqlite extension for clarity

% --- Database Setup and Table Creation ---

% Ensures the 'affects' table exists with the correct schema.
% Call this once when setting up or if you suspect the table is missing.
setup_database :-
    database_file(DBFile),
    sqlite_connect(DBFile, DB, [as_predicates(true)]), % Connect or create the DB
    (   catch(sqlite_query(DB, 'SELECT 1 FROM affects LIMIT 1', _), _, fail)
    ->  format('Table "affects" already exists in ~w.~n', [DBFile])
    ;   format('Table "affects" does not exist. Creating it in ~w...~n', [DBFile]),
        sqlite_query(DB,
                     'CREATE TABLE affects (
                         cause TEXT NOT NULL,
                         effect TEXT NOT NULL,
                         PRIMARY KEY (cause, effect)
                      )',
                     _) % The PRIMARY KEY also ensures uniqueness
    ),
    sqlite_disconnect(DB).

% --- Inserting Facts into the Database ---

% Predicate to insert a single affects(Cause, Effect) fact into the SQLite database.
% Uses 'INSERT OR IGNORE' to avoid errors if the fact (primary key) already exists.
insert_affects_fact(DBConnection, Cause, Effect) :-
    sqlite_query(DBConnection,
                 'INSERT OR IGNORE INTO affects (cause, effect) VALUES (:cause, :effect)',
                 [cause(Cause), effect(Effect)]).

% Predicate to populate the database with all Microchip risk factors.
% This should be called after setup_database/0 if the database is new or needs repopulating.
populate_database_with_microchip_facts :-
    database_file(DBFile),
    sqlite_connect(DBFile, DB, []), % Connect to the DB
    format('Populating database ~w with Microchip risk facts...~n', [DBFile]),

    % List all affects/2 facts here
    % (Using a helper predicate to avoid a very long single predicate)
    forall(microchip_fact(Cause, Effect),
           insert_affects_fact(DB, Cause, Effect)),

    sqlite_disconnect(DB),
    format('Finished populating database.~n').

% Define all the Microchip facts.
% This structure makes it easier to manage the list of facts.
microchip_fact(changes_in_demand, fluctuating_operating_results).
microchip_fact(market_acceptance_issues, fluctuating_operating_results).
microchip_fact(customer_inventory_levels, fluctuating_operating_results).
microchip_fact(inventory_mix_issues, fluctuating_operating_results).
microchip_fact(inability_to_satisfy_orders, fluctuating_operating_results).
microchip_fact(manufacturing_capacity_utilization_changes, fluctuating_operating_results).
microchip_fact(manufacturing_yield_fluctuations, fluctuating_operating_results).
microchip_fact(insufficient_assembly_testing_capacity, fluctuating_operating_results).
microchip_fact(raw_material_availability_issues, fluctuating_operating_results).
microchip_fact(equipment_availability_issues, fluctuating_operating_results).
microchip_fact(competitive_developments, fluctuating_operating_results).
microchip_fact(pricing_pressures, fluctuating_operating_results).
microchip_fact(order_level_fluctuations, fluctuating_operating_results).
microchip_fact(sell_through_distribution_levels, fluctuating_operating_results).
microchip_fact(customer_order_pattern_changes, fluctuating_operating_results).
microchip_fact(seasonality, fluctuating_operating_results).
microchip_fact(supplier_constraints_on_customers, fluctuating_operating_results).
microchip_fact(tax_audit_costs_outcomes, fluctuating_operating_results).
microchip_fact(litigation_costs_outcomes, fluctuating_operating_results).
microchip_fact(business_disruptions, fluctuating_operating_results).
microchip_fact(uninsured_property_damage_losses, fluctuating_operating_results).
microchip_fact(general_economic_conditions, fluctuating_operating_results).
microchip_fact(industry_conditions, fluctuating_operating_results).
microchip_fact(political_conditions, fluctuating_operating_results).
microchip_fact(fluctuating_operating_results, potential_results_below_guidance).
microchip_fact(potential_results_below_guidance, negative_stock_price_effect).
microchip_fact(ineffective_manufacturing_utilization, adverse_operating_results).
microchip_fact(failure_to_maintain_yields, adverse_operating_results).
microchip_fact(manufacturing_complexity, potential_low_yields).
microchip_fact(contaminants, potential_low_yields).
microchip_fact(material_impurities, potential_low_yields).
microchip_fact(personnel_performance, potential_low_yields).
microchip_fact(equipment_performance, potential_low_yields).
microchip_fact(quality_issues, potential_low_yields).
microchip_fact(potential_low_yields, failure_to_maintain_yields).
microchip_fact(failure_to_maintain_yields, revenue_recognition_delays).
microchip_fact(failure_to_maintain_yields, loss_of_revenue).
microchip_fact(failure_to_maintain_yields, loss_of_future_orders).
microchip_fact(failure_to_maintain_yields, customer_penalties).
microchip_fact(low_capacity_utilization, ineffective_manufacturing_utilization).
microchip_fact(low_capacity_utilization, costs_charged_to_expense).
microchip_fact(low_capacity_utilization, lower_gross_margins).
microchip_fact(lower_gross_margins, adverse_operating_results).
microchip_fact(dependency_on_turns_orders, potential_revenue_shortfall).
microchip_fact(short_lead_times, high_percentage_of_turns_orders).
microchip_fact(high_percentage_of_turns_orders, reduced_backlog_visibility).
microchip_fact(industry_conditions, turns_orders_level).
microchip_fact(difficulty_predicting_turns, potential_revenue_shortfall).
microchip_fact(insufficient_turns_orders, potential_revenue_shortfall).
microchip_fact(insufficient_turns_orders, adverse_operating_results).
microchip_fact(intense_competition, pricing_pressures).
microchip_fact(intense_competition, reduced_sales).
microchip_fact(intense_competition, reduced_market_share).
microchip_fact(intense_competition, harm_to_business).
microchip_fact(pricing_pressures, adverse_operating_results).
microchip_fact(price_erosion, pricing_pressures).
microchip_fact(rapid_technological_change, intense_competition).
microchip_fact(inability_to_compete, harm_to_business).
microchip_fact(product_quality, ability_to_compete).
microchip_fact(product_performance, ability_to_compete).
microchip_fact(product_reliability, ability_to_compete).
microchip_fact(product_features, ability_to_compete).
microchip_fact(ease_of_use, ability_to_compete).
microchip_fact(pricing, ability_to_compete).
microchip_fact(product_diversity, ability_to_compete).
microchip_fact(success_in_new_product_design, ability_to_compete).
microchip_fact(rate_of_customer_adoption, ability_to_compete).
microchip_fact(competitor_product_introductions, inability_to_compete).
microchip_fact(number_nature_success_of_competitors, inability_to_compete).
microchip_fact(ability_to_obtain_supplies, ability_to_compete).
microchip_fact(ability_to_protect_ip, ability_to_compete).
microchip_fact(quality_of_customer_service, ability_to_compete).
microchip_fact(general_market_conditions, ability_to_compete).
microchip_fact(economic_conditions, ability_to_compete).
microchip_fact(average_selling_price_declines, adverse_operating_results).
microchip_fact(inability_to_maintain_average_selling_prices, adverse_operating_results).
microchip_fact(dependency_on_distributors, risk_from_distributor_issues).
microchip_fact(loss_of_distributor, reduced_net_sales).
microchip_fact(disruption_in_distributor_operations, reduced_net_sales).
microchip_fact(loss_of_distributor, increased_inventory_returns).
microchip_fact(disruption_in_distributor_operations, increased_inventory_returns).
microchip_fact(distributor_margin_reduction, potential_relationship_impact).
microchip_fact(inability_to_introduce_new_products_timely, adverse_future_operating_results).
microchip_fact(delays_in_development, inability_to_introduce_new_products_timely).
microchip_fact(new_products_lack_market_acceptance, adverse_future_operating_results).
microchip_fact(proper_product_selection, new_product_success).
microchip_fact(timely_design_completion, new_product_success).
microchip_fact(development_of_support_tools, new_product_success).
microchip_fact(market_acceptance, new_product_success).
microchip_fact(new_product_success, positive_operating_results).
microchip_fact(dependency_on_new_tech, risk_from_tech_transition_failure).
microchip_fact(delayed_or_inefficient_tech_transition, adverse_future_operating_results).
microchip_fact(difficulties_in_tech_transitions, reduced_manufacturing_yields).
microchip_fact(difficulties_in_tech_transitions, delivery_delays).
microchip_fact(reduced_manufacturing_yields, adverse_operating_results).
microchip_fact(dependency_on_qualified_personnel, risk_from_personnel_issues).
microchip_fact(loss_of_key_personnel, harm_to_business).
microchip_fact(inability_to_attract_key_personnel, harm_to_business).
microchip_fact(intense_competition_for_personnel, inability_to_attract_key_personnel).
microchip_fact(intense_competition_for_personnel, potential_loss_of_key_personnel).
microchip_fact(dependency_on_contractors, risk_from_contractor_issues).
microchip_fact(disruption_of_contractor, harm_to_business).
microchip_fact(termination_of_contractor, harm_to_business).
microchip_fact(contractor_financial_difficulties, harm_to_business).
microchip_fact(contractor_operational_difficulties, harm_to_business).
microchip_fact(contractor_production_difficulties, harm_to_business).
microchip_fact(contractor_demand_exceeds_capacity, harm_to_business).
microchip_fact(contractor_unable_to_maintain_yields, harm_to_business).
microchip_fact(contractor_unable_to_maintain_costs, harm_to_business).
microchip_fact(contractor_political_upheaval, harm_to_business).
microchip_fact(contractor_infrastructure_disruption, harm_to_business).
microchip_fact(contractor_unwilling_to_deliver, harm_to_business).
microchip_fact(contractor_quality_issues, harm_to_business).
microchip_fact(contractor_issues, interruption_in_production).
microchip_fact(contractor_issues, increased_manufacturing_costs).
microchip_fact(contractor_issues, decline_in_product_reliability).
microchip_fact(contractor_issues, harm_to_business).
microchip_fact(dependency_on_suppliers, risk_from_supplier_issues).
microchip_fact(suppliers_fail_to_meet_needs, harm_to_business).
microchip_fact(raw_material_shortages, harm_to_business).
microchip_fact(equipment_shortages, harm_to_business).
microchip_fact(supplier_delays, harm_to_business).
microchip_fact(supplier_stops_support, harm_to_business).
microchip_fact(interruption_of_raw_material_sources, harm_to_business).
microchip_fact(interruption_of_equipment_sources, harm_to_business).
microchip_fact(seasonality, period_to_period_fluctuations_in_results).
microchip_fact(industry_supply_demand_fluctuations, period_to_period_fluctuations_in_results).
microchip_fact(economic_downturns, period_to_period_fluctuations_in_results).
microchip_fact(diminished_product_demand, period_to_period_fluctuations_in_results).
microchip_fact(production_overcapacity, period_to_period_fluctuations_in_results).
microchip_fact(general_industry_conditions, period_to_period_fluctuations_in_results).
microchip_fact(general_economic_conditions, period_to_period_fluctuations_in_results).
microchip_fact(legal_proceedings, substantial_cost).
microchip_fact(legal_proceedings, diversion_of_resources).
microchip_fact(patent_infringement_claims, potential_legal_harm).
microchip_fact(ip_rights_claims, potential_legal_harm).
microchip_fact(contract_claims, potential_legal_harm).
microchip_fact(indemnification_claims, potential_legal_harm).
microchip_fact(warranty_claims, potential_legal_harm).
microchip_fact(product_liability_claims, potential_legal_harm).
microchip_fact(potential_legal_harm, uninsured_liability).
microchip_fact(potential_legal_harm, charge_to_operations).
microchip_fact(potential_legal_harm, injunction_on_sales).
microchip_fact(potential_legal_harm, injunction_on_processes).
microchip_fact(potential_legal_harm, reduction_in_inventory_value).
microchip_fact(potential_legal_harm, harm_to_business_financials_operations).
microchip_fact(warranty_claims, increased_replacement_costs).
microchip_fact(warranty_claims, damages_claims).
microchip_fact(product_liability_claims, increased_replacement_costs).
microchip_fact(product_liability_claims, damages_claims).
microchip_fact(sales_into_critical_applications, increased_product_liability_exposure).
microchip_fact(failure_to_protect_ip, lost_revenue).
microchip_fact(failure_to_protect_ip, lost_market_opportunities).
microchip_fact(long_expensive_patent_process, potential_failure_to_protect_ip).
microchip_fact(patents_not_issued, potential_failure_to_protect_ip).
microchip_fact(patents_insufficient_scope_strength, potential_failure_to_protect_ip).
microchip_fact(interference_proceedings, potential_failure_to_protect_ip).
microchip_fact(weak_foreign_ip_laws, potential_failure_to_protect_ip).
microchip_fact(infringement_by_third_parties, potential_failure_to_protect_ip).
microchip_fact(no_long_term_contracts, uncertainty_in_order_levels).
microchip_fact(cancellation_of_contracts, adverse_financial_impact).
microchip_fact(inability_to_supply_customer_under_contract, material_adverse_impact).
microchip_fact(manufacturing_facility_disruption, harm_to_business).
microchip_fact(subcontractor_facility_disruption, harm_to_business).
microchip_fact(work_stoppages, potential_facility_disruption).
microchip_fact(power_loss, potential_facility_disruption).
microchip_fact(terrorism, potential_facility_disruption).
microchip_fact(security_risk, potential_facility_disruption).
microchip_fact(political_instability, potential_facility_disruption).
microchip_fact(public_health_issues, potential_facility_disruption).
microchip_fact(telecom_failure, potential_facility_disruption).
microchip_fact(transport_failure, potential_facility_disruption).
microchip_fact(infrastructure_failure, potential_facility_disruption).
microchip_fact(fire, potential_facility_disruption).
microchip_fact(earthquake, potential_facility_disruption).
microchip_fact(floods, potential_facility_disruption).
microchip_fact(natural_disasters, potential_facility_disruption).
microchip_fact(potential_facility_disruption, delays_in_shipments).
microchip_fact(potential_facility_disruption, reduced_revenues).
microchip_fact(potential_facility_disruption, reduced_profits).
microchip_fact(potential_facility_disruption, cancellation_of_orders).
microchip_fact(potential_facility_disruption, loss_of_customers).
microchip_fact(inadequate_insurance_coverage, uncompensated_losses).
microchip_fact(dependency_on_foreign_sales_ops, exposure_to_foreign_risks).
microchip_fact(exposure_to_foreign_risks, sales_decrease).
microchip_fact(exposure_to_foreign_risks, adverse_operating_results).
microchip_fact(political_instability, exposure_to_foreign_risks).
microchip_fact(social_instability, exposure_to_foreign_risks).
microchip_fact(economic_instability, exposure_to_foreign_risks).
microchip_fact(public_health_conditions, exposure_to_foreign_risks).
microchip_fact(trade_restrictions, exposure_to_foreign_risks).
microchip_fact(tariff_changes, exposure_to_foreign_risks).
microchip_fact(import_export_license_issues, exposure_to_foreign_risks).
microchip_fact(difficulty_staffing_managing_international, exposure_to_foreign_risks).
microchip_fact(employment_regulations, exposure_to_foreign_risks).
microchip_fact(international_transport_disruptions, exposure_to_foreign_risks).
microchip_fact(currency_exchange_rate_fluctuations, exposure_to_foreign_risks).
microchip_fact(difficulty_collecting_receivables, exposure_to_foreign_risks).
microchip_fact(economic_slowdown_worldwide, exposure_to_foreign_risks).
microchip_fact(adverse_tax_consequences, exposure_to_foreign_risks).
microchip_fact(dependency_on_it_systems, risk_from_it_disruption).
microchip_fact(it_system_disruption, adverse_impact_operations).
microchip_fact(it_system_disruption, adverse_impact_sales).
microchip_fact(it_system_disruption, adverse_impact_results).
microchip_fact(network_disruption, adverse_impact_operations).
microchip_fact(computer_viruses, potential_it_disruption).
microchip_fact(security_breach, potential_it_disruption).
microchip_fact(energy_blackouts, potential_it_disruption).
microchip_fact(potential_it_disruption, it_system_disruption).
microchip_fact(potential_it_disruption, additional_remedy_costs).
microchip_fact(self_insurance_for_risks, potential_uncovered_losses).
microchip_fact(loss_in_self_insured_area, adverse_financial_effect).
microchip_fact(adverse_judgment_in_self_insured_area, adverse_financial_effect).
microchip_fact(failure_to_comply_with_environmental_regs, imposition_of_fines).
microchip_fact(failure_to_comply_with_environmental_regs, suspension_of_production).
microchip_fact(failure_to_comply_with_environmental_regs, cessation_of_operations).
microchip_fact(failure_to_comply_with_environmental_regs, future_costs_or_liabilities).
microchip_fact(new_environmental_regs, need_to_acquire_costly_equipment).
microchip_fact(need_to_acquire_costly_equipment, significant_expenses).
microchip_fact(failure_to_control_hazardous_discharge, future_liabilities).
microchip_fact(customer_inability_to_use_non_rohs_products, adverse_operating_results).
microchip_fact(compliance_with_securities_laws, increased_costs).
microchip_fact(future_changes_in_laws, additional_costs).
microchip_fact(discovery_of_material_weaknesses, loss_of_investor_confidence).
microchip_fact(loss_of_investor_confidence, adverse_stock_price_effect).
microchip_fact(ongoing_sox_404_compliance, costly_and_challenging).
microchip_fact(sfas_123r_expensing, negatively_impact_earnings).
microchip_fact(changes_in_valuation_assumptions, compensation_expense_changes).
microchip_fact(compensation_expense_changes, adverse_operating_results).
microchip_fact(difficulty_granting_equity, difficulty_attracting_retaining_personnel).
microchip_fact(difficulty_granting_equity, increased_compensation_costs).
microchip_fact(difficulty_granting_equity, productivity_losses).
microchip_fact(difficulty_attracting_retaining_personnel, adverse_effect_on_business).
microchip_fact(quarterly_variations_in_results, stock_price_fluctuation).
microchip_fact(competitor_results, stock_price_fluctuation).
microchip_fact(tech_innovation_announcements, stock_price_fluctuation).
microchip_fact(competitor_product_announcements, stock_price_fluctuation).
microchip_fact(analyst_estimate_changes, stock_price_fluctuation).
microchip_fact(analyst_recommendation_changes, stock_price_fluctuation).
microchip_fact(changes_in_financial_guidance, stock_price_fluctuation).
microchip_fact(failure_to_meet_guidance, stock_price_fluctuation).
microchip_fact(general_semiconductor_industry_conditions, stock_price_fluctuation).
microchip_fact(worldwide_economic_conditions, stock_price_fluctuation).
microchip_fact(financial_conditions, stock_price_fluctuation).
microchip_fact(broad_market_fluctuations, stock_price_fluctuation).
microchip_fact(dependency_on_tax_assessments, risk_from_tax_audits).
microchip_fact(adverse_outcomes_from_tax_examinations, adverse_operating_results).
microchip_fact(integration_of_acquisitions, diversion_of_management_attention).
microchip_fact(integration_of_acquisitions, potential_adverse_integration_effects).
microchip_fact(integration_of_acquisitions, potential_operational_inefficiencies).
microchip_fact(failure_to_profitably_integrate_acquisition, adverse_operating_results).

% --- Loading Facts from Database into Prolog's Dynamic Memory ---

% Declare a dynamic predicate to hold facts loaded from the DB.
% This is what your indirectly_affects/2 rule will query.
:- dynamic user:affects_from_db/2.

% Loads all facts from the 'affects' table in SQLite into user:affects_from_db/2.
% Clears any existing user:affects_from_db/2 facts first.
load_affects_from_db :-
    database_file(DBFile),
    sqlite_connect(DBFile, DB, [as_predicates(true)]),
    retractall(user:affects_from_db(_, _)), % Clear previous dynamic facts
    forall(sqlite_query(DB, 'SELECT cause, effect FROM affects', row(Cause, Effect)),
           assertz(user:affects_from_db(Cause, Effect))),
    sqlite_disconnect(DB),
    format('Loaded affects facts from database into dynamic memory.~n').

% --- Querying Logic (using dynamically loaded facts) ---

% Rule for Transitive Effects (Indirect Effects)
% This rule operates on the user:affects_from_db/2 facts loaded from SQLite.
indirectly_affects(X, Y) :- user:affects_from_db(X, Y).
indirectly_affects(X, Y) :- user:affects_from_db(X, Z), indirectly_affects(Z, Y).

% --- HOW TO USE ---
%
% 0. VERY IMPORTANT:
%    a. Ensure this Prolog file (`.pl`) is saved with UTF-8 encoding.
%    b. **DELETE ANY EXISTING `microchip_risks.sqlite` OR `microchip_risks.db` FILE
%       from your working directory before starting a fresh attempt.**
%       This ensures you are starting with a clean slate for the SQLite database.
%
% 1. ENSURE SWI-PROLOG'S CURRENT WORKING DIRECTORY IS WRITABLE:
%    - In Prolog, check current directory:
%      ?- working_directory(CWD, CWD).
%    - If CWD is not writable by your user, change it to a writable path:
%      ?- working_directory(_, '/Users/yourusername/PrologProjects'). % Adjust path
%
% 2. Start SWI-Prolog and CONSULT THIS FILE:
%    ?- ['/path/to/your/microchip_sqlite3_persistence.pl']. % Use the actual full path
%    - Check for any errors during consultation.
%
% 3. SETUP AND POPULATE THE SQLITE DATABASE (run these ONCE for a new database):
%    a. Setup the database and create the table:
%       ?- setup_database.
%       (Should print "Table 'affects' does not exist. Creating it..." or "already exists.")
%    b. Populate the database with facts:
%       ?- populate_database_with_microchip_facts.
%       (Should print "Populating database..." and "Finished populating database.")
%       At this point, 'microchip_risks.sqlite' should be created and populated.
%       You can now open 'microchip_risks.sqlite' with DBeaver or DB Browser for SQLite
%       to inspect the 'affects' table.
%
% 4. LOAD FACTS INTO PROLOG MEMORY FOR QUERYING (run this at the start of each session
%    where you want to query, AFTER the database has been populated):
%    ?- load_affects_from_db.
%    (Should print "Loaded affects facts from database into dynamic memory.")
%
% 5. VERIFY AND QUERY:
%    - To check if facts were loaded into Prolog's dynamic memory:
%      ?- findall((C,E), user:affects_from_db(C,E), AllFacts), length(AllFacts, NumberOfFacts).
%      (Should show a `NumberOfFacts` greater than 0, matching what's in the DB).
%    - Query using the dynamically loaded facts:
%      ?- user:affects_from_db(intense_competition, Consequence).
%      ?- indirectly_affects(Factor, negative_stock_price_effect).
%
% 6. (Optional) Clear dynamic facts if needed (e.g., before reloading):
%    ?- retractall(user:affects_from_db(_, _)).
%
% --- NOTES ---
% - The `microchip_fact/2` predicates are just a way to list your data within the Prolog file.
%   They are used by `populate_database_with_microchip_facts/0`.
% - `setup_database/0` and `populate_database_with_microchip_facts/0` are typically run once
%   to create and fill the SQLite database.
% - `load_affects_from_db/0` is run in each Prolog session where you want to use the
%   `indirectly_affects/2` rule or query `user:affects_from_db/2`.
% - This approach creates a standard SQLite file, fully accessible by external tools.
%
