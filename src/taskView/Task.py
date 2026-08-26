from datetime import datetime
from PySide6.QtGui import QColor
from pathlib import Path
from typing import List

class Task:
    """
    Task is a class that defines the task object used in this app. All attributes are optional, but apply additional 
    perks such as priority setting, letting the user apply their color code, allowing attachments such as images or links,
    and marking things as exams, projects, etc.

    Parameters
    ----------
    name : str
        The name of the task.
    deadline : 
        The year, month, day, and time that something is due. 
    duration : 
        The time predicted for the task to take. Measured in hours or minutes float.
    description : str
        A description created by the user describing the task.
    color: str (?)
        The color selected by the user for the task.
    priority : int
        A value representing the initial importance of the task. This value will be adjusted by
        things such as proximity to its deadline, if provided. Higher priority is a higher value.
        The minimal priority value is 1.
    atttachments : str
        A string representing either the path to an attachment (image, video, etc) or a link to
        a website.
    laebl : str
        A shorter description, such as 'exam' or 'project.' May be present or custom.
    """

    defaultDescript = "No description provided."

    def __init__(
        self,
        name: str,
        deadline: datetime | None = None,
        duration: int | None = None,  # duration in minutes
        description: str = defaultDescript,
        color: str = "#RRGGBB",
        basePriority: int = 1,
        attachments: List[str] | None = None,
        label: str | None = None,
    ):
        self.name = name
        self.deadline = deadline
        self.duration = duration
        self.description = description
        self.color = color
        self.basePriority = basePriority
        self.attachments = attachments or []
        self.label = label





class TaskSerializer:

    @staticmethod
    def to_dict(task: Task) -> dict:
        return {
            "name": task.name,
            "label": task.label,
            "description": task.description,
            "deadline": task.deadline.isoformat() if task.deadline else None,
            "duration": task.duration,
            "priority": task.basePriority,
            "color": task.color,
            "attachments": task.attachments,
        }

    @staticmethod
    def from_dict(data: dict) -> Task:
        return Task(
            name=data["name"],
            label=data.get("label"),
            description=data.get("description"),
            deadline=datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None,
            duration=data.get("duration"),
            basePriority=data.get("priority", 1),
            color=data.get("color", "#808080"),
            attachments=data.get("attachments", []),
        )