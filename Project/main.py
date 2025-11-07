import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
#from chat_window import Window
from buddy_window import ShapedWindow
from test_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ShapedWindow("feesh")

    test_win = MainWindow()
    test_win.switchGif.connect(win.switch_gif)
    test_win.show()

    if QSystemTrayIcon.isSystemTrayAvailable():
        app.setQuitOnLastWindowClosed(False)
        #win.hide()
        win.show()
    else:
        win.show()
    
    sys.exit(app.exec())
