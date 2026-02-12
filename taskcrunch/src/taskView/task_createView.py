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
from PySide6.QtWidgets import (
    QListWidget,
    QFileDialog,
)
from pathlib import Path
import shutil


class TaskCreationView(QDialog):
    """
    Dialog for creating or editing a Task.
    Mutates the provided Task object if accepted.
    """

    def __init__(
        self,
        task: Task,
        project_path: Path,
        parent=None,
    ):
        super().__init__(parent)
        self.task = task
        self.project_path = project_path

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

        # -------- Duration --------
        layout.addWidget(QLabel("Duration (minutes)"))
        self.duration_input = QSpinBox()
        self.duration_input.setMinimum(0)
        self.duration_input.setMaximum(24 * 60)
        self.duration_input.setValue(task.duration or 0)
        layout.addWidget(self.duration_input)

        # -------- Attachments --------
        layout.addWidget(QLabel("Attachments"))

        self.attachments_list = QListWidget()
        for attachment in task.attachments:
            self.attachments_list.addItem(attachment)

        layout.addWidget(self.attachments_list)

        attach_buttons = QHBoxLayout()

        add_attach_btn = QPushButton("Add")
        remove_attach_btn = QPushButton("Remove")

        add_attach_btn.clicked.connect(self.add_attachment)
        remove_attach_btn.clicked.connect(self.remove_attachment)

        attach_buttons.addWidget(add_attach_btn)
        attach_buttons.addWidget(remove_attach_btn)

        layout.addLayout(attach_buttons)

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
        self.task.name = self.name_input.text().strip()
        self.task.description = self.description_input.toPlainText().strip()
        self.task.deadline = self.deadline_input.dateTime().toPython()
        self.task.basePriority = self.priority_input.value()
        self.task.duration = self.duration_input.value() or None

        self.task.attachments = [
            self.attachments_list.item(i).text()
            for i in range(self.attachments_list.count())
        ]

        super().accept()


    def add_attachment(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Add Attachment",
            "",
            "All Files (*)",
        )

        if not file_path:
            return

        source = Path(file_path)
        dest_dir = self.attachments_dir()
        dest = dest_dir / source.name

        # Handle name collisions
        counter = 1
        while dest.exists():
            dest = dest_dir / f"{source.stem}_{counter}{source.suffix}"
            counter += 1

        shutil.copy2(source, dest)

        # Store relative path
        relative_path = dest.relative_to(self.project_path)
        self.attachments_list.addItem(str(relative_path))



    def remove_attachment(self):
        for item in self.attachments_list.selectedItems():
            self.attachments_list.takeItem(
                self.attachments_list.row(item)
            )

    def attachments_dir(self) -> Path:
        path = self.project_path / "attachments"
        path.mkdir(exist_ok=True)
        return path