from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QCheckBox,
    QLabel,
)

from PySide6.QtCore import Qt, Signal

from src.taskView.Task import Task
from src.app_state import AppState

class TaskItem(QWidget):
    """Describes a single task object widget."""

    remove_requested = Signal(Task)
    edit_requested = Signal(Task)
    taskClicked = Signal(object)
    taskRemoved = Signal(object)

    def __init__(self, task_info: Task):
        super().__init__()

        self.task_info = task_info

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

    def _create_widgets(self):
        self.checkbox = QCheckBox()
        self.name_label = QLabel(self.task_info.name)

    def _create_layouts(self):
        layout = QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.setContentsMargins(6, 2, 6, 2)

    def _connect_signals(self):
        self.checkbox.toggled.connect(self.handle_checkbox)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.taskClicked.emit(self)

        super().mousePressEvent(event)


    def handle_checkbox(self, checked: bool):
        if checked:
            self.taskRemoved.emit(self)