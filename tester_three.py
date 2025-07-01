import random

categories = [
    "Mathematics",
    "Science",
    "Trash",
    "History",
    "Social Sciences & Current Events",
    "Literature",
    "Fine Arts",
    "Geography",
    "Religion",
    "Mythology"
]

# Base strengths
strengths = {
    "PlayerA": 0.9,
    "PlayerB": 0.6,
    "PlayerC": 0.4
}

# How each category affects each player
# positive numbers = strength boost; negative = weakness
adjustments = {
    "PlayerA": {
        "Fine Arts": +0.1,
        "Literature": -0.5
        # … you can add more categories here
    },
    "PlayerB": {
        "Science": +0.2,
        "Religion": -0.3
        # etc.
    },
    "PlayerC": {
        "Mythology": +0.15,
        "History": -0.2
        # etc.
    }
}

def adjust_strength(player_name: str, category: str, base_strength: float) -> float:
    """Return the new strength for `player_name` in `category`."""
    adj = adjustments.get(player_name, {}).get(category, 0.0)
    return base_strength + adj

# Let user pick a category, or fall back to random
choice = input(f"Pick a category from {categories}, or press Enter for random: ").strip()
if choice not in categories:
    choice = random.choice(categories)
    print(f"No valid selection, randomly choosing: {choice!r}")

print(f"\nFINAL CATEGORY → {choice}\n")

# Compute and print each player’s adjusted strength
for player, base in strengths.items():
    new_strength = adjust_strength(player, choice, base)
    print(f"{player}: {base:.2f} → {new_strength:.2f}")
