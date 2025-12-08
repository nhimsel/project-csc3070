from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from settings_window import SettingsUI

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Settings Editor")
window.setCentralWidget(SettingsUI("config.json"))
window.resize(400, 300)
window.show()

sys.exit(app.exec())

