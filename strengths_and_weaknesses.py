#!/usr/bin/env python3
import identifier
import random
import sys

# — Prompt each player for a base probability (0.0–1.0) —
def read_prob(name):
    while True:
        try:
            v = float(input(f"Enter base probability for {name} (0 to 1): ").strip())
            if 0.0 <= v <= 1.0:
                return v
        except ValueError:
            pass
        print("  ❗ Please enter a number between 0 and 1.")

# Get strengths
PlayerA = read_prob("PlayerA")
PlayerB = read_prob("PlayerB")
PlayerC = read_prob("PlayerC")

strengths = {
    "PlayerA": PlayerA,
    "PlayerB": PlayerB,
    "PlayerC": PlayerC
}

# Category adjustments per player
adjustments = {
    "PlayerA": {"Fine Arts": +0.1, "Literature": -0.5},
    "PlayerB": {"Science": +0.2,      "Religion":   -0.3},
    "PlayerC": {"Mythology": +0.15,   "History":    -0.2}
}

def adjust_strength(player_name: str, category: str, base_strength: float) -> float:
    """Return the new strength for `player_name` in `category`."""
    adj = adjustments.get(player_name, {}).get(category, 0.0)
    return base_strength + adj

# — Use the identifier module to pick a random clue & category —
# (identifier.py must expose: load_keywords, load_bank, pick_random, classify)
KEYWORDS = identifier.load_keywords("keywords.json")
bank     = identifier.load_bank("final_jeopardy_all.json")

rec = identifier.pick_random(bank)
q   = rec.get("question", "")
a   = rec.get("answer", "")
orig= rec.get("category", "")

choice = identifier.classify(orig, q, a, KEYWORDS)

# — Display the selected clue and the computed category —
print("\n=== SELECTED FINAL JEOPARDY! CLUE ===")
print(f"Clue:   {q}")
print(f"Answer: {a}")
print(f"Jeopardy! Category: {orig}")
print(f"\n→ FINAL CATEGORY (for strengths): {choice}\n")

# — Compute & print each player’s adjusted strength —
print("=== Player Strengths ===")
for player, base in strengths.items():
    new_str = adjust_strength(player, choice, base)
    print(f"{player}: {base:.2f} → {new_str:.2f}")
