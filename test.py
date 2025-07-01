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