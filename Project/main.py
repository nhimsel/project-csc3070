import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
from chat_window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()

    if QSystemTrayIcon.isSystemTrayAvailable():
        app.setQuitOnLastWindowClosed(False)
        win.hide()
    else:
        win.show()
    sys.exit(app.exec())
