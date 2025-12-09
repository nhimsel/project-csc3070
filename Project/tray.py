from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSystemTrayIcon,
    QMenu,
    QStyle,
    QDialog,
    QVBoxLayout,
)
from PySide6.QtGui import QAction, QIcon
from settings_window import SettingsUI


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
        self.tray.setToolTip(self.window.windowTitle() or "Buddy")

        self.menu = QMenu(self.window)
        self.restore = QAction("Restore", self.window)
        self.settings = QAction("Settings", self.window)
        self.quit_action = QAction("Exit", self.window)
        
        self.menu.addAction(self.restore)
        self.menu.addAction(self.settings)
        self.menu.addAction(self.quit_action)

        self.restore.triggered.connect(self.show_window)
        self.settings.triggered.connect(self.show_settings)
        self.quit_action.triggered.connect(self.quit)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self._on_activated)
        self.tray.show()

        # **NEW**: Initially update the restore action visibility based on the window state
        self.update_restore_action()

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

        # **NEW**: Update the restore button after window visibility changes
        self.update_restore_action()

    def show_window(self):
        self.window.showNormal()
        self.window.raise_()
        self.window.activateWindow()

        # **NEW**: Update the restore button after window visibility changes
        self.update_restore_action()

    def show_settings(self):
        dialog = QDialog(self.window)
        dialog.setWindowTitle("Settings")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout(dialog)
        settings_ui = SettingsUI(dialog)
        layout.addWidget(settings_ui)

        # center dialog on screen
        self.center_dialog_on_screen(dialog)
        
        dialog.exec()

    def center_dialog_on_screen(self, dialog: QDialog):
        # Get the screen where the dialog's parent window is currently located
        parent_widget = dialog.parent() if dialog.parent() else QApplication.activeWindow()
    
        if parent_widget:
            screen = QApplication.screenAt(parent_widget.geometry().center())
        else:
            screen = QApplication.primaryScreen()

        if not screen:
            screen = QApplication.primaryScreen()

        # Get the geometry of the current screen
        screen_geometry = screen.availableGeometry()

        # Calculate position to center the dialog on the screen
        dialog_rect = dialog.geometry()
        x = (screen_geometry.width() - dialog_rect.width()) // 2
        y = (screen_geometry.height() - dialog_rect.height()) // 2

        # Move the dialog to the center of the screen
        dialog.move(screen_geometry.left() + x, screen_geometry.top() + y)

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

    def update_restore_action(self):
        """Update the visibility of the restore action based on window visibility."""
        if self.window.isVisible():
            self.restore.setVisible(False)  # Hide restore button when window is visible
        else:
            self.restore.setVisible(True)   # Show restore button when window is hidden
