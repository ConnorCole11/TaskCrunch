from datetime import datetime

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QColorDialog,
    QSpinBox,
    QDateTimeEdit,
)
from PySide6.QtGui import QColor

from src.taskView.Task import Task


class TaskCreateDialog(QDialog):
    """
    Dialog for creating or editing a Task.
    Mutates the provided Task object if accepted.
    """

    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.task = task

        self.setWindowTitle("Edit Task")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        # -------- Name --------
        layout.addWidget(QLabel("Name"))
        self.name_input = QLineEdit(task.name or "")
        layout.addWidget(self.name_input)

        # -------- Description --------
        layout.addWidget(QLabel("Description"))
        self.description_input = QTextEdit(task.description or "")
        layout.addWidget(self.description_input)

        # -------- Deadline --------
        layout.addWidget(QLabel("Deadline"))
        self.deadline_input = QDateTimeEdit()
        self.deadline_input.setCalendarPopup(True)

        if task.deadline:
            self.deadline_input.setDateTime(task.deadline)
        else:
            self.deadline_input.setDateTime(datetime.now())

        layout.addWidget(self.deadline_input)

        # -------- Priority --------
        layout.addWidget(QLabel("Priority"))
        self.priority_input = QSpinBox()
        self.priority_input.setMinimum(1)
        self.priority_input.setMaximum(10)
        self.priority_input.setValue(task.basePriority or 1)
        layout.addWidget(self.priority_input)

        # -------- Color --------
        color_row = QHBoxLayout()
        self.color_preview = QPushButton()
        self.color_preview.setFixedSize(24, 24)
        self.set_color(task.color or QColor("#808080"))

        self.color_button = QPushButton("Choose color")
        self.color_button.clicked.connect(self.choose_color)

        color_row.addWidget(self.color_preview)
        color_row.addWidget(self.color_button)
        layout.addLayout(color_row)

        # -------- Buttons --------
        buttons = QHBoxLayout()
        buttons.addStretch()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        buttons.addWidget(cancel_btn)
        buttons.addWidget(save_btn)
        layout.addLayout(buttons)

    # ------------------------------------------------------------------

    def choose_color(self):
        color = QColorDialog.getColor(self.task.color, self)
        if color.isValid():
            self.set_color(color)

    def set_color(self, color: QColor):
        self.task.color = color
        self.color_preview.setStyleSheet(
            f"background-color: {color.name()};"
        )

    # ------------------------------------------------------------------

    def accept(self):
        """Apply UI values back into the Task object."""
        self.task.name = self.name_input.text().strip()
        self.task.description = self.description_input.toPlainText().strip()
        self.task.deadline = self.deadline_input.dateTime().toPython()
        self.task.basePriority = self.priority_input.value()

        super().accept()
