from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget,
    QTreeWidgetItem, QPushButton, QLineEdit, QMessageBox,
    QScrollArea
)
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter, QPushButton, QVBoxLayout
from src.projectTree.projectTree import ProjectTree
from src.taskView.tasks_view import TasksView
import config
from src.attributeView.attributeView import AttributeView
from src.taskView.Task import Task
from src.app_state import AppState

from pathlib import Path

class MainWindow(QWidget):
    """
    The overall window for the task manager. 

    Parameters
    ----------
    config : Config
        A Config object that holds the path to the Tasks folder that holds task information.

    Attributes
    ----------
    layout : QVBoxLayout
        A layout that 
    tree : ProjectTree
        A ProjectTree object, which represents the left-most view of the task manager. It shows
        a list of projects that hold tasks.
    editor : TasksView
        A TasksView object that represents the middle view of the task manager. It shows
        a list of tasks within the project selected in the tree.
    splitter : QSplitter
        A QSplitter object that acts as an hstack, separating each subwindow.
    layout : QVBoxLayout
        A QVBoxLayout object. This doens't do anything yet, just makes splitter expandable upon.
    """
    def __init__(self, config):
        super().__init__()
        task_root = Path(config.rootPath) / "Tasks"
        self.app_state = AppState(task_root)

        self.setWindowTitle("📝 To-Do List")
        self.resize(1200, 500)

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()


    def _create_widgets(self):
        self.project_tree = ProjectTree(config, self.app_state)
        self.taskview = TasksView(self.app_state)
        self.attributes = AttributeView()

    def _create_layouts(self):
        splitter = QSplitter()
        splitter.addWidget(self.project_tree)
        splitter.addWidget(self.taskview)
        splitter.addWidget(self.attributes)
        splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

    def _connect_signals(self):
        self.taskview.taskSelected.connect(self.attributes.load_task)
        self.attributes.taskUpdated.connect(self.taskview.refresh_view)
        self.attributes.taskUpdated.connect(lambda _: self.taskview.save())
        self.project_tree.project_selected.connect(self.taskview.load_tasks_from_path)

    def on_item_clicked(self, item):
        path = item.data(0, 1)
        self.taskview.load_tasks_from_path(path)
