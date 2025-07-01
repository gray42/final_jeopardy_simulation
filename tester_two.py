# inputs:
    # starting scores for each player 
    # probabilities of each player getting the answer correct
    # number of simulations
    # number of iterations to run the simulation

# outputs:
    # optimal wagers for each player
    # and their win probabilities

import random

random.seed(42)  # For reproducibility

def finalJeopardySim(starting_scores, probabilities, num_of_sims=5000, iterations=10):
    num_of_players = len(starting_scores)
    # assign possible wagers with increments of ?
    possible_wagers = [list(range(0, score + 1, 10)) for score in starting_scores]
    # initialize empty arrays for optimal wagers and probabilities for each player
    starting_wagers = [starting_scores[i] // 2 for i in range(num_of_players)]
    # a player's best win probability
    best_win_probs = [0.0] * num_of_players

    # loop through for iterations
    for iteration in range(iterations):
        new_wagers = starting_wagers[:]
        # for each player
        for i in range(num_of_players):
            player_best_wager = 0
            player_best_win_prob = 0.0
            # test possible wagers for player i
            for wager in possible_wagers[i]:
                wins = 0
                # test num_of_sims times
                for _ in range(num_of_sims):
                    # copy starting_scores array to final_scores
                    final_scores = starting_scores[:]

                    # determine win probs for each player
                    for j in range(num_of_players):
                        # chance of getting answer correct
                        correct = random.random() < probabilities[j] 
                        # either add or subtract wager based on if correct
                        if j == i:
                            delta = wager if correct else -wager
                        else:
                            delta = new_wagers[j]
                            delta = delta if correct else -delta
                        # compute final score for given player and add to array
                        final_scores[j] += delta
                    # does player i win? yes if he has the max score and it is unique
                    if final_scores[i] == max(final_scores) and final_scores.count(final_scores[i]) == 1:
                        wins += 1
                # decide best wager
                win_prob = wins / num_of_sims
                if win_prob > player_best_win_prob:
                    player_best_win_prob = win_prob
                    player_best_wager = wager
            # update new wagers and best win probabilities for player i
            new_wagers[i] = player_best_wager
            best_win_probs[i] = player_best_win_prob
        
        if new_wagers == starting_wagers:
            break
        starting_wagers = new_wagers.copy()

    return starting_wagers, best_win_probs

starting_scores = [1000, 800, 500]
probabilities = [0.8, 0.6, 0.7]

optimal_wagers, win_probs = finalJeopardySim(starting_scores, probabilities)

for i, (wager, win_prob) in enumerate(zip(optimal_wagers, win_probs)):
    print(f"Player {i + 1}'s optimal wager: {wager} (Win probability: {win_prob * 100:.2f}%)")
