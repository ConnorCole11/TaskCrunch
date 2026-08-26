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


class TasksView(QWidget):
    """
    Central task view.
    Uses shared AppState instead of owning its own data.
    """
    taskSelected = Signal(object)

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
        task_info = task_widget.task_info
        if task_info in self.state.tasks:
            self.state.tasks.remove(task_info)
            self.refresh_view()
            self.save()

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------

    def add_task_widget(self, task_info: Task):
        task_widget = TaskItem(task_info)

        task_widget.taskClicked.connect(self.handle_task_click)
        task_widget.remove_requested.connect(self.remove_task)

        self.task_layout.insertWidget(
            self.task_layout.count() - 1,
            task_widget,
        )

        task_widget.taskRemoved.connect(self.remove_task)

        return task_widget


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

    def apply_sort(self):
        pass

    def on_task_changed(self):
        """
        Reorders TaskItems immediately.
        Preserves selection.
        """
        if self.state.selected_task == None:
            return

        selected_task = self.state.selected_task

        # Sort tasks
        self.apply_sort()

        # Map each task to its existing widget
        task_to_widget = {}
        for i in range(self.task_layout.count()):
            w = self.task_layout.itemAt(i).widget()
            if isinstance(w, TaskItem):
                task_to_widget[w.task] = w

        # Reorder widgets in layout without clearing everything
        # Start from top, remove & reinsert in sorted order
        for i, task in enumerate(self.tasks):
            widget = task_to_widget.get(task)
            if widget:
                current_index = self.task_layout.indexOf(widget)
                if current_index != i:
                    self.task_layout.removeWidget(widget)
                    self.task_layout.insertWidget(i, widget)
                widget.refresh()
            else:
                # Only create new TaskItem for truly new tasks
                self.task_layout.insertWidget(i, self.add_task_widget(task))

        # Ensure stretch is at the bottom
        stretch_index = self.task_layout.count() - 1
        self.task_layout.addStretch(stretch_index)

        # Restore selection
        if selected_task:
            widget = task_to_widget.get(selected_task)
            if widget:
                self.handle_task_click(widget)

        # Save
        self.save()

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
