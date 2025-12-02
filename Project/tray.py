import os
from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QStyle,
)
from PySide6.QtGui import QAction, QIcon


class TrayIcon(QObject):
    """Small helper that encapsulates QSystemTrayIcon logic and menu."""

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.tray = None
        self.is_available = QSystemTrayIcon.isSystemTrayAvailable()
        if not self.is_available:
            return

        self.tray = QSystemTrayIcon(self.window)
        icon = self.window.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray.setIcon(icon)
        self.tray.setToolTip(self.window.windowTitle() or "Application")

        menu = QMenu(self.window)
        restore = QAction("Restore", self.window)
        quit_action = QAction("Exit", self.window)
        menu.addAction(restore)
        menu.addAction(quit_action)

        restore.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_activated)
        self.tray.show()

    def _on_activated(self, reason):
        # only toggle on explicit click/double-click; ignore hover/context events
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.toggle()

    def toggle(self):
        if self.window.isVisible():
            self.window.hide()
            self.window.killSignal.emit()
        else:
            self.show_window()

    def show_window(self):
        self.window.showNormal()
        self.window.raise_()
        self.window.activateWindow()

    def quit(self):
        # Hide the tray icon immediately
        if self.tray:
            try:
                self.tray.hide()
            except Exception:
                pass

        # First attempt a graceful Qt shutdown
        try:
            QApplication.quit()
        except Exception:
            pass

        # Ensure the whole Python process is terminated (kills all threads).
        # Use a short single-shot timer to give Qt a moment to process quit
        # before forcing the exit. os._exit exits immediately without cleanup,
        # which is desired here to guarantee termination of all threads.
        try:
            QTimer.singleShot(250, lambda: os._exit(0))
        except Exception:
            # As a very last resort, call os._exit synchronously
            os._exit(0)

    def show_message(self, title, text):
        if self.tray:
            # use information icon by default; desktop may suppress messages
            self.tray.showMessage(title, text)