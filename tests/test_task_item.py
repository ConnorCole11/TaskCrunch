import unittest
from PySide6.QtWidgets import QApplication
from src.taskView.task_widgets import TaskItem
from src.taskView.Task import Task

app = QApplication.instance() or QApplication([])


class TestTaskItem(unittest.TestCase):

    def test_checkbox_triggers_removal(self):
        task = Task(name="Test")
        item = TaskItem(task)

        triggered = []

        def on_remove(t):
            triggered.append(t)

        item.remove_requested.connect(on_remove)

        # Simulate checking the checkbox
        item.checkbox.setChecked(True)

        # Qt animations are async, so force finish
        item.anim.finished.emit()

        self.assertEqual(len(triggered), 1)
        self.assertEqual(triggered[0], task)


if __name__ == "__main__":
    unittest.main()