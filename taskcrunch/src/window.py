from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget,
    QTreeWidgetItem, QPushButton, QLineEdit, QMessageBox,
    QScrollArea
)
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter, QPushButton, QVBoxLayout
from src.projectTree.projectTree import ProjectTree
from src.taskView.tasks_view import TasksView
from src.system.Config import Config
from src.attributeView.attributeView import AttributeView

config = Config()

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
        self.setWindowTitle("📝 To-Do List")
        self.resize(1200, 500)

        self.tree = ProjectTree(config)
        self.editor = TasksView()
        self.attributes = AttributeView()

        self.tree.itemClicked.connect(self.on_item_clicked)

        # Effective Hstacks the tree, editor, and attributes
        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.attributes)
        splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(splitter)



        

    def on_item_clicked(self, item):
        path = item.data(0, 1)
        self.editor.load_tasks_from_path(path)

