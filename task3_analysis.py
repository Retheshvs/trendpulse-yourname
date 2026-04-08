"""
TrendPulse - Task 3: Analysis with Pandas & NumPy
Loads the cleaned CSV from Task 2, explores it, computes statistics using NumPy,
adds new columns, and saves the result for Task 4.
"""

import pandas as pd
import numpy as np


def load_data():
    """Load the cleaned CSV file from Task 2 into a DataFrame."""
    filepath = "data/trends_clean.csv"
    df = pd.read_csv(filepath)
    print(f"Loaded data: {df.shape}")  # (rows, columns)
    return df


def explore_data(df):
    """Print basic exploration info: first 5 rows, shape, averages."""

    # Print first 5 rows
    print("\nFirst 5 rows:")
    print(df[["post_id", "title", "category", "score", "num_comments"]].head())

    # Average score and average num_comments across all stories
    avg_score    = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    print(f"\nAverage score   : {avg_score:.0f}")
    print(f"Average comments: {avg_comments:.0f}")

    return avg_score  # Return for use in add_columns()


def numpy_analysis(df):
    """Use NumPy to compute and print key statistics about the score column."""
    scores = df["score"].to_numpy()  # Convert to NumPy array

    print("\n--- NumPy Stats ---")
    print(f"Mean score    : {np.mean(scores):.0f}")
    print(f"Median score  : {np.median(scores):.0f}")
    print(f"Std deviation : {np.std(scores):.0f}")
    print(f"Max score     : {np.max(scores)}")
    print(f"Min score     : {np.min(scores)}")

    # Which category has the most stories?
    top_category = df["category"].value_counts().idxmax()
    top_count    = df["category"].value_counts().max()
    print(f"\nMost stories in: {top_category} ({top_count} stories)")

    # Which story has the most comments?
    most_commented_idx   = df["num_comments"].idxmax()
    most_commented_title = df.loc[most_commented_idx, "title"]
    most_commented_count = df.loc[most_commented_idx, "num_comments"]
    print(f'\nMost commented story: "{most_commented_title}" — {most_commented_count} comments')


def add_columns(df, avg_score):
    """
    Add two new computed columns to the DataFrame:
    - engagement : num_comments / (score + 1)  — discussion per upvote
    - is_popular : True if score > average score, else False
    """

    # engagement measures how much discussion a story generates per upvote
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular flags stories that are above-average in score
    df["is_popular"] = df["score"] > avg_score

    print(f"\nAdded 'engagement' and 'is_popular' columns.")
    print(f"Popular stories (above avg score): {df['is_popular'].sum()}")

    return df


def save_result(df):
    """Save the updated DataFrame (with new columns) to data/trends_analysed.csv."""
    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\nSaved to {output_path}")


def main():
    print("=== TrendPulse: Task 3 — Analysis with Pandas & NumPy ===")

    # Step 1 — Load and explore
    df = load_data()
    avg_score = explore_data(df)

    # Step 2 — NumPy statistics
    numpy_analysis(df)

    # Step 3 — Add new columns
    df = add_columns(df, avg_score)

    # Step 4 — Save result
    save_result(df)


if __name__ == "__main__":
    main()