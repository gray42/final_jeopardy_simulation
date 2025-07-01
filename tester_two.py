# inputs:
    # starting amount 
    # wager amount 
    # chance at correct answer
    # number of simulations

# outputs:
    # number of rounds each player wins
    # overall winner
    # optimal wager amount

import random

def finalJeopardySim(starting_scores, probabilities, num_of_sims=1000000):
    num_of_players = 3

    # assign possible wagers with increments of 100
    possible_wagers = [list(range(0, score + 1, 100)) for score in starting_scores]

    # initialize empty arrays for optimal wagers and probabilities for each player
    best_wager = [0] * num_of_players
    best_win_prob = [0.0] * num_of_players

    # loop through for each player
    for i in range(num_of_players):
        # test possible wagers for player i
        for wager in possible_wagers:
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
                    delta = wager if correct else -wager
                    # compute final score for given player and add to array
                    final_scores[j] += delta
                
                # does player i win? yes if he has the max score and it is unique
                if final_scores[i] == max(final_scores) and final_scores.count(final_scores[i]) == 1:
                    wins += 1

        # decided best wager
        win_prob = wins / num_of_sims
        if win_prob > best_win_prob[i]:
            best_win_prob[i] = win_prob
            best_wager[i] = wager

    return best_wager, best_win_prob

starting_scores = [1000, 800, 500]
probabilities = [0.8, 0.6, 0.7]

wagers, probs = finalJeopardySim(starting_scores, probabilities)

for i in range(len(starting_scores)):
    print(f"Player {i + 1}'s optimal wager: {wagers[i]} with an expected win probability of {probs[i]}%")
