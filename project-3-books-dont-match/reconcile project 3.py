"""
Class trip payment reconciliation.

How to use:
1. Fill in ROSTER with every student's name and what they SHOULD owe.
2. Fill in RAW_TRANSACTIONS with the messy list exactly as it came in.
3. Fill in NAME_MAP to resolve each transaction line to a canonical roster name.
   (This is where you apply your matching rules: "X's Mom" / "S/o [surname]"
   -> that student; nicknames/initials -> the obvious roster name.)
4. If a transaction genuinely can't be matched, map it to None -- the script
   will flag it separately instead of guessing.
"""

KNOWN_CORRECT_TOTAL = 49500

# ---- 1. Roster: what each student SHOULD owe ----
ROSTER = {
    "Ahmed": 3000,
    "Bilal": 1500,          # 50% waiver
    "Fatima Noor": 3000,
    "Hassan Ali": 3000,
    "Iqra": 3000,
    "J. Baig": 3000,
    "Kiran": 3000,
    "Laiba": 3000,
    "Mohsin Raza": 3000,
    "Nida Farooq": 3000,
    "Omar": 3000,
    "Palwasha": 3000,
    "Qasim Iqbal": 3000,
    "Rabia": 3000,
    "Sana": 3000,
    "Usman Ghani": 3000,
    "Tauseef Khan": 3000,
    "Zara": 0,               # full scholarship
}

# ---- 2. Raw transaction list, exactly as received (label, amount) ----
RAW_TRANSACTIONS = [
    ("Ahmed R", 3000),
    ("Bilal S/o Sheikh sb", 1500),
    ("FATIMA NOOR", 3000),
    ("Hassan Ali (easypaisa)", 3000),
    ("Iqra M.", 3000),
    ("J. Baig", 3000),
    ("Kiran", 3000),
    ("laiba ch", 3000),
    ("Mohsin Raza", 1500),
    ("Nida Farooq", 3000),
    ("Omar S", 3000),
    ("Palwasha's Mom", 3000),
    ("Qasim Iqbal", 3000),
    ("Rabia H", 3000),
    ("Sana Y", 3000),
    ("Usman Ghani", 3000),
    ("Cash - Tauseef Khan", 3000),
]

# ---- 3. Map each raw label to the canonical roster name ----
# (Apply your rules here: S/o -> that student, X's Mom -> that student,
#  nicknames/initials -> obvious match. Use None if genuinely unclear.)
NAME_MAP = {
    "Ahmed R": "Ahmed",
    "Bilal S/o Sheikh sb": "Bilal",
    "FATIMA NOOR": "Fatima Noor",
    "Hassan Ali (easypaisa)": "Hassan Ali",
    "Iqra M.": "Iqra",
    "J. Baig": "J. Baig",
    "Kiran": "Kiran",
    "laiba ch": "Laiba",
    "Mohsin Raza": "Mohsin Raza",
    "Nida Farooq": "Nida Farooq",
    "Omar S": "Omar",
    "Palwasha's Mom": "Palwasha",
    "Qasim Iqbal": "Qasim Iqbal",
    "Rabia H": "Rabia",
    "Sana Y": "Sana",
    "Usman Ghani": "Usman Ghani",
    "Cash - Tauseef Khan": "Tauseef Khan",
}


def reconcile():
    digital_total = sum(amount for _, amount in RAW_TRANSACTIONS)

    paid = {name: 0 for name in ROSTER}
    unmatched = []

    for label, amount in RAW_TRANSACTIONS:
        canonical = NAME_MAP.get(label)
        if canonical is None:
            unmatched.append((label, amount))
            continue
        if canonical not in ROSTER:
            unmatched.append((label, amount))
            continue
        paid[canonical] += amount

    print("=" * 50)
    print("CLASS TRIP RECONCILIATION")
    print("=" * 50)
    print(f"Digital/transfer total received : Rs {digital_total:,}")
    print(f"Known correct total (hand count) : Rs {KNOWN_CORRECT_TOTAL:,}")

    gap = KNOWN_CORRECT_TOTAL - digital_total
    if gap == 0:
        print("Gap: Rs 0 — totals match!")
    elif gap > 0:
        print(f"Gap: Rs {gap:,} MISSING from digital total")
    else:
        print(f"Gap: Rs {abs(gap):,} MORE than expected in digital total")

    print()
    print("-" * 50)
    print("STUDENTS WHO STILL OWE MONEY")
    print("-" * 50)
    owing = []
    for name, expected in ROSTER.items():
        balance = expected - paid[name]
        if balance > 0:
            owing.append((name, paid[name], expected, balance))

    if owing:
        for name, amt_paid, expected, balance in owing:
            print(f"  {name:15s} paid Rs {amt_paid:,} / owes Rs {expected:,}  "
                  f"-> STILL OWES Rs {balance:,}")
    else:
        print("  None — everyone accounted for is paid in full.")

    if unmatched:
        print()
        print("-" * 50)
        print("UNMATCHED TRANSACTIONS (needs manual review, not guessed)")
        print("-" * 50)
        for label, amount in unmatched:
            print(f"  {label!r} - Rs {amount:,}")

    print()
    print("-" * 50)
    print(f"Sum of 'still owes' amounts: Rs {sum(b for *_, b in owing):,}")
    print(f"This should equal the gap above if everything else checks out.")


if __name__ == "__main__":
    reconcile()
