"""
What's My Grade, Really? — Grade Calculator
--------------------------------------------
Encodes ONE teacher's actual grading policy (not a generic app's guess)
and tells you exactly where you stand, plus what you need on the final.

HOW TO USE THIS FOR YOURSELF:
1. Replace the SAMPLE DATA below with your real scores.
2. Replace the POLICY section with your real teacher's real rules.
3. Run: python3 grade_calculator.py
4. Verify at least one category by hand (see "Verification" printout).
"""

# =========================================================
# 1. SAMPLE DATA -- replace with YOUR real scores
# =========================================================

# Monthly tests, each out of 20. Policy: lowest score is DROPPED.
monthly_tests = [15, 18, 12, 20, 17]   # out of 20 each

# Class assignments, each out of 10. Policy: simple average, nothing dropped.
assignments = [9, 10, 8, 10, 9, 10, 7, 9, 10, 8]  # out of 10 each

# Mid term exam, out of 100.
mid_term = 72

# Final term exam, out of 100.
# Set to None if you haven't taken it yet -- the script will instead
# tell you what score you NEED to hit your target grade.
final_term = None   # e.g. final_term = 81

# =========================================================
# 2. POLICY -- replace with YOUR teacher's real rules
# =========================================================

WEIGHTS = {
    "monthly_tests": 0.15,
    "assignments": 0.15,
    "mid_term": 0.30,
    "final_term": 0.40,
}

# Special rule: if Final Term % is HIGHER than Mid Term %, the Final Term
# score replaces the Mid Term score for grading purposes (rewards
# improvement). This is the kind of rule no generic grade app knows about.
REPLACEMENT_RULE_ENABLED = True

GRADE_BANDS = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0,  "F"),
]

TARGET_GRADE_PERCENT = 80.0  # e.g. aiming for an "A"


# =========================================================
# 3. CALCULATION LOGIC
# =========================================================

def monthly_tests_percent(scores, max_each=20):
    """Drop the lowest score, average the rest, convert to %."""
    if len(scores) <= 1:
        kept = scores
    else:
        scores_sorted = sorted(scores)
        kept = scores_sorted[1:]  # drop the single lowest
    avg = sum(kept) / len(kept)
    return (avg / max_each) * 100


def assignments_percent(scores, max_each=10):
    avg = sum(scores) / len(scores)
    return (avg / max_each) * 100


def letter_grade(percent):
    for cutoff, letter in GRADE_BANDS:
        if percent >= cutoff:
            return letter
    return "F"


def compute_final_percentage(mt_pct, asg_pct, mid_pct, final_pct):
    """
    Applies category weights AND the mid/final replacement rule.
    Returns (overall_percent, mid_used, final_used, replacement_applied)
    """
    mid_used = mid_pct
    replacement_applied = False

    if REPLACEMENT_RULE_ENABLED and final_pct is not None and final_pct > mid_pct:
        mid_used = final_pct
        replacement_applied = True

    overall = (
        mt_pct * WEIGHTS["monthly_tests"]
        + asg_pct * WEIGHTS["assignments"]
        + mid_used * WEIGHTS["mid_term"]
        + final_pct * WEIGHTS["final_term"]
    )
    return overall, mid_used, final_pct, replacement_applied


def score_needed_for_target(mt_pct, asg_pct, mid_pct, target_percent):
    """
    Solves for the Final Term % needed to hit target_percent overall,
    accounting for the conditional replacement rule.
    Uses a straightforward numeric search across 0-100 (robust to the
    rule's conditional branch, unlike solving one clean equation).
    """
    best_x = None
    for x_tenth in range(0, 1001):  # 0.0 to 100.0 in 0.1 steps
        x = x_tenth / 10
        overall, _, _, _ = compute_final_percentage(mt_pct, asg_pct, mid_pct, x)
        if overall >= target_percent:
            best_x = x
            break
    return best_x


# =========================================================
# 4. RUN
# =========================================================

if __name__ == "__main__":
    mt_pct = monthly_tests_percent(monthly_tests)
    asg_pct = assignments_percent(assignments)
    mid_pct = mid_term  # already out of 100

    print("=" * 55)
    print("CATEGORY BREAKDOWN")
    print("=" * 55)
    print(f"Monthly Tests   : raw {monthly_tests} -> lowest dropped -> {mt_pct:.2f}%")
    print(f"Assignments     : raw {assignments} -> average -> {asg_pct:.2f}%")
    print(f"Mid Term        : {mid_pct:.2f}%")
    print(f"Final Term      : {final_term if final_term is not None else 'not taken yet'}")
    print()

    print("=" * 55)
    print("VERIFICATION (check this by hand!)")
    print("=" * 55)
    kept_tests = sorted(monthly_tests)[1:]
    print(f"Monthly tests sorted: {sorted(monthly_tests)}")
    print(f"Dropped lowest: {sorted(monthly_tests)[0]}")
    print(f"Kept: {kept_tests}  ->  sum={sum(kept_tests)}, "
          f"count={len(kept_tests)}, avg={sum(kept_tests)/len(kept_tests):.2f}")
    print(f"As % of {20}: {mt_pct:.2f}%  <-- confirm this matches your own math")
    print()

    if final_term is not None:
        overall, mid_used, final_used, replaced = compute_final_percentage(
            mt_pct, asg_pct, mid_pct, final_term
        )
        print("=" * 55)
        print("FINAL RESULT")
        print("=" * 55)
        if replaced:
            print(f"Replacement rule TRIGGERED: Final ({final_term}%) > Mid ({mid_pct}%), "
                  f"so Mid Term is treated as {mid_used:.2f}% for grading.")
        print(f"Overall percentage: {overall:.2f}%")
        print(f"Letter grade: {letter_grade(overall)}")
    else:
        needed = score_needed_for_target(mt_pct, asg_pct, mid_pct, TARGET_GRADE_PERCENT)
        print("=" * 55)
        print(f"FINAL EXAM SCORE NEEDED FOR {TARGET_GRADE_PERCENT}% "
              f"({letter_grade(TARGET_GRADE_PERCENT)})")
        print("=" * 55)
        if needed is None:
            print("Target is not reachable even with 100% on the final.")
        else:
            print(f"You need at least {needed:.1f}% on the Final Term exam "
                  f"(i.e. {needed:.1f}/100) to reach {TARGET_GRADE_PERCENT}% overall.")
