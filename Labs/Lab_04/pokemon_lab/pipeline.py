#!/usr/bin/env python3

import sys
import update_portfolio
import generate_summary


def run_production_pipeline() -> None:
    """Run the full production pipeline: ETL -> Reporting."""
    print("Starting production pipeline…", file=sys.stderr)

    print("[1/2] Updating portfolio (ETL)…", file=sys.stderr)
    update_portfolio.main()  # writes card_portfolio.csv

    print("[2/2] Generating summary (Reporting)…", file=sys.stderr)
    generate_summary.main()  # reads card_portfolio.csv and prints report

    print("Pipeline complete ✅", file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()
