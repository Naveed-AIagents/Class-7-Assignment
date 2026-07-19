# code-you-never-write
# AI-Assisted Problem Solving: Real-Life Money & Grade Detective Work

## Overview
This project is a collection of three real, personal problems I solved by pairing my own domain knowledge with Claude as a coding assistant. In each case, I gave Claude messy, real-world data (bank/wallet transactions, grading rules, a class trip fund), asked it to **write and run actual code** rather than just estimate an answer, and then **verified the output against a number I already knew by hand**. The goal wasn't just to get an answer — it was to prove the AI's answer was trustworthy before relying on it.

## Why These Three Projects Belong Together
All three follow the same core pattern:

1. **I had a known or hand-calculated baseline** (my own wallet math, my own grade calculation, my own hand-count of trip money).
2. **I gave Claude the raw, messy real data** — inconsistent transaction logs, informal names, teacher-specific grading quirks.
3. **I asked for code, not just conversation** — a script I could see run, with real output, not just a text explanation.
4. **I verified every result against my baseline** before trusting it.
5. **Each project surfaced a real discrepancy** — a duplicate charge, a grade I could act on, a student who still owed money.

This README ties the three sub-projects together as one body of work demonstrating how AI tools can be used responsibly: as a calculator/detective that does the tedious work, while I remain the one who defines the rules and checks the math.

## Projects in This Repository

| # | Project | Problem Solved | Key Result |
|---|---------|-----------------|------------|
| 1 | [Money Detective](./project-1-money-detective/README.md) | Find recurring charges, forgotten subscriptions, and duplicate payments in my own transaction history | Found a duplicate Foodpanda charge |
| 2 | [What's My Grade, Really](./project-2-whats-my-grade-really/README.md) | Calculate true current grade using my teacher's specific rules (dropped lowest score, weighted categories, mid-term/final replacement) | Got a script showing current grade and required final-term score for an A |
| 3 | [The Books Don't Match](./project-3-books-dont-match/README.md) | Reconcile a class trip fund against a messy digital transfer log with nicknames and informal names | Found the exact Rs 1,500 gap — one student (Mohsin Raza) underpaid |

*(Adjust the folder names above to match however you've actually organized the files.)*

## Common Method Across All Projects

**AI Tool Used:** Claude (used as a coding assistant to write and execute Python scripts)

**Workflow:**
- Start with a clear, detailed prompt that includes the raw data and the exact rules/context needed (grading policy, waiver amounts, what counts as a "duplicate," etc.)
- Ask Claude to write and run code rather than answer from reasoning alone, so the process is transparent and checkable
- Review the code's actual output
- Cross-check the output against a number I already calculated by hand
- Only trust and act on the result once it matched my own math

**Verification Philosophy:**
In every project, I never accepted the AI's answer purely on faith. I always had (or built) an independent way to check it — my own wallet total, my own grade calculation, my own hand-count of trip money — and only moved forward once the script's output matched what I already knew to be true.

## What This Demonstrates
- How to turn messy, real-world personal data (transactions, grades, informal payment records) into a well-defined problem an AI tool can solve with code
- How to write prompts that include enough specific rules and context for the AI to get an exact, usable answer instead of a vague one
- How to verify AI-generated results independently before trusting them
- Practical, everyday uses of AI beyond writing or chatting — as a personal finance auditor, an academic calculator, and a reconciliation tool

## Files in This Repository
- `README.md` — this overview file
- `project-1-money-detective/` — transaction analysis project (script, prompts, results)
- `project-2-whats-my-grade-really/` — grade calculator project (script, prompts, results)
- `project-3-books-dont-match/` — class trip fund reconciliation project (`reconcile.py`, screenshots, results)
