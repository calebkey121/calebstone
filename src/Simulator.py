# output_file = open("RandomRun/meta", "w+")
#                 
# output_file.write(f"Win Rate Caleb: {(win1 / numRuns) * 100}%")
# output_file.write(f"First Rate Caleb: {(p1First / numRuns) * 100}%")
# output_file.write(f"Win Rate Dio: {(win2 / numRuns) * 100}%")
# output_file.write(f"First Rate Dio: {(p2First / numRuns) * 100}%")
# output_file.write(f"Tie Rate: {(ties / numRuns) * 100}%")

from src.GameManager import GameManager
from src.GameLogger import GameLogger

def run_simulation(num_games: int = 1000):
    logger = GameLogger(log_file="simulation_results.jsonl")
    
    for _ in range(num_games):
        GameManager(logger=logger)  # Same logger for all games
    
    # Get statistics across all games
    stats = logger.get_summary_stats()
    print(stats)

def main():
    NUM_GAMES = 1000
    print(f"Running simulation with {NUM_GAMES} games...")
    
    run_simulation(NUM_GAMES)

if __name__ == "__main__":
    main()