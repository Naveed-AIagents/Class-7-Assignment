# Project 3: The Books Don't Match

## Problem
I hand-counted the expected total for a class trip fund and needed to reconcile it against a messy digital transfer record with inconsistent names, nicknames, and informal memos (e.g. "Palwasha's Mom", "Cash - Tauseef Khan").

## AI Tool Used
Claude

## My Known Baseline
Expected total: **Rs 49,500**
- 16 students × Rs 3,000 = Rs 48,000
- Bilal (50% waiver) = Rs 1,500
- Zara (full scholarship) = Rs 0
- Total = Rs 49,500 ✔

## Rules for Interpreting Ambiguous Entries
- A payment from "X's Mom" or "S/o [surname]" counts as that student's own payment.
- Nicknames, initials, or partial names (e.g. "laiba ch", "Iqra M.") are matched to whoever it obviously is on the roster.
- If a name genuinely can't be identified, it is flagged rather than guessed.

## Prompts Used
**Initial prompt:**
"hey i need help reconciling money for a class trip i hand counted and know the correct total should be rs 49500 (18 students owe rs 3000 each, except bilal who has 50% waiver so he owes 1500, and zara is on full scholarship so she owes 0) heres the messy bank/wallet transfer list exactly as it came... can u write a python script that adds up the digital total, compares it to my known 49500, and tells me the gap plus exactly which students still owe money"

**Improved prompt:** None needed — first version matched my known total logic correctly.

## Verification
I compared the script's output against my hand-counted total of Rs 49,500. The script reported a digital total of Rs 48,000 — a gap of exactly Rs 1,500. I checked this by hand: every payment matched a roster name correctly except Mohsin Raza, who paid Rs 1,500 instead of his expected Rs 3,000 (he has no known waiver). That single discrepancy accounts for the entire gap, confirming the script's logic is correct.

## Result
Total collected so far: Rs 48,000 of Rs 49,500 expected.
**Mohsin Raza still owes Rs 1,500.** Every other student has paid in full, and no digital entries were left unmatched or ambiguous.

## Files in this folder
- `reconcile.py` — the final script
- `screenshots/` — screenshots of the script running and its output
