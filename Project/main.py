import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
from chat_window import ChatWindow
from buddy_window import ShapedWindow
from test_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    chat_win = ChatWindow()

    buddy_win = ShapedWindow("cat")
    buddy_win.chatSignal.connect(chat_win.show)


    test_win = MainWindow()
    test_win.switchGif.connect(buddy_win.switch_gif)
    test_win.show()

    if QSystemTrayIcon.isSystemTrayAvailable():
        app.setQuitOnLastWindowClosed(False)
    
    buddy_win.show()

    sys.exit(app.exec())
