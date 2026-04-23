import csv
import random
import statistics
from datetime import datetime

from game import Game
from agent import Agent


def run_single_game(weights=None, seed=None):
    if seed is not None:
        random.seed(seed)

    game = Game()
    agent = Agent(weights)

    pieces_played = 0

    while not game.game_over:
        moved = agent.run_game(game)
        if not moved:
            break
        pieces_played += 1

    return {
        "score": game.score,
        "pieces_played": pieces_played
    }


def run_benchmark(num_runs=10, weights=None, save_csv=True):
    results = []

    for run_number in range(1, num_runs + 1):
        result = run_single_game(weights=weights, seed=run_number)
        result["run"] = run_number
        results.append(result)

    scores = [r["score"] for r in results]
    pieces = [r["pieces_played"] for r in results]

    best_run = max(results, key=lambda r: r["score"])
    worst_run = min(results, key=lambda r: r["score"])

    print("\n=== Tetris AI Benchmark Results ===")
    print(f"Runs: {num_runs}")
    print(f"Scores: {scores}")
    print(f"Best Score: {best_run['score']} (Run {best_run['run']})")
    print(f"Worst Score: {worst_run['score']} (Run {worst_run['run']})")
    print(f"Average Score: {statistics.mean(scores):.2f}")
    print(f"Median Score: {statistics.median(scores):.2f}")
    print(f"Average Pieces Placed: {statistics.mean(pieces):.2f}")

    if save_csv:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_results_{timestamp}.csv"

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["run", "score", "pieces_played"])

            for r in results:
                writer.writerow([r["run"], r["score"], r["pieces_played"]])

            writer.writerow([])
            writer.writerow(["best_score", best_run["score"]])
            writer.writerow(["worst_score", worst_run["score"]])
            writer.writerow(["average_score", f"{statistics.mean(scores):.2f}"])
            writer.writerow(["median_score", f"{statistics.median(scores):.2f}"])
            writer.writerow(["average_pieces_played", f"{statistics.mean(pieces):.2f}"])

        print(f"Saved results to {filename}")

    return results


if __name__ == "__main__":
    run_benchmark(num_runs=10)
