import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt

TODO_FILE = "todos.txt"


def load_todos():
    try:
        with open(TODO_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def save_todos():
    with open(TODO_FILE, "w") as f:
        f.write(text.toPlainText())

    QMessageBox.information(window, "Saved", "Your to-do list was saved!")


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("📝 To-Do List")
window.resize(400, 300)

layout = QVBoxLayout(window)

text = QTextEdit()
text.setPlainText(load_todos())
layout.addWidget(text)

save_button = QPushButton("Save")
save_button.clicked.connect(save_todos)
layout.addWidget(save_button)

window.setLayout(layout)
window.show()

sys.exit(app.exec())
