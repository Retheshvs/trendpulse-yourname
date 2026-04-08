import json
import matplotlib.pyplot as plt

def visualize_data():
    with open("data_processed.json", "r") as f:
        data = json.load(f)

    lengths = [item["length"] for item in data[:10]]
    ids = [item["id"] for item in data[:10]]

    plt.bar(ids, lengths)
    plt.xlabel("Post ID")
    plt.ylabel("Title Length")
    plt.title("Title Length of First 10 Posts")

    plt.savefig("visualization.png")
    plt.show()

    print("Visualization created!")

if __name__ == "__main__":
    visualize_data()