# src/taskView/task_detail_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QLabel, QDateEdit,
    QPushButton
)
from PySide6.QtCore import QDate


class AttributeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_task = None

        self.layout = QVBoxLayout(self)

        # Title
        self.title_label = QLabel("Task Name")
        self.title_edit = QLineEdit()

        # Description
        self.desc_label = QLabel("Description")
        self.desc_edit = QTextEdit()

        # Deadline
        self.deadline_label = QLabel("Deadline")
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)

        # Save Button (optional if you want live editing instead)
        self.save_button = QPushButton("Save Changes")

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_edit)

        self.layout.addWidget(self.desc_label)
        self.layout.addWidget(self.desc_edit)

        self.layout.addWidget(self.deadline_label)
        self.layout.addWidget(self.deadline_edit)

        self.layout.addStretch()
        self.layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_changes)

    # Called when a task is selected
    def load_task(self, task):
        self.current_task = task

        if not task:
            self.clear()
            return

        self.title_edit.setText(task.name)
        self.desc_edit.setPlainText(task.description)

        if task.deadline:
            self.deadline_edit.setDate(
                QDate(task.deadline.year,
                      task.deadline.month,
                      task.deadline.day)
            )

    def save_changes(self):
        if not self.current_task:
            return

        self.current_task.name = self.title_edit.text()
        self.current_task.description = self.desc_edit.toPlainText()
        self.current_task.deadline = self.deadline_edit.date().toPyDate()

    def clear(self):
        self.title_edit.clear()
        self.desc_edit.clear()
