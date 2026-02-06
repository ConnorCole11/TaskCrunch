from pathlib import Path
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QScrollArea,
)
from PySide6.QtCore import Qt

from src.task_widgets import TaskItem
from src.filesystem import save_tasks


class TaskEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.current_path: Path | None = None

        layout = QVBoxLayout(self)

        # Scrollable task list
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.task_container)

        layout.addWidget(scroll)

        # Add-task input
        self.new_task_input = QLineEdit()
        self.new_task_input.setPlaceholderText("Add a new task…")
        self.new_task_input.returnPressed.connect(self.add_task)
        layout.addWidget(self.new_task_input)

    # -------- Public API used by MainWindow --------

    def load_text(self, text: str, path: Path):
        """Load tasks for the selected project/subproject"""
        self.current_path = path
        self.clear_tasks()

        for line in text.splitlines():
            self.add_task(line, save=False)

    def toPlainText(self) -> str:
        """Return tasks as newline-separated text"""
        tasks = []
        for i in range(self.task_layout.count()):
            widget = self.task_layout.itemAt(i).widget()
            if isinstance(widget, TaskItem):
                tasks.append(widget.checkbox.text())
        return "\n".join(tasks)

    # -------- Internal helpers --------

    def clear_tasks(self):
        while self.task_layout.count() > 1:
            item = self.task_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_task(self, text=None, save=True):
        if not self.current_path:
            return

        # Use the provided text or the input field
        text = text or self.new_task_input.text().strip()
        if not text:
            return  # nothing to add

        # Create the task widget
        task = TaskItem(text)
        # Connect the removed signal so the task disappears and updates the file
        task.removed.connect(self.remove_task)

        # Add to the layout (above the stretch)
        self.task_layout.insertWidget(0, task)

        # Clear the input field
        self.new_task_input.clear()

        # Save immediately if requested
        if save:
            self.save_tasks_to_file()

    def remove_task(self, task_widget):
        # Remove from layout
        self.task_layout.removeWidget(task_widget)
        task_widget.deleteLater()
        # Save the updated list
        self.save_tasks_to_file()

    def save_tasks_to_file(self):
        if not self.current_path:
            return

        tasks = []
        for i in range(self.task_layout.count()):
            widget = self.task_layout.itemAt(i).widget()
            if isinstance(widget, TaskItem):
                tasks.append(widget.checkbox.text())

        save_tasks(self.current_path, "\n".join(tasks))