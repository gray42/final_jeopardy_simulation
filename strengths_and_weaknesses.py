import random
x = float(input("Enter a number:"))
if x > 1:
    print("Probability cannot be greater than 1")
    x = input("Enter a number:")

y = float(input("Enter a number:"))
if y > 1:
    print("Probability cannot be greater than 1")
    y = input("Enter a number:")

z = float(input("Enter a number:"))
if z > 1:
    print("Probability cannot be greater than 1")
    z = input("Enter a number:")

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

# These weights correspond 1-to-1 with `categories`
weights = [
    0.01,  # Mathematics
    0.10,  # Science
    0.10,  # Trash
    0.30,  # History
    0.10,  # Social Sciences & Current Events
    0.15,  # Literature
    0.05,  # Fine Arts
    0.13,  # Geography
    0.03,  # Religion
    0.03   # Mythology
]

# Base strengths
strengths = {
    "PlayerA": x,
    "PlayerB": y,
    "PlayerC": z
}

# Category adjustments per player
adjustments = {
    "PlayerA": {"Fine Arts": +0.1, "Literature": -0.5},
    "PlayerB": {"Science": +0.2, "Religion": -0.3},
    "PlayerC": {"Mythology": +0.15, "History": -0.2}
}

def adjust_strength(player_name: str, category: str, base_strength: float) -> float:
    """Return the new strength for `player_name` in `category`."""
    adj = adjustments.get(player_name, {}).get(category, 0.0)
    return base_strength + adj

# Let user pick a category, or fall back to weighted random
choice = input(f"Pick a category from {categories}, or press Enter for random: ").strip()
if choice not in categories:
    choice = random.choices(categories, weights=weights, k=1)[0]
    print(f"No valid selection, randomly choosing (weighted): {choice!r}")

print(f"\nFINAL CATEGORY → {choice}\n")

# Compute and print each player’s adjusted strength
for player, base in strengths.items():
    new_strength = adjust_strength(player, choice, base)
    print(f"{player}: {base:.2f} → {new_strength:.2f}")

