from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal, QObject, QEvent

from src.taskView.Task import Task
from src.app_state import AppState


class TaskClickFilter(QObject):
    """Event filter to make a TaskItem clickable for selection."""
    def __init__(self, state: AppState, item):
        super().__init__(item)
        self.state = state
        self.item = item

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress:
            if not isinstance(watched, (QPushButton, QCheckBox)):
                # ✅ update global state directly
                self.state.selected_task = self.item.task
        return False

class TaskItem(QWidget):
    """Describes a single task object widget."""

    remove_requested = Signal(Task)
    edit_requested = Signal(Task)

    def __init__(self, task: Task, state: AppState):
        super().__init__()

        self.task = task
        self.state = state

        # --- checkbox ---
        self.checkbox = QCheckBox()
        # self.checkbox.stateChanged.connect(self.animate_removal)

        # --- label ---
        self.name_label = QLabel(task.name)

        # --- layout ---
        layout = QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.setContentsMargins(6, 2, 6, 2)

        # --- click handling (single source of truth) ---
        self.click_filter = TaskClickFilter(state, self)
        self.installEventFilter(self.click_filter)

        for child in self.findChildren(QWidget):
            child.installEventFilter(self.click_filter)