import json
from pathlib import Path


def load_tasks(path: Path) -> dict:
    path.mkdir(parents=True, exist_ok=True)
    file = path / "tasks.json"

    if not file.exists():
        return {"tasks": []}

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(path: Path, data: dict):
    path.mkdir(parents=True, exist_ok=True)
    file = path / "tasks.json"

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
