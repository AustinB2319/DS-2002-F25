#!/usr/bin/env python3

import os
import sys
import json
import glob
import pandas as pd


def _load_lookup_data(lookup_dir: str) -> pd.DataFrame:
    all_lookup_df = []
    for path in glob.glob(os.path.join(lookup_dir, "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "data" not in data or not isinstance(data["data"], list):
            continue
        df = pd.json_normalize(data["data"])
        holo = "tcgplayer.prices.holofoil.market"
        normal = "tcgplayer.prices.normal.market"
        for col in (holo, normal):
            if col not in df.columns:
                df[col] = pd.NA
        df["card_market_value"] = (
            df[holo].fillna(df[normal]).fillna(0.0).astype(float)
        )
        df = df.rename(
            columns={
                "id": "card_id",
                "name": "card_name",
                "number": "card_number",
                "set.id": "set_id",
                "set.name": "set_name",
            }
        )
        required_cols = [
            "card_id",
            "card_name",
            "card_number",
            "set_id",
            "set_name",
            "card_market_value",
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = pd.NA
        all_lookup_df.append(df[required_cols].copy())
    if not all_lookup_df:
        return pd.DataFrame(
            columns=[
                "card_id",
                "card_name",
                "card_number",
                "set_id",
                "set_name",
                "card_market_value",
            ]
        )
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df = lookup_df.sort_values(
        by=["card_id", "card_market_value"], ascending=[True, False]
    )
    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first").reset_index(drop=True)
    return lookup_df


def _load_inventory_data(inventory_dir: str) -> pd.DataFrame:
    inventory_data = []
    for path in glob.glob(os.path.join(inventory_dir, "*.csv")):
        df = pd.read_csv(path)
        inventory_data.append(df)
    if not inventory_data:
        return pd.DataFrame(
            columns=[
                "card_name",
                "set_id",
                "card_number",
                "binder_name",
                "page_number",
                "slot_number",
                "card_id",
            ]
        )
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    inventory_df["set_id"] = inventory_df["set_id"].astype(str)
    inventory_df["card_number"] = inventory_df["card_number"].astype(str)
    inventory_df["card_id"] = inventory_df["set_id"] + "-" + inventory_df["card_number"]
    return inventory_df


def update_portfolio(inventory_dir: str, lookup_dir: str, output_file: str) -> None:
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    final_cols = [
        "index",
        "binder_name",
        "page_number",
        "slot_number",
        "card_id",
        "card_name",
        "card_number",
        "set_id",
        "set_name",
        "card_market_value",
    ]
    if inventory_df.empty:
        print(
            "ERROR: No inventory found—writing empty portfolio with headers.",
            file=sys.stderr,
        )
        pd.DataFrame(columns=final_cols).to_csv(output_file, index=False)
        return
    lookup_cols = [
        "card_id",
        "card_name",
        "card_number",
        "set_id",
        "set_name",
        "card_market_value",
    ]
    merged = pd.merge(
        inventory_df,
        lookup_df[lookup_cols],
        on="card_id",
        how="left",
        suffixes=("_inv", ""),
    )
    if "card_market_value" not in merged.columns:
        merged["card_market_value"] = 0.0
    merged["card_market_value"] = merged["card_market_value"].fillna(0.0).astype(float)
    merged["set_name"] = merged.get("set_name", pd.Series(dtype=object)).fillna("NOT_FOUND")
    for col in ["binder_name", "page_number", "slot_number"]:
        if col not in merged.columns:
            merged[col] = pd.NA
    merged["index"] = (
        merged["binder_name"].astype(str)
        + "-"
        + merged["page_number"].astype(str)
        + "-"
        + merged["slot_number"].astype(str)
    )
    for col in final_cols:
        if col not in merged.columns:
            merged[col] = pd.NA
    final_df = merged[final_cols].copy()
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    final_df.to_csv(output_file, index=False)
    print(f"Portfolio written to: {output_file}")


def main():
    inventory_dir = "./card_inventory/"
    lookup_dir = "./card_set_lookup/"
    output_file = "card_portfolio.csv"
    update_portfolio(inventory_dir, lookup_dir, output_file)


def test():
    inventory_dir = "./card_inventory_test/"
    lookup_dir = "./card_set_lookup_test/"
    output_file = "test_card_portfolio.csv"
    update_portfolio(inventory_dir, lookup_dir, output_file)


if __name__ == "__main__":
    print("Starting update_portfolio.py in TEST MODE…", file=sys.stderr)
    test()
