""" Number of participants in FJ = 3
Each player comes into FJ with a starting amount X
Giving them a minimum wager of $0 and a max wager of $(x * 2)
Peg the probability of all three contestants at the same likelihood
Or make an approximation to discern each contestant’s likelihood of answering correctly
Give contestants different wagering amounts - maybe enumerate through arrays for each contestant with values of their feasible wager amounts
Run through the simulation n number of times
Record correct or incorrect answers
Wager amount
Winner - any lead changes
Count how often player Y in A, B, C wins and with what wager
"""

# imports

import matplotlib.pyplot as plt
import random

number_of_contestants = 3
number_of_iterations = 100

player_a_start_balance = 1000
player_b_start_balance = 800
player_c_start_balance = 500

player_min_wager = 0

player_a_max_wager = player_a * 2
player_b_max_wager = player_b * 2
player_c_max_wager = player_c * 2

# probability between 0 and 1
culm_probability = 0.75

# all players' wagers = ?

# graph

fig = plt.figure()
fig.title("Final Jeopardy Simulation (" + str(number_of_iterations) + " simulations)")

# simulate x number of times
for i in range(1, number_of_iterations):
    player_a_final_balance = []
    player_b_final_balance = []
    player_c_final_balance = []

    player_a_final_wager = []
    player_b_final_wager = []
    player_c_final_wager = []

    player_a_wins = [0]
    player_b_wins = [0]
    player_c_wins = [0]
    
    player_a_final_wager = round(random.uniform(player_min_wager, player_a_max_wager), 0)


for _ in range(num_of_sims):
    final_scores = []
    for i in range(3):
        random_num = random.random()
        # chance of getting correct answer
        correct = random_num < probabilities[i]
        if correct:
            # add wager
            final_scores.append(starting_scores[i] + wager_scores[i])
        else:
            # deduct wager
            final_scores.append(starting_scores[i] - wager_scores[i])
    highest_score = max(final_scores)
    winner = final_scores.index(highest_score)
    wins[winner] += 1
for i in range(3):
    win_prob = round(wins[i] / num_of_sims, 2) * 100
    player_num = i + 1
    print("Player " + str(player_num) +  " won Final Jeopardy " + str(win_prob) + "% " + "of the time with a wager of $" + str(wager_scores[i])) 