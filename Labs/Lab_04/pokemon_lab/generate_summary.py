#!/usr/bin/env python3

import os
import sys
import pandas as pd


def generate_summary(portfolio_file: str) -> None:
    """Read a portfolio CSV and print summary stats."""
    if not os.path.exists(portfolio_file):
        print(f"ERROR: File not found: {portfolio_file}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("No data found in portfolio file. Nothing to report.")
        return

    # Validate required columns
    required_cols = {"card_market_value", "card_name", "card_id"}
    missing = required_cols - set(df.columns)
    if missing:
        print(f"ERROR: Missing required columns in portfolio: {missing}", file=sys.stderr)
        sys.exit(1)

    # Total portfolio value
    total_portfolio_value = df["card_market_value"].fillna(0.0).sum()

    # Most valuable card
    # Safeguard: if all NaN, fill with 0 first
    if df["card_market_value"].isna().all():
        most_valuable_row = df.iloc[0]
        mv_value = 0.0
    else:
        idx = df["card_market_value"].fillna(0.0).idxmax()
        most_valuable_row = df.loc[idx]
        mv_value = float(most_valuable_row["card_market_value"] or 0.0)

    mv_name = str(most_valuable_row.get("card_name", "UNKNOWN"))
    mv_id = str(most_valuable_row.get("card_id", "UNKNOWN"))

    # Print report
    print("=========== Portfolio Summary ===========")
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print("-----------------------------------------")
    print("Most Valuable Card:")
    print(f"  Name : {mv_name}")
    print(f"  ID   : {mv_id}")
    print(f"  Value: ${mv_value:,.2f}")
    print("=========================================")


def main():
    """Run summary on production portfolio file."""
    generate_summary("card_portfolio.csv")


def test():
    """Run summary on test portfolio file."""
    generate_summary("test_card_portfolio.csv")


if __name__ == "__main__":
    # Default to test mode for safe, self-contained runs
    test()
