import json
from os import path
import requests

target_db_file = path.join(path.dirname(__file__), "../data/open-router/models.json")


def sync_open_router_models():
    response = requests.get("https://openrouter.ai/api/v1/models")
    data = response.json()["data"]
    sorted_data = sorted(data, key=lambda x: x.get("id", ""))
    with open(target_db_file, "w") as f:
        json.dump(sorted_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    sync_open_router_models()
