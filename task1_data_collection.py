"""
TrendPulse - Task 1: Data Collection
Fetches trending stories from HackerNews API and saves them to a JSON file.
"""

import requests
import json
import os
import time
from datetime import datetime

# --- Category keyword mapping (case-insensitive) ---
CATEGORIES = {
    "technology":    ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
}

MAX_STORIES_PER_CATEGORY = 25  # Collect up to 25 per category (125 total)

# HackerNews API endpoints
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"

# Required header
HEADERS = {"User-Agent": "TrendPulse/1.0"}


def assign_category(title):
    """
    Assign a category to a story based on keywords in the title.
    Returns None if no category matches.
    """
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None  # No matching category


def fetch_top_story_ids():
    """Fetch the list of top story IDs from HackerNews (first 500)."""
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        ids = response.json()
        print(f"Fetched {len(ids)} top story IDs.")
        return ids[:500]  # Take only the first 500
    except Exception as e:
        print(f"Error fetching top story IDs: {e}")
        return []


def fetch_story(story_id):
    """Fetch a single story's details by its ID."""
    url = ITEM_URL.format(id=story_id)
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Failed to fetch story {story_id}: {e}")
        return None


def collect_stories(story_ids):
    """
    Iterate through story IDs, categorise each story, and collect
    up to MAX_STORIES_PER_CATEGORY per category.
    Waits 2 seconds between processing each category batch.
    """
    # Track how many stories we have per category
    category_counts = {cat: 0 for cat in CATEGORIES}
    collected = []

    # We'll iterate category by category to apply the sleep correctly
    for category in CATEGORIES:
        print(f"\nCollecting stories for category: '{category}' ...")
        stories_in_category = 0

        for story_id in story_ids:
            # Stop if we've hit the limit for this category
            if stories_in_category >= MAX_STORIES_PER_CATEGORY:
                break

            story = fetch_story(story_id)

            # Skip stories that failed to load or have no title
            if not story or "title" not in story:
                continue

            title = story.get("title", "")
            assigned = assign_category(title)

            # Only keep this story if it belongs to the current category
            if assigned != category:
                continue

            # Extract the required fields
            record = {
                "post_id":      story.get("id"),
                "title":        title,
                "category":     assigned,
                "score":        story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author":       story.get("by", ""),
                "collected_at": datetime.now().isoformat(),
            }

            collected.append(record)
            stories_in_category += 1
            category_counts[category] += 1

        print(f"  Collected {stories_in_category} stories for '{category}'.")

        # Wait 2 seconds between category loops (not per individual fetch)
        time.sleep(2)

    return collected, category_counts


def save_to_json(stories):
    """Save collected stories to data/trends_YYYYMMDD.json."""
    # Create data/ folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{today}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

    return filename


def main():
    print("=== TrendPulse: Task 1 — Data Collection ===\n")

    # Step 1 — Get top story IDs
    story_ids = fetch_top_story_ids()
    if not story_ids:
        print("No story IDs fetched. Exiting.")
        return

    # Step 2 — Collect and categorise stories
    stories, category_counts = collect_stories(story_ids)

    # Step 3 — Save to JSON
    filename = save_to_json(stories)

    # Final summary
    print(f"\nCollected {len(stories)} stories. Saved to {filename}")
    print("\nStories per category:")
    for cat, count in category_counts.items():
        print(f"  {cat:<15} {count}")


if __name__ == "__main__":
    main()