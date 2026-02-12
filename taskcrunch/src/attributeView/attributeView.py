from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QLabel, QDateEdit,
    QPushButton, QSpinBox, QListWidget,
    QHBoxLayout, QFileDialog
)
from PySide6.QtCore import QDate


class AttributeView(QWidget):
    taskUpdated = Signal(object)
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

        self.save_button.clicked.connect(self.save_changes)

        # ----- Priority -----
        self.priority_label = QLabel("Priority")
        self.priority_spin = QSpinBox()
        self.priority_spin.setMinimum(1)
        self.priority_spin.setMaximum(10)

        # ----- Duration -----
        self.duration_label = QLabel("Duration (minutes)")
        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(0)
        self.duration_spin.setMaximum(24 * 60)  # full day in minutes

        # ----- Attachments -----
        self.attach_label = QLabel("Attachments")
        self.attach_list = QListWidget()

        attach_buttons = QHBoxLayout()
        self.add_attach_btn = QPushButton("Add")
        self.remove_attach_btn = QPushButton("Remove")
        attach_buttons.addWidget(self.add_attach_btn)
        attach_buttons.addWidget(self.remove_attach_btn)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_edit)

        self.layout.addWidget(self.deadline_label)
        self.layout.addWidget(self.deadline_edit)

        self.layout.addWidget(self.priority_label)
        self.layout.addWidget(self.priority_spin)

        self.layout.addWidget(self.duration_label)
        self.layout.addWidget(self.duration_spin)

        self.layout.addWidget(self.desc_label)
        self.layout.addWidget(self.desc_edit)

        self.layout.addWidget(self.attach_label)
        self.layout.addWidget(self.attach_list)
        self.layout.addLayout(attach_buttons)
        
        self.layout.addStretch()
        self.layout.addWidget(self.save_button)

        self.add_attach_btn.clicked.connect(self.add_attachment)
        self.remove_attach_btn.clicked.connect(self.remove_attachment)

    # Called when a task is selected
    def load_task(self, task):
        self.current_task = task

        if not task:
            self.clear()
            return

        self.title_edit.setText(task.name)
        self.desc_edit.setPlainText(task.description)

        if task.deadline:
            self.deadline_edit.setDate(QDate(task.deadline.year,
                                            task.deadline.month,
                                            task.deadline.day))

        # ----- New fields -----
        self.priority_spin.setValue(task.basePriority or 1)
        self.duration_spin.setValue(task.duration or 0)

        self.attach_list.clear()
        for attachment in task.attachments:
            self.attach_list.addItem(attachment)


    def save_changes(self):
        if not self.current_task:
            return

        self.current_task.name = self.title_edit.text()
        self.current_task.description = self.desc_edit.toPlainText()

        qdate = self.deadline_edit.date()
        self.current_task.deadline = qdate.toPython()

        # ----- New fields -----
        self.current_task.basePriority = self.priority_spin.value()
        self.current_task.duration = self.duration_spin.value()
        self.current_task.attachments = [
            self.attach_list.item(i).text()
            for i in range(self.attach_list.count())
        ]

        # Emit signal for TasksView to refresh/save
        self.taskUpdated.emit(self.current_task)

    def add_attachment(self):
        if not self.current_task:
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Add Attachment", "", "All Files (*)")
        if not file_path:
            return

        self.attach_list.addItem(file_path)
        self.save_changes()  # optional: save immediately

    def remove_attachment(self):
        for item in self.attach_list.selectedItems():
            self.attach_list.takeItem(self.attach_list.row(item))
        self.save_changes()

    def clear(self):
        self.title_edit.clear()
        self.desc_edit.clear()
        self.deadline_edit.setDate(QDate.currentDate())
        self.priority_spin.setValue(1)
        self.duration_spin.setValue(0)
        self.attach_list.clear()