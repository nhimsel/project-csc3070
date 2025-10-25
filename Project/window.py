import sys

from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QApplication
from PySide6.QtGui import QIcon

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Window
from tray import TrayIcon


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Window()
        self.ui.setupUi(self)

        self.setWindowTitle("test")
        self.ui.lineEdit.textChanged.connect(self.sync_tex)

        # create tray helper (it will be a no-op if system tray is unavailable)
        self.tray = TrayIcon(self)

    def sync_tex(self):
        if self.ui.lineEdit.text() != self.ui.lineEdit_2.text():
            self.ui.lineEdit_2.setText(self.ui.lineEdit.text())

    def closeEvent(self, event):
        # minimize to tray instead of quitting
        event.ignore()
        self.hide()
        # use tray helper to show an optional message
        if getattr(self, "tray", None) and self.tray.is_available:
            self.tray.show_message("test", "Application minimized to tray")

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
