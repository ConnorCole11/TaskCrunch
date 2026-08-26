import unittest
from datetime import datetime
from PySide6.QtGui import QColor

from src.taskView.Task import Task


class TestTask(unittest.TestCase):

    def test_task_creation_defaults(self):
        task = Task(name="Test Task")

        self.assertEqual(task.name, "Test Task")
        self.assertIsNone(task.deadline)
        self.assertEqual(task.duration, None)
        self.assertEqual(task.basePriority, 1)
        self.assertEqual(task.attachments, [])

    def test_to_dict_and_from_dict(self):
        deadline = datetime(2026, 1, 1, 12, 0)

        task = Task(
            name="Test",
            deadline=deadline,
            duration=60,
            description="desc",
            color=QColor("#ff0000"),
            basePriority=5,
            attachments=["file.txt"],
            label="exam",
        )

        data = task.to_dict()
        new_task = Task.from_dict(data)

        self.assertEqual(new_task.name, task.name)
        self.assertEqual(new_task.deadline, task.deadline)
        self.assertEqual(new_task.duration, task.duration)
        self.assertEqual(new_task.description, task.description)
        self.assertEqual(new_task.basePriority, task.basePriority)
        self.assertEqual(new_task.attachments, task.attachments)
        self.assertEqual(new_task.label, task.label)

    def test_deadline_serialization_none(self):
        task = Task(name="No deadline")

        data = task.to_dict()
        self.assertIsNone(data["deadline"])

        new_task = Task.from_dict(data)
        self.assertIsNone(new_task.deadline)


if __name__ == "__main__":
    unittest.main()