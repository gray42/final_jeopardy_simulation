
import json
import random
import re
import sys
from difflib import SequenceMatcher

# —— your ten target buckets —— 
BUCKETS = [
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

def load_keywords(path="keywords.json"):
    """
    Load your single JSON of static keywords per bucket.
    """
    try:
        with open(path, encoding='utf-8') as f:
            kws = json.load(f)
    except FileNotFoundError:
        print(f"Error: cannot find '{path}'.", file=sys.stderr)
        sys.exit(1)

    # Validate
    for b in BUCKETS:
        if b not in kws:
            print(f"Error: bucket '{b}' missing in keywords.json", file=sys.stderr)
            sys.exit(1)
        if not isinstance(kws[b], list) or len(kws[b]) == 0:
            print(f"Error: bucket '{b}' has no keywords", file=sys.stderr)
            sys.exit(1)

    return kws

def load_bank(path="final_jeopardy_all.json"):
    """
    Load the Final Jeopardy! clue bank JSON.
    """
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: cannot find '{path}'.", file=sys.stderr)
        sys.exit(1)

def classify(orig_cat, clue, answer, KEYWORDS):
    """
    Score each bucket by:
      1) 2× string-similarity(orig_cat, bucket)
      2) +1 per whole-word keyword hit in clue+answer
    Return the highest-scoring bucket, or 'Trash' if all scores ≤ 0.
    """
    txt = (clue + " " + answer).lower()
    best_bucket, best_score = "Trash", 0.0

    for bucket in BUCKETS:
        # similarity boost
        sim = SequenceMatcher(None, orig_cat.lower(), bucket.lower()).ratio()
        score = sim * 2.0

        # keyword hits
        for kw in KEYWORDS[bucket]:
            # whole-word match
            hits = len(re.findall(rf"\b{re.escape(kw.lower())}\b", txt))
            score += hits

        if score > best_score:
            best_score, best_bucket = score, bucket

    return best_bucket

def pick_random(bank):
    return random.choice(bank)

def main():
    KEYWORDS = load_keywords()
    bank = load_bank()

    print("=== Final Jeopardy! Random Clue + Static-Keyword Classifier ===")
    print("Press Enter to draw a clue (Ctrl-C to exit).")

    try:
        while True:
            input()
            rec = pick_random(bank)
            q   = rec.get("question", "")
            a   = rec.get("answer", "")
            orig= rec.get("category", "")

            pred = classify(orig, q, a, KEYWORDS)

            print("\n❓ Clue:             ", q)
            print("💡 Answer:          ", a)
            print("🏷 Jeopardy! Category:", orig)
            return("🔍 Predicted Bucket: ", pred, "\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
