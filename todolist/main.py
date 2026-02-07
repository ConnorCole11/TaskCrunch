import sys
from PySide6.QtWidgets import QApplication
from src.window import MainWindow
from src.system.Config import Config
from pathlib import Path

config = Config()
Path(config.taskPath).mkdir(parents=True, exist_ok=True)

app = QApplication(sys.argv)
window = MainWindow(config)
window.show()
sys.exit(app.exec())
