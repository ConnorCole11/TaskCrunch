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
    grey = QColor(128, 128, 128)
    defaultDescript = "No description provided."

    def __init__(
        self,
        name: str,
        deadline: datetime | None = None,
        duration: int | None = None,  # duration in minutes
        description: str = defaultDescript,
        color: QColor = grey,
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

    def to_dict(self):
        return {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "duration": self.duration,
            "priority": self.basePriority,
            "color": self.color.name(),
            "attachments": self.attachments,
        }

    @staticmethod
    def from_dict(data: dict):
        return Task(
            name=data.get("name"),
            label=data.get("label"),
            description=data.get("description"),
            deadline=datetime.fromisoformat(data["deadline"])
            if data.get("deadline")
            else None,
            duration=data.get("duration"),
            basePriority=data.get("priority", 1),
            color=QColor(data.get("color", "#808080")),
            attachments=data.get("attachments", []),
        )