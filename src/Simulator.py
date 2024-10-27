from src.GameManager import GameManager
from src.GameLogger import GameLogger
from pprint import pprint

def run_simulation(num_games: int = 1000):
    logger = GameLogger(log_file="simulation_results.jsonl")
    
    for _ in range(num_games):
        GameManager(logger=logger)  # Same logger for all games
    
    # Get statistics across all games
    stats = logger.get_summary_stats()
    pprint(stats)

def main():
    NUM_GAMES = 1000
    print(f"Running simulation with {NUM_GAMES} games...")
    
    run_simulation(NUM_GAMES)

if __name__ == "__main__":
    main()