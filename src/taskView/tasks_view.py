from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QScrollArea,
)
from PySide6.QtCore import Signal

from src.taskView.task_widgets import TaskItem, TaskClickFilter
from src.taskView.Task import Task, TaskSerializer
from src.system.filesystem import load_tasks, save_tasks
from src.app_state import AppState


class TasksView(QWidget):
    """
    Central task view.
    Uses shared AppState instead of owning its own data.
    """
    taskSelected = Signal(object)

    def __init__(self, state: AppState):
        super().__init__()

        self.state = state 

        layout = QVBoxLayout(self)

        # --- Scrollable task list ---
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.task_container)

        layout.addWidget(scroll)

        # --- Add-task input ---
        self.new_task_input = QLineEdit()
        self.new_task_input.setPlaceholderText("Add a new task…")
        self.new_task_input.returnPressed.connect(self.add_task_from_input)
        layout.addWidget(self.new_task_input)

        # UI-only state stays local
        self.selected_task_item: TaskItem | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def handle_task_click(self, clicked_item: TaskItem):
        if self.selected_task_item and not self.selected_task_item.isHidden():
            self.selected_task_item.setStyleSheet("")

        clicked_item.setStyleSheet("background-color: lightblue;")
        self.selected_task_item = clicked_item

        # ✅ update shared state
        self.state.selected_task = clicked_item.task

        self.taskSelected.emit(clicked_item.task)

    def load_tasks_from_path(self, path: Path):
        """Load tasks for the selected project/subproject."""

        # ✅ update shared state
        self.state.selected_folder = path
        self.state.selected_task = None

        self.selected_task_item = None
        self.clear_tasks()

        data = load_tasks(path) or {}

        # ✅ store in shared state
        self.state.tasks = [
            TaskSerializer.from_dict(task_data)
            for task_data in data.get("tasks", [])
        ]

        for task in self.state.tasks:
            self.add_task_widget(task)
        

    # ------------------------------------------------------------------
    # Task creation / removal
    # ------------------------------------------------------------------

    def add_task_from_input(self):
        if not self.state.selected_folder:
            return

        name = self.new_task_input.text().strip()
        if not name:
            return

        task = Task(name=name)

        # ✅ update shared state
        self.state.tasks.append(task)

        new_item = self.add_task_widget(task)
        self.handle_task_click(new_item)

        self.new_task_input.clear()
        self.save()

    def remove_task(self, task: Task):
        if task in self.state.tasks:
            self.state.tasks.remove(task)
            self.refresh_view()
            self.save()

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------

    def add_task_widget(self, task: Task):
        item = TaskItem(task, self.state)

        item.remove_requested.connect(self.remove_task)

        filter = TaskClickFilter(self, item)
        item.installEventFilter(filter)
        for child in item.findChildren(QWidget):
            child.installEventFilter(filter)

        self.task_layout.insertWidget(
            self.task_layout.count() - 1,
            item,
        )
        return item

    def refresh_view(self):
        self.selected_task_item = None
        self.clear_tasks()

        for task in self.state.tasks:
            self.add_task_widget(task)

    def clear_tasks(self):
        while self.task_layout.count() > 1:
            item = self.task_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self):
        if not self.state.selected_folder:
            return

        data = {
            "tasks": [TaskSerializer.to_dict(task) for task in self.state.tasks]
        }

        save_tasks(self.state.selected_folder, data)