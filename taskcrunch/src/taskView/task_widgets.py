from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal, QObject, QEvent
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QPushButton, QCheckBox

from src.taskView.Task import Task

class TaskClickFilter(QObject):
    """Event filter to make a TaskItem clickable for selection."""
    def __init__(self, view, item):
        super().__init__(item)
        self.view = view
        self.item = item

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress:
            # Only trigger if click is NOT on a button or checkbox
            if not isinstance(watched, (QPushButton, QCheckBox)):
                self.view.handle_task_click(self.item)
        return False  # Let event continue normally

class TaskItem(QWidget):
    """Describes a single task object widget."""
    remove_requested = Signal(Task)
    edit_requested = Signal(Task)

    def __init__(self, task: Task):
        super().__init__()
        self.task = task

        # --- Separate checkbox (for completion) ---
        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self.animate_removal)

        # --- Label for the task name (clickable for selection) ---
        self.name_label = QLabel(task.name)

        # --- Action buttons ---
        self.edit_button = QPushButton("✏️")
        self.delete_button = QPushButton("🗑")
        for btn in (self.edit_button, self.delete_button):
            btn.setFixedSize(24, 24)
            btn.setFlat(True)
        self.edit_button.setToolTip("Edit task")
        self.delete_button.setToolTip("Delete task")
        self.edit_button.clicked.connect(lambda: self.edit_requested.emit(self.task))
        self.delete_button.clicked.connect(lambda: self.remove_requested.emit(self.task))

        # --- Layout ---
        layout = QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        layout.setContentsMargins(6, 2, 6, 2)

    def animate_removal(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.finished.connect(lambda: self.remove_requested.emit(self.task))
        self.anim.start()

