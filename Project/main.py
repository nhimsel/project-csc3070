import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
from chat_window import ChatWindow
from buddy_window import ShapedWindow
from text_emotion_detector import EmotionHandler
from win32_window_parser import VideoScanner

if __name__ == "__main__":
    app = QApplication(sys.argv)

    emotions = EmotionHandler()
    videos = VideoScanner()

    chat_win = ChatWindow()
    chat_win.chat_response.connect(emotions.get_emotion)

    buddy_win = ShapedWindow()
    buddy_win.chatSignalMove.connect(chat_win.move_no_show)
    buddy_win.chatSignalShow.connect(chat_win.move_then_show)
    buddy_win.killSignal.connect(chat_win.close)

    emotions.swap_signal.connect(buddy_win.play_gif_once)
    videos.found.connect(buddy_win.switch_gif)
    videos.start()

    if QSystemTrayIcon.isSystemTrayAvailable():
        app.setQuitOnLastWindowClosed(False)
    
    buddy_win.show()

    sys.exit(app.exec())
