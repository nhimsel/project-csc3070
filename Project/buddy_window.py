import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QSystemTrayIcon
from tray import TrayIcon

anim_dir = "anims"

class ShapedWindow(QWidget):
    cur_anim = "feesh"

    def __init__(self, animation):
        anim_name=animation+".gif"
        image_path=os.path.join(anim_dir, anim_name)
        super().__init__()
        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.offset = None

        self.movie = None
        self.set_image(image_path)

        self.tray = TrayIcon(self)

    # --- Load and display a new image or GIF ---
    def set_image(self, image_path):
        """Switch the displayed image or animation dynamically."""
        self.image_path = image_path
        is_gif = image_path.lower().endswith(".gif")

        # Stop previous movie if it exists
        if self.movie:
            self.movie.stop()
            self.movie.deleteLater()
            self.movie = None

        if is_gif:
            self._init_gif()
        else:
            self._init_static()

    def _init_static(self):
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)
        self.label.setMask(pixmap.mask())
        self.resize(pixmap.size())

    def _init_gif(self):
        self.movie = QMovie(self.image_path)
        self.label.setMovie(self.movie)
        self.movie.frameChanged.connect(self._update_mask)
        self.movie.start()

        first_frame = self.movie.currentPixmap()
        if not first_frame.isNull():
            self.resize(first_frame.size())

    def _update_mask(self):
        pix = self.movie.currentPixmap()
        if not pix.isNull():
            self.label.setMask(pix.mask())
            self.resize(pix.size())

    def switch_gif(self, animation):
        anim_name=animation+".gif"
        image_path=os.path.join(anim_dir, anim_name)
        self.set_image(image_path)
        self.cur_anim=animation

    # --- Dragging behavior ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            #self.offset = event.pos()
            print(self.cur_anim)
            if (self.cur_anim == "feesh"):
                self.switch_gif("feesh-2")
            else:
                self.switch_gif("feesh")


    def mouseMoveEvent(self, event):
        if self.offset and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                self.raise_()
                self.activateWindow()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()
