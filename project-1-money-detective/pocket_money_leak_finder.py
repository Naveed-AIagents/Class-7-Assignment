"""
pocket_money_leak_finder.py
============================

WHAT THIS DOES
--------------
Reads a wallet/bank transaction export and answers three questions:
  1. Where does the money actually go? (spend grouped by category)
  2. What's quietly charging me every month? (subscriptions/utilities)
  3. Did anything get billed twice on the same day? (exact-duplicate charges)
It also rebuilds your running balance day by day to show how much cash
you have left heading into your next pocket money / paycheck.

EXPECTED INPUT FILE
--------------------
A CSV with exactly these columns (header names must match):
  Date            - a date, e.g. 2026-07-01 (any format pandas can parse)
  Description     - free text, e.g. "Foodpanda - Cheezious"
  Amount (PKR)    - a number; POSITIVE = money in, NEGATIVE = money out
  Category        - a label you assign, e.g. Food, Travel, Rent,
                    Subscription, Utilities, Income, Books, etc.

  One recurring category is treated as your allowance/income stream:
  by default this script looks for Category == "Income" to find
  pocket-money/paycheck deposits and work out how often they arrive.
  Change INCOME_CATEGORY below if you label it differently.

By default the script looks for a file named "transactions.csv" in the
same folder. Pass a different path as a command-line argument, e.g.:
    python3 pocket_money_leak_finder.py my_export.csv

RULES IT FOLLOWS
-----------------
- Recurring charges = any transaction whose Category is "Subscription"
  or "Utilities" (edit RECURRING_CATEGORIES below to add more, e.g.
  "Rent" if that varies and you want it flagged too).
- Duplicate charge = same Date + same Description + same Amount
  appearing more than once. This is a strict, exact match on purpose
  (it flags the Foodpanda-style same-item-same-day double bill,
  not two different orders from the same restaurant).
- Running balance starts at 0 and simply adds/subtracts every
  transaction in date order — it shows relative cash flow within the
  file, not your real bank balance (unless the file covers your
  whole history).
- "Next pocket money" is estimated from the gap (in days) between your
  most recent income deposits, then projected forward from the last
  one seen in the file.
- Nothing is ever silently dropped: every transaction in the file
  is accounted for in either the category totals or the running
  balance.

USAGE
-----
    python3 pocket_money_leak_finder.py [path_to_csv]

Requires: pandas (pip install pandas --break-system-packages)
"""

import sys
import pandas as pd

# ---- configurable rules -----------------------------------------------
RECURRING_CATEGORIES = {"Subscription", "Utilities"}
INCOME_CATEGORY = "Income"
AMOUNT_COL = "Amount (PKR)"
# ------------------------------------------------------------------------


def load(path):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df[AMOUNT_COL] = df[AMOUNT_COL].astype(float)
    return df.sort_values("Date").reset_index(drop=True)


def print_totals(df):
    print("=== Date range ===")
    print(df["Date"].min().date(), "to", df["Date"].max().date())

    income = df[df[AMOUNT_COL] > 0][AMOUNT_COL].sum()
    expenses = df[df[AMOUNT_COL] < 0][AMOUNT_COL].sum()
    print("\n=== Totals ===")
    print(f"Income:   {income:,.0f}")
    print(f"Expenses: {expenses:,.0f}")
    print(f"Net:      {income + expenses:,.0f}")


def print_categories(df):
    print("\n=== Spend by category (biggest leak first) ===")
    cat = (
        df[df[AMOUNT_COL] < 0]
        .groupby("Category")[AMOUNT_COL]
        .agg(["sum", "count"])
        .sort_values("sum")
    )
    print(cat)


def print_recurring(df):
    print("\n=== Quietly-recurring charges (subscriptions/utilities) ===")
    recurring = df[df["Category"].isin(RECURRING_CATEGORIES)]
    if recurring.empty:
        print("None found.")
    else:
        print(recurring[["Date", "Description", AMOUNT_COL, "Category"]])
        print(f"\nTotal per cycle: {recurring[AMOUNT_COL].sum():,.0f}")


def print_duplicates(df):
    print("\n=== Same charge billed twice on the same day ===")
    dupes = df[df.duplicated(subset=["Date", "Description", AMOUNT_COL], keep=False)]
    if dupes.empty:
        print("None found.")
    else:
        print(dupes.sort_values("Date")[["Date", "Description", AMOUNT_COL]])


def print_balance_and_forecast(df):
    print("\n=== Running balance ===")
    df = df.copy()
    df["Balance"] = df[AMOUNT_COL].cumsum()
    print(df[["Date", "Description", AMOUNT_COL, "Balance"]].to_string(index=False))

    income_dates = df[df["Category"] == INCOME_CATEGORY]["Date"].tolist()
    if len(income_dates) < 2:
        print("\nNot enough income entries to estimate a pocket-money cadence.")
        return

    gaps = [(income_dates[i + 1] - income_dates[i]).days for i in range(len(income_dates) - 1)]
    avg_gap = round(sum(gaps) / len(gaps))
    last_pocket = income_dates[-1]
    next_pocket = last_pocket + pd.Timedelta(days=avg_gap)
    last_date = df["Date"].max()
    final_balance = df["Balance"].iloc[-1]

    print(f"\nPocket-money gaps seen (days): {gaps}")
    print(f"Last pocket money: {last_pocket.date()}")
    print(f"Estimated next pocket money: {next_pocket.date()} (every ~{avg_gap} days)")
    print(f"Last transaction on file: {last_date.date()}")
    print(f"Balance left as of last transaction: {final_balance:,.0f}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "transactions.csv"
    df = load(path)
    print_totals(df)
    print_categories(df)
    print_recurring(df)
    print_duplicates(df)
    print_balance_and_forecast(df)


if __name__ == "__main__":
    main()
