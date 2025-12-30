import pandas as pd
import random
import itertools
from tqdm import tqdm

# --- Simulation Parameters ---
NUM_SIMULATIONS = 50         # Number of entire leagues to simulate.
NUM_PLAYERS = 24             # Total players in the league (must be a multiple of 4).
NUM_MATCHES = 6              # Number of matches each player plays.
WINNING_SCORE = 11           # Score to win a game.
BONUS_POINTS_SCENARIOS = [0, 1, 2, 3, 4] # Bonus points to test.

def simulate_game(player1, player2, player3, player4):
    """Simulates a single game of pickleball between two teams."""
    team1_skill = player1['skill'] + player2['skill']
    team2_skill = player3['skill'] + player4['skill']
    total_skill = team1_skill + team2_skill

    if total_skill == 0: # Avoid division by zero
        return 0, 0

    team1_win_prob = team1_skill / total_skill

    team1_score, team2_score = 0, 0
    while team1_score < WINNING_SCORE and team2_score < WINNING_SCORE:
        if random.random() < team1_win_prob:
            team1_score += 1
        else:
            team2_score += 1
    
    return team1_score, team2_score

def run_simulation(sim_id):
    """Runs a full league simulation for one set of players."""
    # 1. Create players with a range of skill levels
    players = [{'id': i, 'skill': random.randint(50, 100)} for i in range(NUM_PLAYERS)]
    
    # Data structure to hold player stats for this simulation
    player_stats = {p['id']: {'wins': 0, 'points_for': 0, 'skill': p['skill']} for p in players}

    # 2. Simulate the ladder league over 6 matches
    for match_num in range(NUM_MATCHES):
        # Sort players by total points to create courts (ladder format)
        # On the first match, the sorting is random.
        if match_num > 0:
            sorted_players = sorted(players, key=lambda p: player_stats[p['id']]['points_for'], reverse=True)
        else:
            random.shuffle(players)
            sorted_players = players

        # Create courts of 4 players
        for i in range(0, NUM_PLAYERS, 4):
            court_players = sorted_players[i:i+4]
            
            # Define the 3 unique pairings for a round robin
            pairings = [
                ((court_players[0], court_players[1]), (court_players[2], court_players[3])),
                ((court_players[0], court_players[2]), (court_players[1], court_players[3])),
                ((court_players[0], court_players[3]), (court_players[1], court_players[2]))
            ]
            
            # Each pair plays twice (6 games total per match)
            for (p1, p2), (p3, p4) in pairings * 2:
                team1_score, team2_score = simulate_game(p1, p2, p3, p4)

                # Update stats
                player_stats[p1['id']]['points_for'] += team1_score
                player_stats[p2['id']]['points_for'] += team1_score
                player_stats[p3['id']]['points_for'] += team2_score
                player_stats[p4['id']]['points_for'] += team2_score

                if team1_score > team2_score:
                    player_stats[p1['id']]['wins'] += 1
                    player_stats[p2['id']]['wins'] += 1
                else:
                    player_stats[p3['id']]['wins'] += 1
                    player_stats[p4['id']]['wins'] += 1

    # 3. Compile results for this simulation
    results = []
    for player_id, stats in player_stats.items():
        result_row = {
            'simulation_id': sim_id,
            'player_id': player_id,
            'player_skill': stats['skill'],
            'total_wins': stats['wins'],
            'total_points_raw': stats['points_for']
        }
        # Calculate final score for each bonus scenario
        for bonus in BONUS_POINTS_SCENARIOS:
            result_row[f'final_score_bonus_{bonus}'] = stats['points_for'] + (stats['wins'] * bonus)
        results.append(result_row)
        
    return results

# --- Main Execution ---
if __name__ == "__main__":
    print("Running Pickleball Ladder League Simulations...")
    all_results = []
    for i in tqdm(range(NUM_SIMULATIONS), desc="Simulating Leagues"):
        sim_results = run_simulation(i)
        all_results.extend(sim_results)

    df = pd.DataFrame(all_results)

    # Calculate ranks for each scoring method within each simulation
    for bonus in BONUS_POINTS_SCENARIOS:
        df[f'rank_bonus_{bonus}'] = df.groupby('simulation_id')[f'final_score_bonus_{bonus}'].rank(method='first', ascending=False)
    
    # Calculate the "true" rank based on skill
    df['rank_skill'] = df.groupby('simulation_id')['player_skill'].rank(method='first', ascending=False)
    
    # Save to CSV
    output_filename = 'pickleball_league_simulation_results.csv'
    df.to_csv(output_filename, index=False)
    
    print(f"\nSimulation complete. Data saved to '{output_filename}'")