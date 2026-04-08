"""
TrendPulse - Task 2: Data Processing
Loads the JSON from Task 1, cleans it with Pandas, and saves a tidy CSV file.
"""

import os
import glob
import pandas as pd


def find_latest_json():
    """Find the most recently created trends JSON file in data/."""
    files = glob.glob("data/trends_*.json")
    if not files:
        raise FileNotFoundError("No trends JSON file found in data/ folder. Run Task 1 first.")
    # Sort by filename (YYYYMMDD in name ensures correct order)
    latest = sorted(files)[-1]
    return latest


def load_json(filepath):
    """Load the JSON file into a Pandas DataFrame."""
    df = pd.read_json(filepath)
    print(f"Loaded {len(df)} stories from {filepath}")
    return df


def clean_data(df):
    """
    Apply all cleaning steps and return the cleaned DataFrame.
    Prints the row count after each step.
    """

    # --- Step 1: Remove duplicates based on post_id ---
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # --- Step 2: Drop rows where post_id, title, or score is missing ---
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # --- Step 3: Enforce correct data types ---
    # score and num_comments must be integers
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    # --- Step 4: Remove low-quality stories (score < 5) ---
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # --- Step 5: Strip extra whitespace from the title column ---
    df["title"] = df["title"].str.strip()

    return df


def save_csv(df):
    """Save the cleaned DataFrame to data/trends_clean.csv."""
    os.makedirs("data", exist_ok=True)
    output_path = "data/trends_clean.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\nSaved {len(df)} rows to {output_path}")
    return output_path


def print_category_summary(df):
    """Print how many stories exist per category."""
    print("\nStories per category:")
    summary = df["category"].value_counts()
    for category, count in summary.items():
        print(f"  {category:<15} {count}")


def main():
    print("=== TrendPulse: Task 2 — Data Processing ===\n")

    # Step 1 — Load the JSON file
    json_file = find_latest_json()
    df = load_json(json_file)
    print()

    # Step 2 — Clean the data
    df = clean_data(df)

    # Step 3 — Save as CSV + print summaries
    save_csv(df)
    print_category_summary(df)


if __name__ == "__main__":
    main()