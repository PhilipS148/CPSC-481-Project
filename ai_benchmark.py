import csv
import random
import statistics
from datetime import datetime

from game import Game
from agent import Agent
from config import DEFAULT_WEIGHTS

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

# can change weight preset in config file later
def run_benchmark(num_runs=10, weights= DEFAULT_WEIGHTS , save_csv=True):
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


#below is function to try and find more 'optimal' weight values, since before was just random choice, function is sort of based off run_benchmark() above

def optimal_weight_search(num_trials = 10, runs_per_trial = 10, save_csv=True):
    best_weights = None
    best_avg_score = float("-inf")
    best_avg_pieces = 0
    trial_results = []


    #below is just assigning random weights (between two values) per run to find best ones

    for trial in range(1, num_trials + 1):
        weights = [
            random.uniform(0.5,3.0), #lines
            random.uniform(-2, -0.1), #agg height
            random.uniform(-4,-0.5), #holes
            random.uniform(-2.0, -0.5), #bumpiness
            random.uniform(-3.0, -0.2), #max height
        ]
    
        results = run_benchmark(num_runs=runs_per_trial, weights=weights, save_csv=False)

        #reads results and interprets like function above
        scores = [r["score"] for r in results]
        pieces = [r["pieces_played"] for r in results]

        avg_score = statistics.mean(scores)
        avg_pieces = statistics.mean(pieces)

        trial_results.append({
            "trial": trial,
            "weights": weights,
            "average_score": avg_score,
            "average_pieces": avg_pieces
        })


        print(f"\nTrial {trial}/{num_trials}")
        print(f"Weights: {[round(w, 3) for w in weights]}")
        print(f"Average Score: {avg_score:.2f}")
        print(f"Average Pieces: {avg_pieces:.2f}")
        print(f"============ End of Trial: {trial} ============")

        if avg_score > best_avg_score:
            best_avg_score = avg_score
            best_avg_pieces = avg_pieces
            best_weights = weights

    print(f"\n=== Optimal Weights from Trials ===")
    print(f"Best Weights = {[round(b, 3) for b in best_weights]}")
    print(f"Best Average Score from Trials: {best_avg_score:.2f}")
    print(f"Best Average Pieces Played from Trials: {best_avg_pieces:.2f}")


    if save_csv:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weight_search_results_{timestamp}.csv"

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "trial",
                "lines_weight",
                "height_weight",
                "holes_weight",
                "bumpiness_weight",
                "max_height_weight",
                "average_score",
                "average_pieces"
            ])

            for r in trial_results:
                w = r["weights"]
                writer.writerow([
                    r["trial"],
                    round(w[0], 4),
                    round(w[1], 4),
                    round(w[2], 4),
                    round(w[3], 4),
                    round(w[4], 4),
                    round(r["average_score"], 2),
                    round(r["average_pieces"], 2)
                ])

            writer.writerow([])
            writer.writerow(["BEST_WEIGHTS"])
            writer.writerow([
                "lines",
                "height",
                "holes",
                "bumpiness",
                "max_height"
            ])
            writer.writerow([round(w, 4) for w in best_weights])
            writer.writerow(["best_average_score", round(best_avg_score, 2)])
            writer.writerow(["best_average_pieces", round(best_avg_pieces, 2)])

        print(f"Saved weight search results to {filename}")

if __name__ == "__main__":
    optimal_weight_search(num_trials=5, runs_per_trial=10, save_csv=True)
