from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QScrollArea,
    QDialog
)
from PySide6.QtCore import Signal

from src.taskView.task_widgets import TaskItem
from src.taskView.Task import Task, TaskSerializer
from src.system.filesystem import load_tasks, save_tasks
from src.app_state import AppState

from datetime import date, datetime

class TasksView(QWidget):
    """
    Central task view.
    Uses shared AppState instead of owning its own data.
    """
    taskSelected = Signal(Task)

    def __init__(self, state: AppState):
        super().__init__()

        self.state = state 

        # Default settings
        self.sort_mode = "deadline"
        self.sort_reverse = False

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

    def _create_widgets(self):
        self.task_container = QWidget()
        self.new_task_input = QLineEdit()
        self.new_task_input.setPlaceholderText("Add a new task…")

    def _create_layouts(self):
        layout = QVBoxLayout(self)
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.task_container)

        layout.addWidget(scroll)
        layout.addWidget(self.new_task_input)

    def _connect_signals(self):
        self.new_task_input.returnPressed.connect(self.add_task_from_input)
        
 

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def handle_task_click(self, clicked_item: TaskItem):
        """Called when a task is clicked."""

        # Unhighlight previous task
        if self.selected_task_item:
            self.selected_task_item.setStyleSheet("")

        # Remember the new selection
        self.selected_task_item = clicked_item
        self.state.selected_task = clicked_item.task_info

        # Highlight new task
        clicked_item.setStyleSheet("background-color: lightblue;")

        # Notify the rest of the application
        self.taskSelected.emit(clicked_item.task_info)

    # def load_tasks_from_path(self, path: Path):
    #     """Load tasks for the selected project and all subprojects."""

    #     self.state.selected_folder = path
    #     self.state.selected_task = None

    #     self.selected_task_item = None
    #     self._clear_tasks()

    #     self.state.tasks = []

    #     # Include the selected folder itself
    #     folders = [path]

    #     # Include all subproject folders recursively
    #     folders.extend(p for p in path.rglob("*") if p.is_dir())

    #     for folder in folders:
    #         data = load_tasks(folder) or {}

    #         for task_data in data.get("tasks", []):
    #             task = TaskSerializer.from_dict(task_data)
    #             self.state.tasks.append(task)
    #             self.add_task_widget(task)

    def load_tasks_from_path(self, path: Path):
        """Load tasks for the selected project and all subprojects."""

        self.state.selected_folder = path
        self.state.selected_task = None

        self.selected_task_item = None
        self._clear_tasks()

        self.state.tasks = []

        # Include the selected folder itself
        folders = [path]

        # Include all subproject folders recursively
        folders.extend(
            p for p in path.rglob("*")
            if p.is_dir()
        )

        # Load tasks from every folder
        for folder in folders:
            data = load_tasks(folder) or {}

            for task_data in data.get("tasks", []):
                task = TaskSerializer.from_dict(task_data)
                self.state.tasks.append(task)

        # Sort all loaded tasks
        self.apply_sort()

        # Create widgets in sorted order
        for task in self.state.tasks:
            self.add_task_widget(task)
        

    # ------------------------------------------------------------------
    # Task creation / removal
    # ------------------------------------------------------------------

    def add_task_from_input(self):
        """Creates a task object after the user enters a taskname."""
        if not self.state.selected_folder:
            return

        name = self.new_task_input.text().strip()
        if not name:
            return

        task_info = Task(name=name)

        # ✅ update shared state
        self.state.tasks.append(task_info)

        task_widget = self.add_task_widget(task_info)
        self.handle_task_click(task_widget)

        self.new_task_input.clear()
        self.save()

    def remove_task(self, task_widget: TaskItem):
        """Removes task data, and task widget"""
        task_info = task_widget.task_info
        if task_info in self.state.tasks:
            self.state.tasks.remove(task_info)
            self.refresh_view()
            self.save()

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------

    def add_task_widget(self, task_info: Task):
        """Takes task info and creates a task widget"""
        task_widget = TaskItem(task_info)

        task_widget.taskClicked.connect(self.handle_task_click)
        task_widget.remove_requested.connect(self.remove_task)

        self.task_layout.insertWidget(
            self.task_layout.count() - 1,
            task_widget,
        )

        task_widget.taskRemoved.connect(self.remove_task)

        return task_widget

    def _clear_tasks(self):
        """Removes all task widgets"""
        while self.task_layout.count() > 1:
            item = self.task_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def refresh_view(self):
        """Clears all tasks and adds back what is saved in the saved data files"""
        self.selected_task_item = None
        self._clear_tasks()

        self.apply_sort()
        for task in self.state.tasks:
            self.add_task_widget(task)

    def apply_sort(self):
        if self.sort_mode == "deadline":
            self.state.tasks.sort(
                key=lambda task: (
                    task.deadline.date()
                    if isinstance(task.deadline, datetime)
                    else task.deadline
                ) if task.deadline else date.max,
                reverse=self.sort_reverse
            )

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
