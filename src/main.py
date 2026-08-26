import sys
from PySide6.QtWidgets import QApplication
from src.window import MainWindow
import config
from pathlib import Path

Path(config.rootPath).expanduser().mkdir(parents=True, exist_ok=True)

app = QApplication(sys.argv)
window = MainWindow(config)
window.show()
sys.exit(app.exec())
