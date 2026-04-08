import requests
import time
import json
from datetime import datetime
import os

# API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# Categories with keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category
    return "others"

def fetch_data():
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        story_ids = response.json()[:500]
    except:
        print("Error fetching top stories")
        return

    collected = []
    category_count = {key: 0 for key in categories}

    for story_id in story_ids:
        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            story = res.json()

            if not story or "title" not in story:
                continue

            category = get_category(story["title"])

            # limit 25 per category
            if category in category_count and category_count[category] >= 25:
                continue

            data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected.append(data)

            if category in category_count:
                category_count[category] += 1

            # stop if all categories filled
            if all(count >= 25 for count in category_count.values()):
                break

        except:
            print(f"Error fetching story {story_id}")
            continue

    # create folder
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w") as f:
        json.dump(collected, f, indent=4)

    print(f"Collected {len(collected)} stories. Saved to {filename}")


if __name__ == "__main__":
    fetch_data()