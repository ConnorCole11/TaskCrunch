import unittest
from pathlib import Path
from PySide6.QtWidgets import QApplication

from src.taskView.tasks_view import TasksView
from src.taskView.Task import Task

app = QApplication.instance() or QApplication([])


class TestTasksView(unittest.TestCase):

    def setUp(self):
        self.view = TasksView()
        self.view.current_path = Path("test_project")

    def test_add_task(self):
        self.view.new_task_input.setText("New Task")
        self.view.add_task_from_input()

        self.assertEqual(len(self.view.tasks), 1)
        self.assertEqual(self.view.tasks[0].name, "New Task")

    def test_remove_task(self):
        task = Task(name="Delete me")
        self.view.tasks.append(task)

        self.view.remove_task(task)

        self.assertNotIn(task, self.view.tasks)

    def test_clear_tasks(self):
        self.view.tasks = [Task(name="A"), Task(name="B")]
        self.view.refresh_view()

        self.assertEqual(len(self.view.tasks), 2)


if __name__ == "__main__":
    unittest.main()