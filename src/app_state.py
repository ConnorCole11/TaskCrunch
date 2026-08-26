from pathlib import Path
from src.taskView.Task import Task


class AppState:
    def __init__(self, task_root):
        self.selected_folder = task_root
        self.selected_task: Task | None = None
        self.sort_mode: str | None = None
        
        self.tasks: list[Task] = []
