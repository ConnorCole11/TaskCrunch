from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget,
    QTreeWidgetItem, QPushButton, QLineEdit, QMessageBox,
    QScrollArea
)
from src.taskView.task_widgets import TaskItem
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter, QPushButton, QVBoxLayout
from src.projectTree.sidebar import ProjectTree
from src.taskView.tasks_view import TaskEditor
from src.system.filesystem import load_tasks, save_tasks


class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("📝 To-Do List")
        self.resize(800, 500)

        self.tree = ProjectTree(config)
        self.editor = TaskEditor()

        self.tree.itemClicked.connect(self.on_item_clicked)

        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.editor)
        splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

    def on_item_clicked(self, item):
        path = item.data(0, 1)
        text = load_tasks(path)
        self.editor.load_text(text, path)
