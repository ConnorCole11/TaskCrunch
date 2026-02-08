from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QIcon

from src.taskView.Task import Task


class TaskItem(QWidget):
    """
    UI representation of a single Task.
    Displays a checkbox, task name, and action buttons.
    """

    # Signals emitted upward to the TaskEditor / controller
    remove_requested = Signal(Task)
    edit_requested = Signal(Task)

    def __init__(self, task: Task):
        super().__init__()

        self.task = task

        # --- Main checkbox (task name) ---
        self.checkbox = QCheckBox(task.name)
        self.checkbox.stateChanged.connect(self.animate_removal)

        # --- Action buttons ---
        self.edit_button = QPushButton("✏️")
        self.delete_button = QPushButton("🗑")

        for btn in (self.edit_button, self.delete_button):
            btn.setFixedSize(24, 24)
            btn.setFlat(True)  # icon-style button

        self.edit_button.setToolTip("Edit task")
        self.delete_button.setToolTip("Delete task")

        self.edit_button.clicked.connect(
            lambda: self.edit_requested.emit(self.task)
        )
        self.delete_button.clicked.connect(
            lambda: self.remove_requested.emit(self.task)
        )

        # --- Layout ---
        layout = QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addStretch()  # pushes buttons to the right
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)

        layout.setContentsMargins(6, 2, 6, 2)

    # --- Animation for completed task ---
    def animate_removal(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.finished.connect(
            lambda: self.remove_requested.emit(self.task)
        )
        self.anim.start()
