# inputs:
    # starting scores for each player 
    # probabilities of each player getting the answer correct
    # number of simulations
    # number of iterations to run the simulation

# outputs:
    # optimal wagers for each player
    # and their win probabilities

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

random.seed(42)  # For reproducibility

def finalJeopardySim(starting_scores, probabilities, num_of_sims=50000, iterations=10):
    num_of_players = len(starting_scores)
    # assign possible wagers with increments of ?
    wager_increments = 50
    possible_wagers = [list(range(0, score + 1, wager_increments)) for score in starting_scores]
    # initialize empty arrays for optimal wagers and probabilities for each player
    starting_wagers = [starting_scores[i] // 2 for i in range(num_of_players)]
    # a player's best win probability
    best_win_probs = [0.0] * num_of_players

    win_prob_history = [[] for _ in range(num_of_players)]
    wager_space = possible_wagers

    # loop through for iterations
    for iteration in range(iterations):
        new_wagers = starting_wagers[:]
        # for each player, find the best wager given the current wagers of the other players
        for i in range(num_of_players):
            player_best_wager = 0
            player_best_win_prob = 0.0
            win_probs_for_plot = []
            # test possible wagers for player i
            for wager in possible_wagers[i]:
                wins = 0
                # test num_of_sims times
                for _ in range(num_of_sims):
                    # copy starting_scores array to final_scores
                    final_scores = starting_scores[:]

                    # determine win probs for each player
                    for j in range(num_of_players):
                        correct = random.random() < probabilities[j]
                        # either add or subtract wager based on if correct
                        delta = (wager if correct else -wager) if j == i else \
                                 (starting_wagers[j] if correct else -starting_scores[j])
                        # compute final score for given player and add to array
                        final_scores[j] += delta
                    # does player i win? yes if he has the max score and it is unique
                    if final_scores[i] == max(final_scores) and final_scores.count(final_scores[i]) == 1:
                        wins += 1

                # decide best wager
                win_prob = wins / num_of_sims
                win_probs_for_plot.append(win_prob)

                if win_prob > player_best_win_prob:
                    player_best_win_prob = win_prob
                    player_best_wager = wager

            # store best wager and win probability for player i
            new_wagers[i] = player_best_wager
            best_win_probs[i] = player_best_win_prob
            win_prob_history[i].append((possible_wagers[i], win_probs_for_plot))
        
        # update wagers after all players have chose best response (if same, then break)
        if new_wagers == starting_wagers:
            break

        starting_wagers = new_wagers[:]

    return starting_wagers, best_win_probs, win_prob_history

starting_scores = [1000, 800, 700]
probabilities = [0.6, 1, 0.7]

optimal_wagers, win_probs, history = finalJeopardySim(starting_scores, probabilities)

for i, (wager, win_prob) in enumerate(zip(optimal_wagers, win_probs)):
    print(f"Player {i + 1}'s optimal wager: {wager} (Win probability: {win_prob * 100:.2f}%)")


def plot_win_probs(history):
    for i, player_data in enumerate(history):
        last_iter = player_data[-1]  # Only plot last iteration
        x_vals, y_vals = last_iter
        plt.plot(x_vals, y_vals, label=f'Player {i + 1}')
    
    plt.xlabel("Wager Amount")
    plt.ylabel("Win Probability")
    plt.title("Final Jeopardy: Win Probabilities vs. Wager Amounts")
    plt.legend()
    plt.grid(True)
    plt.show()

def print_optimal_table(optimal_wagers, win_probs):
    df = pd.DataFrame({
        'Player': [f'Player {i + 1}' for i in range(len(optimal_wagers))],
        'Optimal Wager': optimal_wagers,
        'Win Probability': [f"{p * 100:.2f}%" for p in win_probs]
    })
    print(df)

print_optimal_table(optimal_wagers, win_probs)
plot_win_probs(history)
