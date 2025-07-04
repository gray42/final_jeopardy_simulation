# inputs:
    # starting scores for each player 
    # probabilities of each player getting the answer correct
    # number of simulations
    # number of iterations to run the simulation

# outputs:
    # optimal wagers for each player
    # and their win probabilities

import random
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from strengths_and_weaknesses import get_probabilities

random.seed(42)  # For reproducibility

def finalJeopardySim(starting_scores, probabilities, wager_increments, num_of_sims=10000, iterations=20, ):
    num_of_players = len(starting_scores)

    # starting wagers
    def get_starting_wagers(score, position, starting_scores):
        sorted_scores = sorted(starting_scores, reverse=True)
        first_place = sorted_scores[0]
        second_place = sorted_scores[1]
        # if you are leader
        if position == 0:
            # bet enough to cover the second place player doubling up
            return min(score, max(0, 2 * second_place - score))
        # else if you are trailing
        else:
            # when trailing, wager enough to to catch up to leader if they answer wrong
            return min(score, max(0, 2 * first_place - score))

    # initialize starting wagers
    starting_wagers = []
    for i, score in enumerate(starting_scores):
        # sort players by score so that the highest score is first
        # range(len(starting_scores)) gives indices of players, while lambda function sorts in reverse order
        position = sorted(range(len(starting_scores)), key=lambda x: starting_scores[x], reverse=True).index(i)
        # get starting wager and append to list
        starting_wager = get_starting_wagers(score, position, starting_scores)
        starting_wagers.append(starting_wager)

    # a player's best win probability
    best_win_probs = [0.0] * num_of_players

    # track wager history for iterations
    convergence_history = []
    # Factor to prevent oscillation in wagers
    dampening_factor = 0.7  

    print(f"Initial wagers: {starting_wagers}")

    # loop through for iterations
    for iteration in tqdm(range(iterations)):
        # initialize old, new wagers and win probabilities
        old_wagers = starting_wagers[:]
        new_wagers = starting_wagers[:]
        iteration_win_probs = []

        heatmap = [[] for _ in range(num_of_players)]
        wager_range = [[] for _ in range(num_of_players)]

        # simulate each player
        for i in range(num_of_players):
            # rebuild possible wagers for each player
            player_score = starting_scores[i]

            strategic_wager = get_strategic_wagers(
                player_score, starting_scores, starting_wagers, i, increment=wager_increments)

            # initialize best wager and win probability for player i
            best_wager = starting_wagers[i]
            best_win_prob = 0.0

            player_wager_win_probs = []

            # test possible wagers for player i
            for wager in strategic_wager:
                wins = 0
                ties = 0

                #  calculate final scores for every player
                for _ in range(num_of_sims):
                    final_scores = []
                    # determine win probs for each player
                    for j in range(num_of_players):
                        correct = random.random() < probabilities[j]
                        player_wager = wager if j == i else starting_wagers[j]
                        if correct:
                            final_scores.append(starting_scores[j] + player_wager)
                        else:
                            final_scores.append(starting_scores[j] - player_wager)
                    
                    max_score = max(final_scores)   
                    # get index of winner(s)
                    winners = [i for i, score in enumerate(final_scores) if score == max_score]
                    # solo winner
                    if len(winners) == 1:
                        if winners[0] == i:
                            wins += 1
                    else:
                        # tie break - split win probabilities
                        if i in winners:
                            wins += 1 / len(winners)
                        ties += 1

                # calculate win probability for this wager
                win_prob = wins / num_of_sims
                player_wager_win_probs.append((wager, win_prob))
                # if this wager gives a better win probability, update best wager and win prob
                if win_prob > best_win_prob:
                    best_win_prob = win_prob
                    best_wager = wager
            # update wagers and win probabilities for heatmap of player i
            wagers, win_probs_for_player = zip(*player_wager_win_probs)
            wager_range[i] = list(wagers)
            heatmap[i] = list(win_probs_for_player)
            
            # Apply dampening to prevent oscillation
            if iteration > 0:
                # calculate a weighted average of best wager and previous wager using dampening factor
                new_wagers[i] = int(dampening_factor * best_wager + (1 - dampening_factor) * starting_wagers[i])
            else:
                # first time use best wager
                new_wagers[i] = best_wager
            # append player's best win prob for iteration
            iteration_win_probs.append(best_win_prob)
        # update starting wagers/win probs with wagers/win probs found from this iteration
        starting_wagers = new_wagers
        best_win_probs = iteration_win_probs
        # record wager history for convergence analysis
        convergence_history.append(starting_wagers[:])
        
        # Print current iteration results
        print(f"Iteration {iteration+1}: Wagers = {starting_wagers}, Win Probs = {[f'{p:.3f}' for p in best_win_probs]}")
        
        # Check for convergence (less strict to allow for minor fluctuations)
        if iteration > 0:
            # calculate change for new vs old wagers
            wager_changes = [abs(new_wagers[i] - old_wagers[i]) for i in range(num_of_players)]
            # check if all of the changes are within the wager increment - then wager has converged
            if all(change <= wager_increments for change in wager_changes):
                print(f"Converged after {iteration+1} iterations.")
                break

    return starting_wagers, best_win_probs, convergence_history, wager_range, heatmap

def get_strategic_wagers(player_score, all_scores, starting_wagers, i, increment=50):
    wagers = set()
    wagers.add(0)
    wagers.add(player_score)

    # get starting wager and then calculate nearby wagers
    current = starting_wagers[i]
    for x in [-2*increment, -increment, 0, increment, 2*increment]:
       wager = current + x
       if 0 <= wager <= player_score:
        wagers.add(wager)

    # loop through opponents' scores and wagers to come up with strategic wagers
    for j, (score, wager) in enumerate(zip(all_scores, starting_wagers)):
        # skip current player
        if j == i:
            continue
            
        # minimum amount to wager to beat opponent's score given they answer correctly
        target_to_beat_correct = score + wager - player_score
        if 0 <= target_to_beat_correct <= player_score:
            # wager = just enough
            wagers.add(target_to_beat_correct)
            # wager = just enough + padding
            wagers.add(min(player_score, target_to_beat_correct + increment))
        
         # minimum amount to wager to beat opponent's score given they answer incorrectly 
        target_to_beat_wrong = score - wager - player_score
        if 0 <= target_to_beat_wrong <= player_score:
            wagers.add(target_to_beat_wrong)
            wagers.add(min(player_score, target_to_beat_wrong + increment))
        
        # "Forrest Bounce" - wager to tie if both wrong
        tie_wager = player_score - score + wager
        if 0 <= tie_wager <= player_score:
            wagers.add(tie_wager)
    
    # add regular wagers in increments to list
    
    wagers.update(range(0, player_score + 1, increment))
    valid_wagers = sorted({int(w) for w in wagers if w >= 0 and w <= player_score})
    
    return valid_wagers

# LOOK INTO VISUALS MORE 
def plot_convergence(history, starting_scores):
    history = np.array(history)
    x = np.arange(history.shape[0])
    plt.figure(figsize=(12, 6))
    # plot each player's wager history
    for i in range(history.shape[1]):
        plt.plot(x, history[:, i], label=f"Player {i+1} (Start: ${starting_scores[i]})")
    plt.xlabel("Iteration")
    plt.ylabel("Wager Amount")
    plt.title("Convergence of Wagers Over Iterations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_heatmap(player_index, wager_range, win_probs):
    plt.figure(figsize=(8, 5))
    plt.scatter(wager_range, win_probs, c=win_probs, cmap='viridis', s=100, edgecolor='k')
    plt.colorbar(label="Win Probability")
    plt.xlabel("Wager")
    plt.ylabel("Win Probability")
    plt.title(f"Player {player_index+1}: Win Probability vs Wager")
    plt.grid(True)
    plt.show()

def plot_final_win_probs(win_probs, wager):
    plt.figure(figsize=(8, 5))
    players = [f'Player {i+1}' for i in range(len(win_probs))]
    plt.bar(players, win_probs, color='skyblue')
    plt.ylim(0, 1)
    plt.ylabel("Win Probability")
    plt.title("Final Win Probabilities")
    for i, prob in enumerate(win_probs):
        plt.text(i, prob + 0.02, f"{prob:.2%}", ha='center')
        plt.text(i, 0.01, f"Wager: ${wager[i]}", ha='center', fontsize=9, color='darkgreen')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()



if __name__ == "__main__":
    # TEST CASE 1
    print("\n===================== TEST CASE 1 =====================")
    starting_scores = [1000, 800, 700]
    #probabilities = [0.65, 0.70, 0.60] 
    probabilities = get_probabilities()  
    print(f"Probabilities: {probabilities}")

    optimal_wagers, win_probs, history, wager_range, heatmap = finalJeopardySim(
        starting_scores, probabilities, 
        num_of_sims=20000,  
        iterations=15,
        wager_increments=100
    )

    # Display results
    print("\n=== TEST CASE 1 RESULTS ===")
    df = pd.DataFrame({
        'Player': [f'Player {i + 1}' for i in range(len(optimal_wagers))],
        'Starting Score': [f'${score:,}' for score in starting_scores],
        'Probability Correct': [f'{p:.1%}' for p in probabilities],
        'Optimal Wager': [f'${wager:,}' for wager in optimal_wagers],
        'Win Probability': [f'{p:.1%}' for p in win_probs]
    })
    print(df.to_string(index=False))

    # call visuals
    plot_final_win_probs(win_probs, optimal_wagers)
    for i in range(len(starting_scores)):
        plot_heatmap(i, wager_range[i], heatmap[i])
    plot_convergence(history, starting_scores)

    # TEST CASE 2
    print("\n===================== TEST CASE 2 =====================")
    starting_scores = [1200, 1300, 650]
    probabilities = [0.75, 0.50, 0.90] 

    optimal_wagers, win_probs, history, wager_range, heatmap = finalJeopardySim(
        starting_scores, probabilities, 
        num_of_sims=20000,  
        iterations=15,
        wager_increments=100
    )

    # Display results
    print("\n=== TEST CASE 2 RESULTS ===")
    df = pd.DataFrame({
        'Player': [f'Player {i + 1}' for i in range(len(optimal_wagers))],
        'Starting Score': [f'${score:,}' for score in starting_scores],
        'Probability Correct': [f'{p:.1%}' for p in probabilities],
        'Optimal Wager': [f'${wager:,}' for wager in optimal_wagers],
        'Win Probability': [f'{p:.1%}' for p in win_probs]
    })
    print(df.to_string(index=False))
    plot_convergence(history, starting_scores)

    # TEST CASE 3
    print("\n===================== TEST CASE 3 - LOCK GAME =====================")
    starting_scores = [1300, 600, 500]
    probabilities = [0.75, 0.50, 0.90] 

    optimal_wagers, win_probs, history, wager_range, heatmap = finalJeopardySim(
        starting_scores, probabilities, 
        num_of_sims=20000,  
        iterations=15,
        wager_increments=100
    )

    # Display results
    print("\n=== TEST CASE 3 - LOCK GAME RESULTS ===")
    df = pd.DataFrame({
        'Player': [f'Player {i + 1}' for i in range(len(optimal_wagers))],
        'Starting Score': [f'${score:,}' for score in starting_scores],
        'Probability Correct': [f'{p:.1%}' for p in probabilities],
        'Optimal Wager': [f'${wager:,}' for wager in optimal_wagers],
        'Win Probability': [f'{p:.1%}' for p in win_probs]
    })
    print(df.to_string(index=False))
    plot_convergence(history, starting_scores)

    # TEST CASE 4
    print("\n===================== TEST CASE 4 - LOCK TIE GAME =====================")
    starting_scores = [1200, 600, 500]
    probabilities = [0.75, 0.50, 0.90] 

    optimal_wagers, win_probs, history, wager_range, heatmap = finalJeopardySim(
        starting_scores, probabilities, 
        num_of_sims=20000,  
        iterations=15,
        wager_increments=100
    )

    # Display results
    print("\n=== TEST CASE 4 - LOCK TIE GAME RESULTS ===")
    df = pd.DataFrame({
        'Player': [f'Player {i + 1}' for i in range(len(optimal_wagers))],
        'Starting Score': [f'${score:,}' for score in starting_scores],
        'Probability Correct': [f'{p:.1%}' for p in probabilities],
        'Optimal Wager': [f'${wager:,}' for wager in optimal_wagers],
        'Win Probability': [f'{p:.1%}' for p in win_probs]
    })
    print(df.to_string(index=False))
    plot_convergence(history, starting_scores)

    # TEST CASE 5
    print("\n===================== TEST CASE 5 - Two-Thirds Game & Three-Quarters Game =====================")
    starting_scores = [1600, 1300, 900]
    probabilities = [0.75, 0.60, 0.90] 

    optimal_wagers, win_probs, history, wager_range, heatmap = finalJeopardySim(
        starting_scores, probabilities, 
        num_of_sims=20000,  
        iterations=15,
        wager_increments=100
    )

    # Display results
    print("\n===================== TEST CASE 5 - Two-Thirds Game & Three-Quarters Game =====================")
    df = pd.DataFrame({
        'Player': [f'Player {i + 1}' for i in range(len(optimal_wagers))],
        'Starting Score': [f'${score:,}' for score in starting_scores],
        'Probability Correct': [f'{p:.1%}' for p in probabilities],
        'Optimal Wager': [f'${wager:,}' for wager in optimal_wagers],
        'Win Probability': [f'{p:.1%}' for p in win_probs]
    })
    print(df.to_string(index=False))
    plot_convergence(history, starting_scores)


