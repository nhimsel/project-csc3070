from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QApplication
from PySide6.QtCore import QEvent, Qt, QRunnable, Slot, Signal, QThreadPool, QObject

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Window
from tray import TrayIcon
from openai import send_message


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Window()
        self.ui.setupUi(self)

        self.setWindowTitle("test")
        self.ui.textEdit.installEventFilter(self)
        self.ui.pushButton.clicked.connect(self.message_send)

        # create tray helper (it will be a no-op if system tray is unavailable)
        self.tray = TrayIcon(self)

    def message_send(self):
        self.ui.pushButton.setDisabled(True)
        input=self.ui.textEdit.toPlainText()
        #send_message(input, self.ui.textEdit_2)
        #self.ui.textEdit_2.setText(send_message(input))
        worker = message_worker(input)
        worker.signals.result.connect(self.restore_ui)
        QThreadPool.globalInstance().start(worker)

    def restore_ui(self, response):
        self.ui.textEdit_2.setText(response)
        self.ui.textEdit.clear()
        self.ui.pushButton.setEnabled(True)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self.ui.textEdit:
            if event.key() == Qt.Key.Key_Return and self.ui.textEdit.hasFocus():
                self.message_send()
        return super().eventFilter(obj,event)

    def closeEvent(self, event):
        # minimize to tray instead of quitting
        event.ignore()
        self.hide()

        # use tray helper to show an optional message
    ## this notification is kinda annoying.
        #if getattr(self, "tray", None) and self.tray.is_available:
        #    self.tray.show_message("test", "Application minimized to tray")

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                self.raise_()
                self.activateWindow()

    def quit_app(self):
        # hide tray icon before quitting
        self.tray_icon.hide()
        QApplication.quit()

class message_worker(QRunnable):
    def __init__(self, input):
        super().__init__()
        self.input= input
        self.signals = message_worker_signal()

    @Slot()
    def run(self):
        try:
            response = send_message(self.input)
            self.signals.result.emit(response)
        except Exception as e:
            self.signals.result.emit("error")

class message_worker_signal(QObject):
    result = Signal(str)