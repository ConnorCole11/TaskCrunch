from PySide6.QtWidgets import QWidget, QHBoxLayout, QCheckBox
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal


class TaskItem(QWidget):
    removed = Signal(QWidget)

    def __init__(self, text: str):
        super().__init__()

        self.checkbox = QCheckBox(text)
        self.checkbox.stateChanged.connect(self.animate_removal)

        layout = QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.setContentsMargins(5, 2, 5, 2)

    def animate_removal(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.finished.connect(lambda: self.removed.emit(self))
        self.anim.start()
