# output_file = open("RandomRun/meta", "w+")
#                 
# output_file.write(f"Win Rate Caleb: {(win1 / numRuns) * 100}%")
# output_file.write(f"First Rate Caleb: {(p1First / numRuns) * 100}%")
# output_file.write(f"Win Rate Dio: {(win2 / numRuns) * 100}%")
# output_file.write(f"First Rate Dio: {(p2First / numRuns) * 100}%")
# output_file.write(f"Tie Rate: {(ties / numRuns) * 100}%")

from GameManager import GameManager
from GameState import GameResult
from dataclasses import dataclass

@dataclass
class GameStats:
    total_games: int = 0
    first_player_wins: int = 0
    second_player_wins: int = 0
    ties: int = 0
    
    @property
    def first_player_winrate(self) -> float:
        return (self.first_player_wins / self.total_games * 100) if self.total_games > 0 else 0
    
    @property
    def second_player_winrate(self) -> float:
        return (self.second_player_wins / self.total_games * 100) if self.total_games > 0 else 0
    
    @property
    def tie_rate(self) -> float:
        return (self.ties / self.total_games * 100) if self.total_games > 0 else 0


def run_simulation(num_games: int = 1000) -> GameStats:
    stats = GameStats()
    
    for _ in range(num_games):
        game = GameManager()
        game.run_game()
        result = game.game_state.get_result()
        stats.total_games += 1
        
        if result == GameResult.TIE:
            stats.ties += 1
        else:
            # Check if first player won
            first_player = game.game_state.who_went_first
            is_first_player_win = (
                (result == GameResult.PLAYER1_WIN and first_player == game.game_state.player1) or
                (result == GameResult.PLAYER2_WIN and first_player == game.game_state.player2)
            )
            
            if is_first_player_win:
                stats.first_player_wins += 1
            else:
                stats.second_player_wins += 1
    
    return stats

def print_stats(stats: GameStats) -> None:
    print(f"\nGame Statistics (Total Games: {stats.total_games})")
    print("-" * 50)
    print(f"First Player Win Rate:  {stats.first_player_winrate:.1f}%")
    print(f"Second Player Win Rate: {stats.second_player_winrate:.1f}%")
    print(f"Tie Rate:              {stats.tie_rate:.1f}%")

def save_stats(stats: GameStats, filename: str = "simulation_results.txt") -> None:
    with open(filename, "w") as f:
        f.write("Game Simulation Results\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Total Games: {stats.total_games}\n")
        f.write(f"First Player Wins: {stats.first_player_wins} ({stats.first_player_winrate:.1f}%)\n")
        f.write(f"Second Player Wins: {stats.second_player_wins} ({stats.second_player_winrate:.1f}%)\n")
        f.write(f"Ties: {stats.ties} ({stats.tie_rate:.1f}%)\n")

def main():
    NUM_GAMES = 1000
    print(f"Running simulation with {NUM_GAMES} games...")
    
    stats = run_simulation(NUM_GAMES)
    print_stats(stats)
    save_stats(stats)

if __name__ == "__main__":
    main()