import json

def process_data():
    with open("data_raw.json", "r") as f:
        data = json.load(f)

    cleaned_data = []

    for item in data:
        cleaned_item = {
            "id": item.get("id"),
            "title": item.get("title").strip(),
            "length": len(item.get("title"))
        }
        cleaned_data.append(cleaned_item)

    with open("data_processed.json", "w") as f:
        json.dump(cleaned_data, f, indent=4)

    print("Data processed!")

if __name__ == "__main__":
    process_data()