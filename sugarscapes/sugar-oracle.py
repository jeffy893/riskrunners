import random
import csv
import math
import time # Import time module to estimate runtime

# --- Simulation Parameters to Vary ---
# Expanded lists for more data points
PEOPLE_VALUES = [50, 100, 250, 500, 750, 1000, 1500, 2000, 3000, 5000] # More values and higher max
MAX_VISITS_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # More granular visits up to 10

# --- Fixed Simulation Constants ---
SIMULATION_YEARS = 10
VISIT_COST = 1.0
# ASSUMPTION: Probability of diagnosis per person per quarter check
P_DIAGNOSIS_PER_QUARTER = 0.005
POLICY_MAX_VISITS = 1 # Max visits per month in the 3 months prior for coverage
OUTPUT_CSV_FILE = 'simulation_results_with_id.csv' # Updated filename

def run_simulation(num_people, max_visits_per_month):
    """
    Runs a single simulation instance with given parameters.

    Args:
        num_people (int): Number of people in this simulation run.
        max_visits_per_month (int): Maximum random visits per person per month.

    Returns:
        dict: A dictionary containing the key results of the simulation.
    """
    simulation_months = SIMULATION_YEARS * 12

    # --- Data Structure for People ---
    people = []
    for i in range(num_people):
        people.append({
            "id": i,
            "monthly_visit_history": [0] * simulation_months,
            "has_diabetes": False,
            "is_covered": False, # Is insurance covering future visits?
            "diagnosis_month": -1
        })

    # --- Simulation Run ---
    total_insured_cost = 0.0

    for month in range(simulation_months):
        # 1. Simulate Monthly Visits
        for person in people:
            visits_this_month = random.randint(0, max_visits_per_month)
            if month < len(person["monthly_visit_history"]):
                 person["monthly_visit_history"][month] = visits_this_month
            else:
                 print(f"Warning: Month index {month} out of bounds for person {person['id']}")
                 continue

            if person["has_diabetes"] and person["is_covered"]:
                total_insured_cost += visits_this_month * VISIT_COST

        # 2. Perform Quarterly Checks
        if (month + 1) >= 3 and (month + 1) % 3 == 0:
            for person in people:
                if not person["has_diabetes"]:
                    if random.random() < P_DIAGNOSIS_PER_QUARTER:
                        person["has_diabetes"] = True
                        person["diagnosis_month"] = month

                        if month >= 2:
                            visits_m3 = person["monthly_visit_history"][month - 2]
                            visits_m2 = person["monthly_visit_history"][month - 1]
                            visits_m1 = person["monthly_visit_history"][month]

                            if (visits_m1 <= POLICY_MAX_VISITS and
                                visits_m2 <= POLICY_MAX_VISITS and
                                visits_m3 <= POLICY_MAX_VISITS):
                                person["is_covered"] = True
                            else:
                                person["is_covered"] = False
                        else:
                             person["is_covered"] = False


    # --- Calculate Premiums ---
    num_diagnosed = sum(1 for p in people if p["has_diabetes"])
    num_covered = sum(1 for p in people if p["is_covered"])

    if SIMULATION_YEARS > 0 and num_people > 0:
        average_annual_cost_pool = total_insured_cost / SIMULATION_YEARS
        annual_premium_per_person = average_annual_cost_pool / num_people
        monthly_premium_per_person = annual_premium_per_person / 12.0
    else:
        # Handle edge case where num_people is 0, although unlikely with current PEOPLE_VALUES
        annual_premium_per_person = 0.0
        monthly_premium_per_person = 0.0

    # --- Return Results ---
    # Note: simulation_id is added in the main loop now
    return {
        "num_people": num_people,
        "max_visits_per_month": max_visits_per_month,
        "num_diagnosed": num_diagnosed,
        "num_covered": num_covered,
        "total_insured_cost": total_insured_cost,
        "annual_premium_per_person": annual_premium_per_person,
        "monthly_premium_per_person": monthly_premium_per_person
    }

# --- Main Execution Logic ---
all_results = []
start_time = time.time() # Record start time

total_simulations = len(PEOPLE_VALUES) * len(MAX_VISITS_VALUES)
print(f"Starting simulations... Expecting {total_simulations} combinations.")
print("NOTE: This may take a significant amount of time depending on your hardware.")

current_simulation = 0 # Initialize counter outside the loops
# Loop through all combinations of parameters
for num_p in PEOPLE_VALUES:
    for max_v in MAX_VISITS_VALUES:
        current_simulation += 1 # Increment simulation ID for each run
        run_start_time = time.time()
        print(f"  ({current_simulation}/{total_simulations}) Running simulation with: NUM_PEOPLE={num_p}, MAX_VISITS_PER_MONTH={max_v}")

        # Run the simulation
        results = run_simulation(num_p, max_v)

        # Add the simulation ID to the results dictionary
        results['simulation_id'] = current_simulation

        # Store the complete results
        all_results.append(results)

        run_end_time = time.time()
        # Display results (cost formatting done later for CSV)
        print(f"    -> Completed in {run_end_time - run_start_time:.2f} seconds. Diagnosed: {results['num_diagnosed']}, Covered: {results['num_covered']}, Total Cost: ${results['total_insured_cost']:.2f}")


end_time = time.time() # Record end time
print(f"\nAll simulations complete. Total execution time: {end_time - start_time:.2f} seconds.")

# --- Write Results to CSV ---
if all_results:
    # Explicitly define column order with simulation_id first
    csv_columns = [
        'simulation_id',
        'num_people',
        'max_visits_per_month',
        'num_diagnosed',
        'num_covered',
        'total_insured_cost',
        'annual_premium_per_person',
        'monthly_premium_per_person'
    ]

    try:
        with open(OUTPUT_CSV_FILE, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in all_results:
                 # Format currency fields before writing
                 data['total_insured_cost'] = f"{data['total_insured_cost']:.2f}"
                 data['annual_premium_per_person'] = f"{data['annual_premium_per_person']:.2f}"
                 data['monthly_premium_per_person'] = f"{data['monthly_premium_per_person']:.2f}"
                 writer.writerow(data)
        print(f"\nResults successfully written to {OUTPUT_CSV_FILE}")
    except IOError:
        print(f"Error: Could not write to CSV file {OUTPUT_CSV_FILE}")
    except Exception as e:
        print(f"An unexpected error occurred during CSV writing: {e}")
else:
    print("No simulation results generated to write to CSV.")