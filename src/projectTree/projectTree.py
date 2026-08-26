from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QInputDialog, QMessageBox
)
from PySide6.QtCore import Signal
from pathlib import Path
import shutil

from src.app_state import AppState


class ProjectTree(QWidget):
    project_selected = Signal(Path)

    def __init__(self, config, state: AppState):
        super().__init__()
        self.config = config
        self.state = state  # ✅ shared state

        self.STORAGE_FOLDER = "Tasks"
        self.LISTS_ROOT = Path(self.config.rootPath).expanduser() / self.STORAGE_FOLDER

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

        self.populate()

    def _create_widgets(self):
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)

        self.add_button = QPushButton("+ Add Folder")
        self.remove_button = QPushButton("- Remove Folder")

    def _create_layouts(self):
        folder_buttons = QHBoxLayout()
        folder_buttons.addWidget(self.add_button)
        folder_buttons.addWidget(self.remove_button)
        folder_buttons.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(folder_buttons)
        layout.addWidget(self.tree)

    def _connect_signals(self):
        self.tree.itemClicked.connect(self.on_item_clicked)
        self.add_button.clicked.connect(self.add_folder)
        self.remove_button.clicked.connect(self.remove_folder)
        

    # ------------------------------------------------------------------
    # Selection handling
    # ------------------------------------------------------------------

    def on_item_clicked(self, item: QTreeWidgetItem):
        path = item.data(0, 1)

        # ✅ update shared state
        self.state.selected_folder = path
        self.state.selected_task = None  # reset selection

        self.project_selected.emit(Path(path))

    # ------------------------------------------------------------------
    # TREE POPULATION
    # ------------------------------------------------------------------

    def populate(self):
        expanded_paths = self.get_expanded_paths()
        self.tree.clear()

        root_item = self._build_item(self.LISTS_ROOT)
        root_item.setText(0, self.STORAGE_FOLDER)

        self.tree.addTopLevelItem(root_item)
        root_item.setExpanded(True)

        self.restore_expanded_state(expanded_paths)

    def _build_item(self, path: Path) -> QTreeWidgetItem:
        item = QTreeWidgetItem([path.name])
        item.setData(0, 1, path)

        for child in sorted(path.iterdir()):
            if child.is_dir():
                item.addChild(self._build_item(child))

        return item

    # ------------------------------------------------------------------
    # Folder operations
    # ------------------------------------------------------------------

    def add_folder(self):
        selected = self.tree.currentItem()
        parent_path = selected.data(0, 1) if selected else self.LISTS_ROOT

        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if not ok or not name.strip():
            return

        new_folder = parent_path / name.strip()
        new_folder.mkdir(exist_ok=True)

        self.populate()
        self.select_path(new_folder, expand_parent=True)

    def remove_folder(self):
        selected = self.tree.currentItem()
        if not selected:
            return

        path = selected.data(0, 1)

        if path == self.LISTS_ROOT:
            QMessageBox.warning(self, "Cannot remove root", "Cannot remove the root folder.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{path.name}' and all its contents?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            shutil.rmtree(path)

            # ✅ clear state if deleted folder was selected
            if self.state.selected_folder == path:
                self.state.selected_folder = None
                self.state.selected_task = None

            self.populate()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_expanded_paths(self):
        expanded = set()

        def recurse(item: QTreeWidgetItem):
            path = item.data(0, 1)
            if item.isExpanded():
                expanded.add(path)
            for i in range(item.childCount()):
                recurse(item.child(i))

        for i in range(self.tree.topLevelItemCount()):
            recurse(self.tree.topLevelItem(i))

        return expanded

    def restore_expanded_state(self, expanded_paths):
        def recurse(item: QTreeWidgetItem):
            path = item.data(0, 1)
            if path in expanded_paths:
                item.setExpanded(True)
            for i in range(item.childCount()):
                recurse(item.child(i))

        for i in range(self.tree.topLevelItemCount()):
            recurse(self.tree.topLevelItem(i))

    def select_path(self, path: Path, expand_parent=False):
        def recurse(item: QTreeWidgetItem, parent=None):
            if item.data(0, 1) == path:
                self.tree.setCurrentItem(item)

                # ✅ update state when selecting programmatically
                self.state.selected_folder = path
                self.state.selected_task = None

                if expand_parent and parent:
                    parent.setExpanded(True)
                return True

            for i in range(item.childCount()):
                if recurse(item.child(i), parent=item):
                    return True
            return False

        for i in range(self.tree.topLevelItemCount()):
            if recurse(self.tree.topLevelItem(i)):
                break