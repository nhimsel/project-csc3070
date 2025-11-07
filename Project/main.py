import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
#from chat_window import Window
from buddy_window import ShapedWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ShapedWindow("feesh")

    if QSystemTrayIcon.isSystemTrayAvailable():
        app.setQuitOnLastWindowClosed(False)
        #win.hide()
        win.show()
    else:
        win.show()
    sys.exit(app.exec())
