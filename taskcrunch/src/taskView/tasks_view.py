from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QScrollArea,
)
from PySide6.QtCore import Signal

from src.taskView.task_widgets import TaskItem, TaskClickFilter
from src.taskView.Task import Task
# from src.taskView.task_createView import TaskCreationView
from src.system.filesystem import load_tasks, save_tasks


class TasksView(QWidget):
    """
    Central task view.
    Owns the in-memory Task objects for the currently selected folder.
    """
    taskSelected = Signal(object)
    def __init__(self):
        super().__init__()

        self.current_path: Path | None = None
        self.tasks: list[Task] = []

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

        # Used to identify task to be highlighted
        self.selected_task_item: TaskItem | None = None

        

    # ------------------------------------------------------------------
    # Public API (called by MainWindow)
    # ------------------------------------------------------------------
    def handle_task_click(self, clicked_item: Task):
        # Unhighlight previous
        if self.selected_task_item:
            self.selected_task_item.setStyleSheet("")  # Reset style

        # Highlight new
        clicked_item.setStyleSheet("background-color: lightblue;")  # Example
        self.selected_task_item = clicked_item

        # Emit the task object as before
        self.taskSelected.emit(clicked_item.task)

    def load_tasks_from_path(self, path: Path):
        """Load tasks for the selected project/subproject."""
        self.current_path = path
        self.clear_tasks()

        data = load_tasks(path) or {}
        self.tasks = [
            Task.from_dict(task_data)
            for task_data in data.get("tasks", [])
        ]

        for task in self.tasks:
            self.add_task_widget(task)

    # ------------------------------------------------------------------
    # Task creation / removal / editing
    # ------------------------------------------------------------------

    def add_task_from_input(self):
        """Quick-create a task using only the name."""
        if not self.current_path:
            return

        name = self.new_task_input.text().strip()
        if not name:
            return

        task = Task(name=name)
        self.tasks.append(task)

        new_item = self.add_task_widget(task)
        self.handle_task_click(new_item)
        self.new_task_input.clear()
        self.save()

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)
            self.refresh_view()
            self.save()

    # def edit_task(self, task: Task):
    #     """Open dialog to edit an existing task."""
    #     dialog = TaskCreationView(
    #         task,
    #         project_path=self.current_path,
    #         parent=self,
    #         )

    #     if dialog.exec():
    #         # task is already mutated
    #         self.refresh_view()
    #         self.save()

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------

    def add_task_widget(self, task: Task):
        item = TaskItem(task)

        item.remove_requested.connect(self.remove_task)
        # item.edit_requested.connect(self.edit_task)

        # --- Event filter for clickable selection ---
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
        self.selected_task_item = None  # clear previous selection
        self.clear_tasks()
        for task in self.tasks:
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
        if not self.current_path:
            return

        data = {
            "tasks": [task.to_dict() for task in self.tasks]
        }
        save_tasks(self.current_path, data)
