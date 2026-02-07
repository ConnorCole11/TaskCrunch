from pathlib import Path

LISTS_ROOT = Path("lists")


def get_task_file(folder_path: Path) -> Path:
    return folder_path / "tasks.txt"


def load_tasks(folder_path: Path) -> str:
    task_file = get_task_file(folder_path)
    if task_file.exists():
        return task_file.read_text()
    return ""


def save_tasks(folder_path: Path, text: str):
    task_file = get_task_file(folder_path)
    task_file.parent.mkdir(parents=True, exist_ok=True)
    task_file.write_text(text)
